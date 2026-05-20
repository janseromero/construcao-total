"""Rateio: regras + resultado calculado."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class RateioEscopo(StrEnum):
    obra_inteira = "obra_inteira"
    eap = "eap"


class RateioCriterio(StrEnum):
    fracao_ideal = "fracao_ideal"
    area_privativa = "area_privativa"
    igualitario = "igualitario"
    customizado = "customizado"


class RegraRateio(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "regra_rateio"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    escopo_tipo: Mapped[RateioEscopo] = mapped_column(
        SAEnum(RateioEscopo, name="rateio_escopo"), nullable=False
    )
    escopo_eap_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="CASCADE")
    )
    criterio: Mapped[RateioCriterio] = mapped_column(
        SAEnum(RateioCriterio, name="rateio_criterio"), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    vigente_desde: Mapped[date | None] = mapped_column(Date)


class RegraRateioPesoUnidade(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "regra_rateio_peso_unidade"

    regra_rateio_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("regra_rateio.id", ondelete="CASCADE"), nullable=False
    )
    unidade_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False
    )
    peso: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)


class RateioCalculado(Base, UUIDPKMixin, TimestampMixin):
    """Cache do cálculo de rateio por unidade (e opcionalmente por EAP)."""

    __tablename__ = "rateio_calculado"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unidade_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="CASCADE")
    )
    custo_acumulado: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    calculado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
