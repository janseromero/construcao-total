"""Execução: NF, apropriação, medição, apontamento, lançamento manual."""

from datetime import date
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class NotaFiscalStatus(StrEnum):
    pendente_apropriacao = "pendente_apropriacao"
    parcialmente_apropriada = "parcialmente_apropriada"
    totalmente_apropriada = "totalmente_apropriada"
    cancelada = "cancelada"


class NotaFiscal(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "nota_fiscal"
    __table_args__ = (
        UniqueConstraint("tenant_id", "chave_acesso", name="uq_nf_chave_acesso"),
    )

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    obra_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="SET NULL"), index=True
    )
    fornecedor_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("fornecedor.id", ondelete="RESTRICT"), nullable=False
    )
    numero: Mapped[str] = mapped_column(String(50), nullable=False)
    serie: Mapped[str | None] = mapped_column(String(10))
    chave_acesso: Mapped[str | None] = mapped_column(String(50))
    data_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    valor_produtos: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )
    valor_servicos: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )
    valor_impostos: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), default=Decimal("0"), nullable=False
    )
    status: Mapped[NotaFiscalStatus] = mapped_column(
        SAEnum(NotaFiscalStatus, name="nf_status"),
        default=NotaFiscalStatus.pendente_apropriacao,
        nullable=False,
    )
    xml_original: Mapped[str | None] = mapped_column(Text)


class NotaFiscalItem(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "nota_fiscal_item"

    nota_fiscal_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("nota_fiscal.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    ncm: Mapped[str | None] = mapped_column(String(10))
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    valor_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    insumo_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("insumo.id", ondelete="SET NULL")
    )


class ApropriacaoOrigem(StrEnum):
    nota_fiscal_item = "nota_fiscal_item"
    medicao = "medicao"
    lancamento_manual = "lancamento_manual"
    apontamento_mao_obra = "apontamento_mao_obra"


class ApropriacaoCusto(Base, UUIDPKMixin, TimestampMixin):
    """Apropria valor de um lançamento a uma folha da EAP.

    Pode ter valor negativo (estorno). Não atualiza — corrige por contraposição.
    """

    __tablename__ = "apropriacao_custo"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    origem_tipo: Mapped[ApropriacaoOrigem] = mapped_column(
        SAEnum(ApropriacaoOrigem, name="apropriacao_origem"), nullable=False
    )
    origem_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    quantidade: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    data_competencia: Mapped[date] = mapped_column(Date, nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(500))
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("user_account.id", ondelete="SET NULL")
    )


class MedicaoStatus(StrEnum):
    pendente = "pendente"
    aprovada = "aprovada"
    paga = "paga"


class Medicao(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "medicao"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    contrato_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("contrato.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False
    )
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    data_competencia: Mapped[date] = mapped_column(Date, nullable=False)
    percentual_periodo: Mapped[Decimal] = mapped_column(Numeric(7, 4), nullable=False)
    valor_periodo: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    status: Mapped[MedicaoStatus] = mapped_column(
        SAEnum(MedicaoStatus, name="medicao_status"),
        default=MedicaoStatus.pendente,
        nullable=False,
    )
    eap_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="SET NULL")
    )


class ApontamentoMaoObra(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "apontamento_mao_obra"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False
    )
    data: Mapped[date] = mapped_column(Date, nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("insumo.id", ondelete="RESTRICT"), nullable=False
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    custo_unitario_snapshot: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text)


class LancamentoManual(Base, UUIDPKMixin, TimestampMixin):
    """Custo avulso (taxas, emolumentos, etc) lançado pelo Proprietário."""

    __tablename__ = "lancamento_manual"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False
    )
    data: Mapped[date] = mapped_column(Date, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    fornecedor_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("fornecedor.id", ondelete="SET NULL")
    )
