"""Schemas: Obra, Tipologia, Unidade, EAP."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.obra import ObraStatus
from app.schemas.common import ORMModel


class ObraIn(BaseModel):
    nome: str
    endereco: str | None = None
    uf: str = Field(min_length=2, max_length=2)
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    area_total_construida: Decimal | None = None
    area_terreno: Decimal | None = None
    em_afetacao: bool = False
    status: ObraStatus = ObraStatus.planejamento


class ObraOut(ORMModel):
    id: UUID
    nome: str
    endereco: str | None
    uf: str
    data_inicio_prevista: date | None
    data_fim_prevista: date | None
    area_total_construida: Decimal | None
    area_terreno: Decimal | None
    em_afetacao: bool
    status: ObraStatus


class TipologiaIn(BaseModel):
    nome: str
    area_privativa_m2: Decimal
    area_comum_proporcional_m2: Decimal = Decimal("0")
    descricao: str | None = None


class TipologiaOut(ORMModel):
    id: UUID
    obra_id: UUID
    nome: str
    area_privativa_m2: Decimal
    area_comum_proporcional_m2: Decimal
    descricao: str | None


class UnidadeIn(BaseModel):
    tipologia_id: UUID | None = None
    identificador: str
    andar: int | None = None
    bloco: str | None = None
    fracao_ideal: Decimal = Decimal("0")
    area_privativa_m2: Decimal = Decimal("0")


class UnidadeOut(ORMModel):
    id: UUID
    obra_id: UUID
    tipologia_id: UUID | None
    identificador: str
    andar: int | None
    bloco: str | None
    fracao_ideal: Decimal
    area_privativa_m2: Decimal


class EAPIn(BaseModel):
    parent_id: UUID | None = None
    codigo: str
    nome: str
    ordem: int = 0


class EAPOut(ORMModel):
    id: UUID
    obra_id: UUID
    parent_id: UUID | None
    codigo: str
    nome: str
    nivel: int
    ordem: int
