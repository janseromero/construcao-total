"""Helpers de composição."""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalogo import Composicao, ComposicaoInsumo, Insumo


def recalcular_custo(db: Session, composicao_id: UUID) -> Decimal:
    composicao = db.get(Composicao, composicao_id)
    if composicao is None:
        raise ValueError("Composição não encontrada")
    linhas = list(
        db.scalars(select(ComposicaoInsumo).where(ComposicaoInsumo.composicao_id == composicao_id))
    )
    total = Decimal("0")
    for ln in linhas:
        total += (ln.coeficiente or Decimal("0")) * (ln.custo_unitario_snapshot or Decimal("0"))
    composicao.custo_unitario_calculado = total.quantize(Decimal("0.0001"))
    return composicao.custo_unitario_calculado


def snapshot_de(insumo_id: UUID, db: Session) -> Decimal:
    insumo = db.get(Insumo, insumo_id)
    if insumo is None:
        raise ValueError("Insumo não encontrado")
    return insumo.custo_unitario_referencia or Decimal("0")
