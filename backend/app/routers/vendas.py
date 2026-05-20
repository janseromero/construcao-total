"""Vendas + compradores (somente Proprietário)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_proprietario
from app.db.session import get_db
from app.models.user import User
from app.models.venda import Comprador, Venda
from app.schemas.venda import CompradorIn, CompradorOut, VendaIn, VendaOut

router = APIRouter(tags=["vendas"])


# ----- Compradores -----


@router.get("/compradores", response_model=list[CompradorOut])
def list_compradores(db: Session = Depends(get_db), user: User = Depends(require_proprietario)):
    return list(
        db.scalars(
            select(Comprador).where(Comprador.tenant_id == user.tenant_id).order_by(Comprador.nome)
        )
    )


@router.post("/compradores", response_model=CompradorOut, status_code=status.HTTP_201_CREATED)
def create_comprador(
    payload: CompradorIn, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    c = Comprador(**payload.model_dump(), tenant_id=user.tenant_id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/compradores/{c_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comprador(
    c_id: UUID, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    c = db.get(Comprador, c_id)
    if c is None or c.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Comprador não encontrado")
    db.delete(c)
    db.commit()


# ----- Vendas -----


@router.get("/vendas", response_model=list[VendaOut])
def list_vendas(
    obra_id: UUID | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    q = select(Venda).where(Venda.tenant_id == user.tenant_id)
    if obra_id is not None:
        from app.models.obra import Unidade

        q = q.join(Unidade, Unidade.id == Venda.unidade_id).where(Unidade.obra_id == obra_id)
    return list(db.scalars(q.order_by(Venda.created_at.desc())))


@router.post("/vendas", response_model=VendaOut, status_code=status.HTTP_201_CREATED)
def create_venda(
    payload: VendaIn, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    from app.models.obra import Obra, Unidade

    unidade = db.get(Unidade, payload.unidade_id)
    if unidade is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unidade inválida")
    obra = db.get(Obra, unidade.obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unidade fora do tenant")

    v = Venda(**payload.model_dump(), tenant_id=user.tenant_id)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.put("/vendas/{v_id}", response_model=VendaOut)
def update_venda(
    v_id: UUID,
    payload: VendaIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    v = db.get(Venda, v_id)
    if v is None or v.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Venda não encontrada")
    for k, val in payload.model_dump().items():
        setattr(v, k, val)
    db.commit()
    db.refresh(v)
    return v


@router.delete("/vendas/{v_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venda(
    v_id: UUID, db: Session = Depends(get_db), user: User = Depends(require_proprietario)
):
    v = db.get(Venda, v_id)
    if v is None or v.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Venda não encontrada")
    db.delete(v)
    db.commit()
