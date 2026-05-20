"""Orçamentos versionados + itens."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_proprietario
from app.db.session import get_db
from app.models.obra import EAP, Obra
from app.models.orcamento import Orcamento, OrcamentoItem, OrcamentoStatus
from app.models.user import User
from app.schemas.orcamento import OrcamentoIn, OrcamentoItemIn, OrcamentoItemOut, OrcamentoOut

router = APIRouter(prefix="/obras/{obra_id}/orcamentos", tags=["orcamentos"])


def _check_obra(db: Session, user: User, obra_id: UUID) -> None:
    obra = db.get(Obra, obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Obra não encontrada")


def _get_orc(db: Session, user: User, obra_id: UUID, orc_id: UUID) -> Orcamento:
    _check_obra(db, user, obra_id)
    o = db.get(Orcamento, orc_id)
    if o is None or o.obra_id != obra_id or o.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Orçamento não encontrado")
    return o


@router.get("", response_model=list[OrcamentoOut])
def list_orcamentos(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    return list(
        db.scalars(
            select(Orcamento).where(Orcamento.obra_id == obra_id).order_by(Orcamento.versao.desc())
        )
    )


@router.post("", response_model=OrcamentoOut, status_code=status.HTTP_201_CREATED)
def create_orcamento(
    obra_id: UUID,
    payload: OrcamentoIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _check_obra(db, user, obra_id)
    max_versao = db.scalar(
        select(Orcamento.versao).where(Orcamento.obra_id == obra_id).order_by(Orcamento.versao.desc())
    )
    versao = (max_versao or 0) + 1
    o = Orcamento(
        tenant_id=user.tenant_id,
        obra_id=obra_id,
        versao=versao,
        nome=payload.nome,
        status=OrcamentoStatus.rascunho,
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


@router.post("/{orc_id}/aprovar", response_model=OrcamentoOut)
def aprovar(
    obra_id: UUID,
    orc_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    o = _get_orc(db, user, obra_id, orc_id)
    if o.status != OrcamentoStatus.rascunho:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Só rascunhos podem ser aprovados")
    # Marca anterior aprovado como superado
    anterior = db.scalar(
        select(Orcamento).where(
            Orcamento.obra_id == obra_id,
            Orcamento.status == OrcamentoStatus.aprovado,
            Orcamento.id != orc_id,
        )
    )
    if anterior:
        anterior.status = OrcamentoStatus.superado
    o.status = OrcamentoStatus.aprovado
    o.data_aprovacao = datetime.now(UTC)
    o.aprovado_por_user_id = user.id
    db.commit()
    db.refresh(o)
    return o


@router.delete("/{orc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_orcamento(
    obra_id: UUID,
    orc_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    o = _get_orc(db, user, obra_id, orc_id)
    if o.status == OrcamentoStatus.aprovado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Não é possível remover orçamento aprovado")
    db.delete(o)
    db.commit()


# ----- Itens -----


@router.get("/{orc_id}/itens", response_model=list[OrcamentoItemOut])
def list_itens(
    obra_id: UUID,
    orc_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_orc(db, user, obra_id, orc_id)
    return list(db.scalars(select(OrcamentoItem).where(OrcamentoItem.orcamento_id == orc_id)))


@router.post("/{orc_id}/itens", response_model=OrcamentoItemOut, status_code=status.HTTP_201_CREATED)
def add_item(
    obra_id: UUID,
    orc_id: UUID,
    payload: OrcamentoItemIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    o = _get_orc(db, user, obra_id, orc_id)
    if o.status != OrcamentoStatus.rascunho:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Só rascunhos aceitam itens novos")
    eap = db.get(EAP, payload.eap_id)
    if eap is None or eap.obra_id != obra_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "EAP inválida")
    custo_total = (payload.quantidade or Decimal("0")) * (payload.custo_unitario or Decimal("0"))
    item = OrcamentoItem(
        orcamento_id=orc_id,
        eap_id=payload.eap_id,
        composicao_id=payload.composicao_id,
        descricao=payload.descricao,
        unidade=payload.unidade,
        quantidade=payload.quantidade,
        custo_unitario=payload.custo_unitario,
        custo_total=custo_total.quantize(Decimal("0.0001")),
    )
    db.add(item)
    db.flush()
    # Recalcula total do orçamento
    total = db.scalar(
        select(OrcamentoItem.custo_total).where(OrcamentoItem.orcamento_id == orc_id)
    )
    soma = sum(
        (i.custo_total for i in db.scalars(select(OrcamentoItem).where(OrcamentoItem.orcamento_id == orc_id))),
        Decimal("0"),
    )
    o.custo_total_calculado = soma.quantize(Decimal("0.0001"))
    _ = total
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{orc_id}/itens/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(
    obra_id: UUID,
    orc_id: UUID,
    item_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    o = _get_orc(db, user, obra_id, orc_id)
    if o.status != OrcamentoStatus.rascunho:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Só rascunhos podem ser editados")
    item = db.get(OrcamentoItem, item_id)
    if item is None or item.orcamento_id != orc_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item não encontrado")
    db.delete(item)
    db.flush()
    soma = sum(
        (i.custo_total for i in db.scalars(select(OrcamentoItem).where(OrcamentoItem.orcamento_id == orc_id))),
        Decimal("0"),
    )
    o.custo_total_calculado = soma.quantize(Decimal("0.0001"))
    db.commit()
