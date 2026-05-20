"""Obra + estrutura física (tipologia, unidade, EAP, cronograma, contrato)."""

from datetime import date
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class ObraStatus(StrEnum):
    planejamento = "planejamento"
    em_obra = "em_obra"
    concluida = "concluida"
    pausada = "pausada"


class Obra(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "obra"

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco: Mapped[str | None] = mapped_column(String(500))
    uf: Mapped[str] = mapped_column(String(2), nullable=False)
    data_inicio_prevista: Mapped[date | None] = mapped_column(Date)
    data_fim_prevista: Mapped[date | None] = mapped_column(Date)
    data_inicio_real: Mapped[date | None] = mapped_column(Date)
    data_fim_real: Mapped[date | None] = mapped_column(Date)
    area_total_construida: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    area_terreno: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    em_afetacao: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    regime_tributario: Mapped[str | None] = mapped_column(String(30))
    status: Mapped[ObraStatus] = mapped_column(
        SAEnum(ObraStatus, name="obra_status"), default=ObraStatus.planejamento, nullable=False
    )


class Tipologia(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "tipologia"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    area_privativa_m2: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    area_comum_proporcional_m2: Mapped[Decimal] = mapped_column(
        Numeric(14, 4), default=Decimal("0"), nullable=False
    )
    descricao: Mapped[str | None] = mapped_column(Text)


class Unidade(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "unidade"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tipologia_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("tipologia.id", ondelete="SET NULL")
    )
    identificador: Mapped[str] = mapped_column(String(50), nullable=False)
    andar: Mapped[int | None] = mapped_column(Integer)
    bloco: Mapped[str | None] = mapped_column(String(20))
    fracao_ideal: Mapped[Decimal] = mapped_column(Numeric(12, 8), default=Decimal("0"), nullable=False)
    area_privativa_m2: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=Decimal("0"), nullable=False)


class EAP(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "eap"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="CASCADE")
    )
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    nivel: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class CronogramaEtapa(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "cronograma_etapa"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eap_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("eap.id", ondelete="CASCADE"), nullable=False
    )
    data_inicio_prevista: Mapped[date | None] = mapped_column(Date)
    data_fim_prevista: Mapped[date | None] = mapped_column(Date)
    peso_financeiro_percentual: Mapped[Decimal] = mapped_column(
        Numeric(7, 4), default=Decimal("0"), nullable=False
    )
    data_inicio_real: Mapped[date | None] = mapped_column(Date)
    data_fim_real: Mapped[date | None] = mapped_column(Date)
    percentual_concluido: Mapped[Decimal] = mapped_column(
        Numeric(7, 4), default=Decimal("0"), nullable=False
    )


class ContratoStatus(StrEnum):
    vigente = "vigente"
    concluido = "concluido"
    rescindido = "rescindido"


class Contrato(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "contrato"

    obra_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True
    )
    fornecedor_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("fornecedor.id", ondelete="RESTRICT"), nullable=False
    )
    numero: Mapped[str] = mapped_column(String(50), nullable=False)
    objeto: Mapped[str] = mapped_column(Text, nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    data_assinatura: Mapped[date | None] = mapped_column(Date)
    data_inicio: Mapped[date | None] = mapped_column(Date)
    data_fim_prevista: Mapped[date | None] = mapped_column(Date)
    status: Mapped[ContratoStatus] = mapped_column(
        SAEnum(ContratoStatus, name="contrato_status"),
        default=ContratoStatus.vigente,
        nullable=False,
    )
