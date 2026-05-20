"""Relatórios de análise."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_proprietario
from app.db.session import get_db
from app.models.obra import Obra
from app.models.user import User
from app.schemas.rateio import CustoUnidadeRow, MargemUnidadeRow, OrcadoVsRealizadoRow
from app.services.analise import custo_por_unidade, margem_por_unidade, orcado_vs_realizado

router = APIRouter(prefix="/obras/{obra_id}/analise", tags=["analise"])


def _check_obra(db: Session, user: User, obra_id: UUID) -> None:
    obra = db.get(Obra, obra_id)
    if obra is None or obra.tenant_id != user.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Obra não encontrada")


@router.get("/custo-por-unidade", response_model=list[CustoUnidadeRow])
def custo_unidade(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    return custo_por_unidade(db, obra_id)


@router.get("/margem-por-unidade", response_model=list[MargemUnidadeRow])
def margem_unidade(
    obra_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    _check_obra(db, user, obra_id)
    return margem_por_unidade(db, obra_id)


@router.get("/orcado-vs-realizado", response_model=list[OrcadoVsRealizadoRow])
def orcado_real(
    obra_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    _check_obra(db, user, obra_id)
    return orcado_vs_realizado(db, obra_id)


@router.get("/resumo")
def resumo(
    obra_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_proprietario),
):
    """Resumo executivo: VGV, custo total, margem total."""
    _check_obra(db, user, obra_id)
    margens = margem_por_unidade(db, obra_id)
    vgv = sum((m.preco_venda or Decimal("0") for m in margens), Decimal("0"))
    custo = sum((m.custo_acumulado for m in margens), Decimal("0"))
    margem = vgv - custo
    pct = (margem / vgv * Decimal("100")) if vgv > 0 else None
    return {
        "vgv": float(vgv),
        "custo_total": float(custo),
        "margem_total": float(margem),
        "margem_percentual": float(pct) if pct is not None else None,
        "unidades_total": len(margens),
        "unidades_vendidas": sum(1 for m in margens if m.preco_venda),
    }
