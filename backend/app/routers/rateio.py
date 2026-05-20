"""Rateio: regras + recálculo manual."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_proprietario
from app.db.session import get_db
from app.models.obra import Obra
from app.models.rateio import RegraRateio, RegraRateioPesoUnidade
from app.models.user import User
from app.schemas.rateio import RegraRateioIn, RegraRateioOut
from app.services.rateio import calcular_rateio

router = APIRouter(prefix="/obras/{obra_id}/rateio", tags=["rateio"])


def _check_obra(db: Session, user: User, obra_id: UUID) -> None:
    obra = db.get(Obra, obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Obra não encontrada")


@router.get("/regras", response_model=list[RegraRateioOut])
def list_regras(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    return list(db.scalars(select(RegraRateio).where(RegraRateio.obra_id == obra_id)))


@router.post("/regras", response_model=RegraRateioOut, status_code=status.HTTP_201_CREATED)
def create_regra(
    obra_id: UUID,
    payload: RegraRateioIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    _check_obra(db, user, obra_id)
    regra = RegraRateio(
        obra_id=obra_id,
        escopo_tipo=payload.escopo_tipo,
        escopo_eap_id=payload.escopo_eap_id,
        criterio=payload.criterio,
        ativo=True,
    )
    db.add(regra)
    db.flush()
    for p in payload.pesos:
        db.add(
            RegraRateioPesoUnidade(
                regra_rateio_id=regra.id, unidade_id=p.unidade_id, peso=p.peso
            )
        )
    db.commit()
    db.refresh(regra)
    return regra


@router.delete("/regras/{regra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_regra(
    obra_id: UUID,
    regra_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    _check_obra(db, user, obra_id)
    regra = db.get(RegraRateio, regra_id)
    if regra is None or regra.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Regra não encontrada")
    db.delete(regra)
    db.commit()


@router.post("/recalcular", status_code=status.HTTP_200_OK)
def recalcular(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    result = calcular_rateio(db, obra_id)
    db.commit()
    return {"unidades_atualizadas": len(result)}
