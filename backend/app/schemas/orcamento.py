"""Schemas: Orçamento + Item."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.orcamento import OrcamentoStatus
from app.schemas.common import ORMModel


class OrcamentoIn(BaseModel):
    nome: str


class OrcamentoOut(ORMModel):
    id: UUID
    obra_id: UUID
    versao: int
    nome: str
    status: OrcamentoStatus
    data_aprovacao: datetime | None
    custo_total_calculado: Decimal


class OrcamentoItemIn(BaseModel):
    eap_id: UUID
    composicao_id: UUID | None = None
    descricao: str
    unidade: str
    quantidade: Decimal
    custo_unitario: Decimal


class OrcamentoItemOut(ORMModel):
    id: UUID
    orcamento_id: UUID
    eap_id: UUID
    composicao_id: UUID | None
    descricao: str
    unidade: str
    quantidade: Decimal
    custo_unitario: Decimal
    custo_total: Decimal
