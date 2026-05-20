"""Fornecedores, insumos, composições."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.catalogo import Composicao, ComposicaoInsumo, Fornecedor, Insumo
from app.models.user import User
from app.schemas.catalogo import (
    ComposicaoIn,
    ComposicaoInsumoOut,
    ComposicaoOut,
    FornecedorIn,
    FornecedorOut,
    InsumoIn,
    InsumoOut,
)
from app.services.composicao import recalcular_custo, snapshot_de

router = APIRouter(tags=["catalogo"])

# ----- Fornecedores -----


@router.get("/fornecedores", response_model=list[FornecedorOut])
def list_fornecedores(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(
        db.scalars(
            select(Fornecedor).where(Fornecedor.tenant_id == user.tenant_id).order_by(Fornecedor.nome)
        )
    )


@router.post("/fornecedores", response_model=FornecedorOut, status_code=status.HTTP_201_CREATED)
def create_fornecedor(
    payload: FornecedorIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    f = Fornecedor(**payload.model_dump(), tenant_id=user.tenant_id)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


@router.put("/fornecedores/{forn_id}", response_model=FornecedorOut)
def update_fornecedor(
    forn_id: UUID,
    payload: FornecedorIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    f = db.get(Fornecedor, forn_id)
    if f is None or f.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Fornecedor não encontrado")
    for k, v in payload.model_dump().items():
        setattr(f, k, v)
    db.commit()
    db.refresh(f)
    return f


@router.delete("/fornecedores/{forn_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fornecedor(
    forn_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    f = db.get(Fornecedor, forn_id)
    if f is None or f.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Fornecedor não encontrado")
    db.delete(f)
    db.commit()


# ----- Insumos -----


@router.get("/insumos", response_model=list[InsumoOut])
def list_insumos(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(
        db.scalars(
            select(Insumo).where(Insumo.tenant_id == user.tenant_id).order_by(Insumo.codigo)
        )
    )


@router.post("/insumos", response_model=InsumoOut, status_code=status.HTTP_201_CREATED)
def create_insumo(
    payload: InsumoIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    i = Insumo(**payload.model_dump(), tenant_id=user.tenant_id)
    db.add(i)
    db.commit()
    db.refresh(i)
    return i


@router.put("/insumos/{insumo_id}", response_model=InsumoOut)
def update_insumo(
    insumo_id: UUID,
    payload: InsumoIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    i = db.get(Insumo, insumo_id)
    if i is None or i.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Insumo não encontrado")
    for k, v in payload.model_dump().items():
        setattr(i, k, v)
    db.commit()
    db.refresh(i)
    return i


@router.delete("/insumos/{insumo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_insumo(
    insumo_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    i = db.get(Insumo, insumo_id)
    if i is None or i.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Insumo não encontrado")
    db.delete(i)
    db.commit()


# ----- Composições -----


def _serialize_composicao(db: Session, c: Composicao) -> ComposicaoOut:
    linhas = list(
        db.scalars(select(ComposicaoInsumo).where(ComposicaoInsumo.composicao_id == c.id))
    )
    return ComposicaoOut(
        id=c.id,
        codigo=c.codigo,
        descricao=c.descricao,
        unidade=c.unidade,
        sinapi_codigo=c.sinapi_codigo,
        custo_unitario_calculado=c.custo_unitario_calculado,
        insumos=[ComposicaoInsumoOut.model_validate(ln) for ln in linhas],
    )


@router.get("/composicoes", response_model=list[ComposicaoOut])
def list_composicoes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cs = list(
        db.scalars(
            select(Composicao).where(Composicao.tenant_id == user.tenant_id).order_by(Composicao.codigo)
        )
    )
    return [_serialize_composicao(db, c) for c in cs]


@router.post("/composicoes", response_model=ComposicaoOut, status_code=status.HTTP_201_CREATED)
def create_composicao(
    payload: ComposicaoIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    c = Composicao(
        tenant_id=user.tenant_id,
        codigo=payload.codigo,
        descricao=payload.descricao,
        unidade=payload.unidade,
        sinapi_codigo=payload.sinapi_codigo,
    )
    db.add(c)
    db.flush()
    for ln in payload.insumos:
        insumo = db.get(Insumo, ln.insumo_id)
        if insumo is None or insumo.tenant_id != user.tenant_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Insumo {ln.insumo_id} inválido")
        db.add(
            ComposicaoInsumo(
                composicao_id=c.id,
                insumo_id=ln.insumo_id,
                coeficiente=ln.coeficiente,
                custo_unitario_snapshot=snapshot_de(ln.insumo_id, db),
            )
        )
    db.flush()
    recalcular_custo(db, c.id)
    db.commit()
    db.refresh(c)
    return _serialize_composicao(db, c)


@router.put("/composicoes/{c_id}", response_model=ComposicaoOut)
def update_composicao(
    c_id: UUID,
    payload: ComposicaoIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    c = db.get(Composicao, c_id)
    if c is None or c.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Composição não encontrada")
    c.codigo = payload.codigo
    c.descricao = payload.descricao
    c.unidade = payload.unidade
    c.sinapi_codigo = payload.sinapi_codigo
    db.query(ComposicaoInsumo).filter(ComposicaoInsumo.composicao_id == c_id).delete()
    db.flush()
    for ln in payload.insumos:
        insumo = db.get(Insumo, ln.insumo_id)
        if insumo is None or insumo.tenant_id != user.tenant_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Insumo {ln.insumo_id} inválido")
        db.add(
            ComposicaoInsumo(
                composicao_id=c.id,
                insumo_id=ln.insumo_id,
                coeficiente=ln.coeficiente,
                custo_unitario_snapshot=snapshot_de(ln.insumo_id, db),
            )
        )
    db.flush()
    recalcular_custo(db, c.id)
    db.commit()
    db.refresh(c)
    return _serialize_composicao(db, c)


@router.delete("/composicoes/{c_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_composicao(
    c_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    c = db.get(Composicao, c_id)
    if c is None or c.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Composição não encontrada")
    db.delete(c)
    db.commit()
