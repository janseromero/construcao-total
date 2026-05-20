"""ORM models — all entities for Onda 1.

Domain reference: docs/architecture/domain-model.md
"""

from app.models.audit import AuditLog
from app.models.catalogo import Composicao, ComposicaoInsumo, Fornecedor, Insumo
from app.models.execucao import (
    ApontamentoMaoObra,
    ApropriacaoCusto,
    LancamentoManual,
    Medicao,
    NotaFiscal,
    NotaFiscalItem,
)
from app.models.obra import EAP, Contrato, CronogramaEtapa, Obra, Tipologia, Unidade
from app.models.orcamento import Orcamento, OrcamentoItem
from app.models.rateio import RateioCalculado, RegraRateio, RegraRateioPesoUnidade
from app.models.tenant import Tenant
from app.models.user import User
from app.models.venda import Comprador, Venda

__all__ = [
    "AuditLog",
    "Tenant",
    "User",
    "Fornecedor",
    "Insumo",
    "Composicao",
    "ComposicaoInsumo",
    "Obra",
    "Tipologia",
    "Unidade",
    "EAP",
    "CronogramaEtapa",
    "Contrato",
    "Orcamento",
    "OrcamentoItem",
    "NotaFiscal",
    "NotaFiscalItem",
    "ApropriacaoCusto",
    "Medicao",
    "ApontamentoMaoObra",
    "LancamentoManual",
    "RegraRateio",
    "RegraRateioPesoUnidade",
    "RateioCalculado",
    "Comprador",
    "Venda",
]
