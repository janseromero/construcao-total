"""Orçamento versionado."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class OrcamentoStatus(StrEnum):
    rascunho = "rascunho"
    aprovado = "aprovado"
    superado = "superado"


class Orcamento(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "orcamento"
    __table_args__ = (UniqueConstraint("obra_id", "versao", name="uq_orcamento_obra_versao"),)

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    versao: Mapped[int] = mapped_column(Integer, nullable=False)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[OrcamentoStatus] = mapped_column(
        SAEnum(OrcamentoStatus, name="orcamento_status"),
        default=OrcamentoStatus.rascunho,
        nullable=False,
    )
    data_aprovacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    aprovado_por_user_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("user_account.id", ondelete="SET NULL")
    )
    custo_total_calculado: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )


class OrcamentoItem(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "orcamento_item"

    orcamento_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("orcamento.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False
    )
    composicao_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("composicao.id", ondelete="SET NULL")
    )
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    custo_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    custo_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
