"""Catálogo: fornecedor, insumo, composição."""

from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class FornecedorTipo(StrEnum):
    material = "material"
    servico = "servico"
    equipamento = "equipamento"
    misto = "misto"


class Fornecedor(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "fornecedor"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cnpj_cpf: Mapped[str | None] = mapped_column(String(20))
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[FornecedorTipo] = mapped_column(
        SAEnum(FornecedorTipo, name="fornecedor_tipo"),
        default=FornecedorTipo.material,
        nullable=False,
    )
    contato: Mapped[str | None] = mapped_column(String(200))
    observacoes: Mapped[str | None] = mapped_column(Text)


class InsumoTipo(StrEnum):
    material = "material"
    mao_obra = "mao_obra"
    equipamento = "equipamento"


class Insumo(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "insumo"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_insumo_codigo"),)

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    tipo: Mapped[InsumoTipo] = mapped_column(
        SAEnum(InsumoTipo, name="insumo_tipo"), default=InsumoTipo.material, nullable=False
    )
    sinapi_codigo: Mapped[str | None] = mapped_column(String(20))
    custo_unitario_referencia: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )


class Composicao(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "composicao"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_composicao_codigo"),)

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    sinapi_codigo: Mapped[str | None] = mapped_column(String(20))
    custo_unitario_calculado: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )


class ComposicaoInsumo(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "composicao_insumo"

    composicao_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("composicao.id", ondelete="CASCADE"), nullable=False
    )
    insumo_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("insumo.id", ondelete="RESTRICT"), nullable=False
    )
    coeficiente: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    custo_unitario_snapshot: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
