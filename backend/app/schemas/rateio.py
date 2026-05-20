"""Schemas: Regra de rateio + análise."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.rateio import RateioCriterio, RateioEscopo
from app.schemas.common import ORMModel


class PesoUnidadeIn(BaseModel):
    unidade_id: UUID
    peso: Decimal


class RegraRateioIn(BaseModel):
    escopo_tipo: RateioEscopo
    escopo_eap_id: UUID | None = None
    criterio: RateioCriterio
    pesos: list[PesoUnidadeIn] = []


class RegraRateioOut(ORMModel):
    id: UUID
    obra_id: UUID
    escopo_tipo: RateioEscopo
    escopo_eap_id: UUID | None
    criterio: RateioCriterio
    ativo: bool


class CustoUnidadeRow(BaseModel):
    unidade_id: UUID
    identificador: str
    area_privativa_m2: Decimal
    fracao_ideal: Decimal
    custo_acumulado: Decimal
    custo_por_m2: Decimal


class MargemUnidadeRow(BaseModel):
    unidade_id: UUID
    identificador: str
    custo_acumulado: Decimal
    preco_venda: Decimal | None
    margem_valor: Decimal | None
    margem_percentual: Decimal | None


class OrcadoVsRealizadoRow(BaseModel):
    eap_id: UUID
    codigo: str
    nome: str
    orcado: Decimal
    realizado: Decimal
    delta: Decimal
    percentual: Decimal | None  # realizado/orçado
