"""Vendas: comprador + venda."""

from datetime import date
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Comprador(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "comprador"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    cpf_cnpj: Mapped[str | None] = mapped_column(String(20))
    contato: Mapped[str | None] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(255))


class VendaStatus(StrEnum):
    disponivel = "disponivel"
    reservada = "reservada"
    vendida = "vendida"
    distratada = "distratada"


class Venda(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "venda"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unidade_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False, index=True
    )
    comprador_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("comprador.id", ondelete="SET NULL")
    )
    preco_tabela: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    preco_venda_final: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    data_venda: Mapped[date | None] = mapped_column(Date)
    status: Mapped[VendaStatus] = mapped_column(
        SAEnum(VendaStatus, name="venda_status"), default=VendaStatus.disponivel, nullable=False
    )
    observacoes: Mapped[str | None] = mapped_column(Text)
