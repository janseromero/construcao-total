"""Schemas: Comprador + Venda."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.venda import VendaStatus
from app.schemas.common import ORMModel


class CompradorIn(BaseModel):
    nome: str
    cpf_cnpj: str | None = None
    contato: str | None = None
    email: str | None = None


class CompradorOut(ORMModel):
    id: UUID
    nome: str
    cpf_cnpj: str | None
    contato: str | None
    email: str | None


class VendaIn(BaseModel):
    unidade_id: UUID
    comprador_id: UUID | None = None
    preco_tabela: Decimal
    preco_venda_final: Decimal | None = None
    data_venda: date | None = None
    status: VendaStatus = VendaStatus.disponivel
    observacoes: str | None = None


class VendaOut(ORMModel):
    id: UUID
    unidade_id: UUID
    comprador_id: UUID | None
    preco_tabela: Decimal
    preco_venda_final: Decimal | None
    data_venda: date | None
    status: VendaStatus
    observacoes: str | None
