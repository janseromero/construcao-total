"""Execução: NF, Apropriação, Apontamento, Lançamento manual."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_proprietario
from app.db.session import get_db
from app.models.catalogo import Insumo
from app.models.execucao import (
    ApontamentoMaoObra,
    ApropriacaoCusto,
    ApropriacaoOrigem,
    LancamentoManual,
    NotaFiscal,
    NotaFiscalItem,
)
from app.models.obra import EAP, Obra
from app.models.user import User
from app.schemas.execucao import (
    ApontamentoIn,
    ApontamentoOut,
    ApropriacaoIn,
    ApropriacaoOut,
    LancamentoManualIn,
    LancamentoManualOut,
    NotaFiscalIn,
    NotaFiscalItemOut,
    NotaFiscalOut,
)
from app.services.apropriacao import atualizar_status_nf, validar_apropriacao_nf_item

router = APIRouter(tags=["execucao"])


def _check_obra(db: Session, user: User, obra_id: UUID) -> Obra:
    obra = db.get(Obra, obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Obra não encontrada")
    return obra


# ----- Notas Fiscais -----


def _serialize_nf(db: Session, nf: NotaFiscal) -> NotaFiscalOut:
    itens = list(db.scalars(select(NotaFiscalItem).where(NotaFiscalItem.nota_fiscal_id == nf.id)))
    return NotaFiscalOut(
        id=nf.id,
        obra_id=nf.obra_id,
        fornecedor_id=nf.fornecedor_id,
        numero=nf.numero,
        serie=nf.serie,
        chave_acesso=nf.chave_acesso,
        data_emissao=nf.data_emissao,
        valor_total=nf.valor_total,
        valor_produtos=nf.valor_produtos,
        valor_servicos=nf.valor_servicos,
        valor_impostos=nf.valor_impostos,
        status=nf.status,
        itens=[NotaFiscalItemOut.model_validate(i) for i in itens],
    )


@router.get("/notas-fiscais", response_model=list[NotaFiscalOut])
def list_nfs(
    obra_id: UUID | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = select(NotaFiscal).where(NotaFiscal.tenant_id == user.tenant_id)
    if obra_id is not None:
        q = q.where(NotaFiscal.obra_id == obra_id)
    nfs = list(db.scalars(q.order_by(NotaFiscal.data_emissao.desc())))
    return [_serialize_nf(db, nf) for nf in nfs]


@router.post("/notas-fiscais", response_model=NotaFiscalOut, status_code=status.HTTP_201_CREATED)
def create_nf(
    payload: NotaFiscalIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    if payload.obra_id is not None:
        _check_obra(db, user, payload.obra_id)
    nf = NotaFiscal(
        tenant_id=user.tenant_id,
        obra_id=payload.obra_id,
        fornecedor_id=payload.fornecedor_id,
        numero=payload.numero,
        serie=payload.serie,
        chave_acesso=payload.chave_acesso,
        data_emissao=payload.data_emissao,
        valor_total=payload.valor_total,
        valor_produtos=payload.valor_produtos,
        valor_servicos=payload.valor_servicos,
        valor_impostos=payload.valor_impostos,
    )
    db.add(nf)
    db.flush()
    for item in payload.itens:
        db.add(NotaFiscalItem(nota_fiscal_id=nf.id, **item.model_dump()))
    db.commit()
    db.refresh(nf)
    return _serialize_nf(db, nf)


@router.get("/notas-fiscais/{nf_id}", response_model=NotaFiscalOut)
def get_nf(nf_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    nf = db.get(NotaFiscal, nf_id)
    if nf is None or nf.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "NF não encontrada")
    return _serialize_nf(db, nf)


@router.delete("/notas-fiscais/{nf_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nf(
    nf_id: UUID, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    nf = db.get(NotaFiscal, nf_id)
    if nf is None or nf.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "NF não encontrada")
    db.delete(nf)
    db.commit()


# ----- Apropriações -----


@router.post("/apropriacoes", response_model=ApropriacaoOut, status_code=status.HTTP_201_CREATED)
def criar_apropriacao(
    payload: ApropriacaoIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _check_obra(db, user, payload.obra_id)
    eap = db.get(EAP, payload.eap_id)
    if eap is None or eap.obra_id != payload.obra_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "EAP inválida para esta obra")

    if payload.origem_tipo == ApropriacaoOrigem.nota_fiscal_item:
        try:
            validar_apropriacao_nf_item(
                db, nf_item_id=payload.origem_id, novo_valor=payload.valor
            )
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    ap = ApropriacaoCusto(
        tenant_id=user.tenant_id,
        obra_id=payload.obra_id,
        eap_id=payload.eap_id,
        origem_tipo=payload.origem_tipo,
        origem_id=payload.origem_id,
        valor=payload.valor,
        quantidade=payload.quantidade,
        data_competencia=payload.data_competencia,
        descricao=payload.descricao,
        created_by_user_id=user.id,
    )
    db.add(ap)
    db.flush()
    if payload.origem_tipo == ApropriacaoOrigem.nota_fiscal_item:
        nf_item = db.get(NotaFiscalItem, payload.origem_id)
        if nf_item:
            atualizar_status_nf(db, nf_item.nota_fiscal_id)
    db.commit()
    db.refresh(ap)
    return ap


@router.get("/apropriacoes", response_model=list[ApropriacaoOut])
def list_apropriacoes(
    obra_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _check_obra(db, user, obra_id)
    return list(
        db.scalars(
            select(ApropriacaoCusto)
            .where(ApropriacaoCusto.obra_id == obra_id)
            .order_by(ApropriacaoCusto.data_competencia.desc())
        )
    )


@router.delete("/apropriacoes/{ap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apropriacao(
    ap_id: UUID, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    ap = db.get(ApropriacaoCusto, ap_id)
    if ap is None or ap.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Apropriação não encontrada")
    origem_tipo = ap.origem_tipo
    origem_id = ap.origem_id
    db.delete(ap)
    db.flush()
    if origem_tipo == ApropriacaoOrigem.nota_fiscal_item:
        nf_item = db.get(NotaFiscalItem, origem_id)
        if nf_item:
            atualizar_status_nf(db, nf_item.nota_fiscal_id)
    db.commit()


# ----- Apontamento de mão de obra -----


def _mask_apontamento(user: User, ap: ApontamentoMaoObra) -> ApontamentoOut:
    """Mascara valores para operacional."""
    from app.models.user import UserRole

    data = ApontamentoOut(
        id=ap.id,
        obra_id=ap.obra_id,
        eap_id=ap.eap_id,
        data=ap.data,
        insumo_id=ap.insumo_id,
        quantidade=ap.quantidade,
        valor_total=ap.valor_total if user.role == UserRole.proprietario else None,
    )
    return data


@router.post("/apontamentos", response_model=ApontamentoOut, status_code=status.HTTP_201_CREATED)
def criar_apontamento(
    payload: ApontamentoIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _check_obra(db, user, payload.obra_id)
    insumo = db.get(Insumo, payload.insumo_id)
    if insumo is None or insumo.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insumo inválido")
    custo_unit = insumo.custo_unitario_referencia or Decimal("0")
    valor_total = (payload.quantidade * custo_unit).quantize(Decimal("0.0001"))
    ap = ApontamentoMaoObra(
        tenant_id=user.tenant_id,
        obra_id=payload.obra_id,
        eap_id=payload.eap_id,
        data=payload.data,
        insumo_id=payload.insumo_id,
        quantidade=payload.quantidade,
        custo_unitario_snapshot=custo_unit,
        valor_total=valor_total,
        observacao=payload.observacao,
    )
    db.add(ap)
    db.flush()
    # Gera apropriação automática
    db.add(
        ApropriacaoCusto(
            tenant_id=user.tenant_id,
            obra_id=payload.obra_id,
            eap_id=payload.eap_id,
            origem_tipo=ApropriacaoOrigem.apontamento_mao_obra,
            origem_id=ap.id,
            valor=valor_total,
            quantidade=payload.quantidade,
            data_competencia=payload.data,
            descricao=payload.observacao or "Apontamento de mão de obra",
            created_by_user_id=user.id,
        )
    )
    db.commit()
    db.refresh(ap)
    return _mask_apontamento(user, ap)


@router.get("/apontamentos", response_model=list[ApontamentoOut])
def list_apontamentos(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    aps = list(
        db.scalars(
            select(ApontamentoMaoObra)
            .where(ApontamentoMaoObra.obra_id == obra_id)
            .order_by(ApontamentoMaoObra.data.desc())
        )
    )
    return [_mask_apontamento(user, ap) for ap in aps]


# ----- Lançamento manual (proprietário) -----


@router.post(
    "/lancamentos-manuais",
    response_model=LancamentoManualOut,
    status_code=status.HTTP_201_CREATED,
)
def criar_lancamento(
    payload: LancamentoManualIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    _check_obra(db, user, payload.obra_id)
    lm = LancamentoManual(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(lm)
    db.flush()
    db.add(
        ApropriacaoCusto(
            tenant_id=user.tenant_id,
            obra_id=payload.obra_id,
            eap_id=payload.eap_id,
            origem_tipo=ApropriacaoOrigem.lancamento_manual,
            origem_id=lm.id,
            valor=payload.valor,
            data_competencia=payload.data,
            descricao=payload.descricao,
            created_by_user_id=user.id,
        )
    )
    db.commit()
    db.refresh(lm)
    return lm


@router.get("/lancamentos-manuais", response_model=list[LancamentoManualOut])
def list_lancamentos(
    obra_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    _check_obra(db, user, obra_id)
    return list(
        db.scalars(
            select(LancamentoManual)
            .where(LancamentoManual.obra_id == obra_id)
            .order_by(LancamentoManual.data.desc())
        )
    )
