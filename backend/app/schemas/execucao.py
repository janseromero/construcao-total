"""Schemas: NF, Apropriação, Apontamento, Lançamento manual."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.execucao import ApropriacaoOrigem, NotaFiscalStatus
from app.schemas.common import ORMModel


class NotaFiscalItemIn(BaseModel):
    descricao: str
    ncm: str | None = None
    unidade: str
    quantidade: Decimal
    valor_unitario: Decimal
    valor_total: Decimal
    insumo_id: UUID | None = None


class NotaFiscalItemOut(ORMModel):
    id: UUID
    nota_fiscal_id: UUID
    descricao: str
    ncm: str | None
    unidade: str
    quantidade: Decimal
    valor_unitario: Decimal
    valor_total: Decimal
    insumo_id: UUID | None


class NotaFiscalIn(BaseModel):
    obra_id: UUID | None = None
    fornecedor_id: UUID
    numero: str
    serie: str | None = None
    chave_acesso: str | None = None
    data_emissao: date
    valor_total: Decimal
    valor_produtos: Decimal = Decimal("0")
    valor_servicos: Decimal = Decimal("0")
    valor_impostos: Decimal = Decimal("0")
    itens: list[NotaFiscalItemIn] = []


class NotaFiscalOut(ORMModel):
    id: UUID
    obra_id: UUID | None
    fornecedor_id: UUID
    numero: str
    serie: str | None
    chave_acesso: str | None
    data_emissao: date
    valor_total: Decimal
    valor_produtos: Decimal
    valor_servicos: Decimal
    valor_impostos: Decimal
    status: NotaFiscalStatus
    itens: list[NotaFiscalItemOut] = []


class ApropriacaoIn(BaseModel):
    obra_id: UUID
    eap_id: UUID
    origem_tipo: ApropriacaoOrigem
    origem_id: UUID
    valor: Decimal
    quantidade: Decimal | None = None
    data_competencia: date
    descricao: str | None = None


class ApropriacaoOut(ORMModel):
    id: UUID
    obra_id: UUID
    eap_id: UUID
    origem_tipo: ApropriacaoOrigem
    origem_id: UUID
    valor: Decimal
    quantidade: Decimal | None
    data_competencia: date
    descricao: str | None


class ApontamentoIn(BaseModel):
    obra_id: UUID
    eap_id: UUID
    data: date
    insumo_id: UUID
    quantidade: Decimal
    observacao: str | None = None


class ApontamentoOut(ORMModel):
    id: UUID
    obra_id: UUID
    eap_id: UUID
    data: date
    insumo_id: UUID
    quantidade: Decimal
    valor_total: Decimal | None  # ocultado para Operacional


class LancamentoManualIn(BaseModel):
    obra_id: UUID
    eap_id: UUID
    data: date
    valor: Decimal
    descricao: str
    fornecedor_id: UUID | None = None


class LancamentoManualOut(ORMModel):
    id: UUID
    obra_id: UUID
    eap_id: UUID
    data: date
    valor: Decimal
    descricao: str
    fornecedor_id: UUID | None
