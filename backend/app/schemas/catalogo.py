"""Schemas: Fornecedor, Insumo, Composição."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.catalogo import FornecedorTipo, InsumoTipo
from app.schemas.common import ORMModel


class FornecedorIn(BaseModel):
    cnpj_cpf: str | None = None
    nome: str
    tipo: FornecedorTipo = FornecedorTipo.material
    contato: str | None = None
    observacoes: str | None = None


class FornecedorOut(ORMModel):
    id: UUID
    cnpj_cpf: str | None
    nome: str
    tipo: FornecedorTipo
    contato: str | None
    observacoes: str | None


class InsumoIn(BaseModel):
    codigo: str
    descricao: str
    unidade: str
    tipo: InsumoTipo = InsumoTipo.material
    sinapi_codigo: str | None = None
    custo_unitario_referencia: Decimal = Decimal("0")


class InsumoOut(ORMModel):
    id: UUID
    codigo: str
    descricao: str
    unidade: str
    tipo: InsumoTipo
    sinapi_codigo: str | None
    custo_unitario_referencia: Decimal


class ComposicaoInsumoIn(BaseModel):
    insumo_id: UUID
    coeficiente: Decimal


class ComposicaoInsumoOut(ORMModel):
    id: UUID
    insumo_id: UUID
    coeficiente: Decimal
    custo_unitario_snapshot: Decimal


class ComposicaoIn(BaseModel):
    codigo: str
    descricao: str
    unidade: str
    sinapi_codigo: str | None = None
    insumos: list[ComposicaoInsumoIn] = []


class ComposicaoOut(ORMModel):
    id: UUID
    codigo: str
    descricao: str
    unidade: str
    sinapi_codigo: str | None
    custo_unitario_calculado: Decimal
    insumos: list[ComposicaoInsumoOut] = []
