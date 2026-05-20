"""Obras + tipologias + unidades + EAP."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.obra import EAP, Obra, Tipologia, Unidade
from app.models.rateio import RateioCriterio, RateioEscopo, RegraRateio
from app.models.user import User
from app.schemas.obra import (
    EAPIn,
    EAPOut,
    ObraIn,
    ObraOut,
    TipologiaIn,
    TipologiaOut,
    UnidadeIn,
    UnidadeOut,
)

router = APIRouter(prefix="/obras", tags=["obras"])


def _get_obra(db: Session, user: User, obra_id: UUID) -> Obra:
    obra = db.get(Obra, obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Obra não encontrada")
    return obra


@router.get("", response_model=list[ObraOut])
def list_obras(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(db.scalars(select(Obra).where(Obra.tenant_id == user.tenant_id).order_by(Obra.created_at.desc())))


@router.post("", response_model=ObraOut, status_code=status.HTTP_201_CREATED)
def create_obra(
    payload: ObraIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    obra = Obra(**payload.model_dump(), tenant_id=user.tenant_id)
    db.add(obra)
    db.flush()
    # Regra de rateio default: obra inteira / fração ideal
    db.add(
        RegraRateio(
            obra_id=obra.id,
            escopo_tipo=RateioEscopo.obra_inteira,
            criterio=RateioCriterio.fracao_ideal,
            ativo=True,
        )
    )
    db.commit()
    db.refresh(obra)
    return obra


@router.get("/{obra_id}", response_model=ObraOut)
def get_obra(obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return _get_obra(db, user, obra_id)


@router.put("/{obra_id}", response_model=ObraOut)
def update_obra(
    obra_id: UUID,
    payload: ObraIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    obra = _get_obra(db, user, obra_id)
    for k, v in payload.model_dump().items():
        setattr(obra, k, v)
    db.commit()
    db.refresh(obra)
    return obra


@router.delete("/{obra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_obra(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    obra = _get_obra(db, user, obra_id)
    db.delete(obra)
    db.commit()


# ----- Tipologias -----


@router.get("/{obra_id}/tipologias", response_model=list[TipologiaOut])
def list_tipologias(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _get_obra(db, user, obra_id)
    return list(db.scalars(select(Tipologia).where(Tipologia.obra_id == obra_id)))


@router.post(
    "/{obra_id}/tipologias", response_model=TipologiaOut, status_code=status.HTTP_201_CREATED
)
def create_tipologia(
    obra_id: UUID,
    payload: TipologiaIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    tip = Tipologia(**payload.model_dump(), obra_id=obra_id)
    db.add(tip)
    db.commit()
    db.refresh(tip)
    return tip


@router.put("/{obra_id}/tipologias/{tip_id}", response_model=TipologiaOut)
def update_tipologia(
    obra_id: UUID,
    tip_id: UUID,
    payload: TipologiaIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    tip = db.get(Tipologia, tip_id)
    if tip is None or tip.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tipologia não encontrada")
    for k, v in payload.model_dump().items():
        setattr(tip, k, v)
    db.commit()
    db.refresh(tip)
    return tip


@router.delete("/{obra_id}/tipologias/{tip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipologia(
    obra_id: UUID,
    tip_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    tip = db.get(Tipologia, tip_id)
    if tip is None or tip.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tipologia não encontrada")
    db.delete(tip)
    db.commit()


# ----- Unidades -----


@router.get("/{obra_id}/unidades", response_model=list[UnidadeOut])
def list_unidades(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _get_obra(db, user, obra_id)
    return list(
        db.scalars(
            select(Unidade).where(Unidade.obra_id == obra_id).order_by(Unidade.identificador)
        )
    )


@router.post(
    "/{obra_id}/unidades", response_model=UnidadeOut, status_code=status.HTTP_201_CREATED
)
def create_unidade(
    obra_id: UUID,
    payload: UnidadeIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    unidade = Unidade(**payload.model_dump(), obra_id=obra_id)
    db.add(unidade)
    db.commit()
    db.refresh(unidade)
    return unidade


@router.put("/{obra_id}/unidades/{unidade_id}", response_model=UnidadeOut)
def update_unidade(
    obra_id: UUID,
    unidade_id: UUID,
    payload: UnidadeIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    unidade = db.get(Unidade, unidade_id)
    if unidade is None or unidade.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unidade não encontrada")
    for k, v in payload.model_dump().items():
        setattr(unidade, k, v)
    db.commit()
    db.refresh(unidade)
    return unidade


@router.delete("/{obra_id}/unidades/{unidade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unidade(
    obra_id: UUID,
    unidade_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    unidade = db.get(Unidade, unidade_id)
    if unidade is None or unidade.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unidade não encontrada")
    db.delete(unidade)
    db.commit()


# ----- EAP -----


@router.get("/{obra_id}/eap", response_model=list[EAPOut])
def list_eap(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _get_obra(db, user, obra_id)
    return list(
        db.scalars(select(EAP).where(EAP.obra_id == obra_id).order_by(EAP.nivel, EAP.ordem, EAP.codigo))
    )


@router.post("/{obra_id}/eap", response_model=EAPOut, status_code=status.HTTP_201_CREATED)
def create_eap(
    obra_id: UUID,
    payload: EAPIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    nivel = 1
    if payload.parent_id:
        parent = db.get(EAP, payload.parent_id)
        if parent is None or parent.obra_id != obra_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Parent EAP inválido")
        nivel = parent.nivel + 1
    eap = EAP(**payload.model_dump(), obra_id=obra_id, nivel=nivel)
    db.add(eap)
    db.commit()
    db.refresh(eap)
    return eap


@router.delete("/{obra_id}/eap/{eap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_eap(
    obra_id: UUID,
    eap_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_obra(db, user, obra_id)
    eap = db.get(EAP, eap_id)
    if eap is None or eap.obra_id != obra_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "EAP não encontrada")
    db.delete(eap)
    db.commit()
