"""Serviço de cálculo de rateio de custos por unidade.

Estratégia:
1. Para cada apropriação_custo da obra, encontrar a regra de rateio aplicável:
   - Se existir regra com escopo=EAP cuja eap_id == apropriacao.eap_id (ou ancestral), usa ela.
   - Senão, usa a regra geral da obra (escopo=obra_inteira).
2. Aplica o critério para distribuir o valor entre as unidades:
   - fracao_ideal: peso = unidade.fracao_ideal
   - area_privativa: peso = unidade.area_privativa_m2
   - igualitario: peso = 1 (para toda unidade)
   - customizado: peso = regra_rateio_peso_unidade.peso
3. Normaliza pesos (soma=1) e distribui.
4. Persiste o consolidado em rateio_calculado (uma linha por unidade, eap_id=NULL).
"""

from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.execucao import ApropriacaoCusto
from app.models.obra import EAP, Unidade
from app.models.rateio import (
    RateioCalculado,
    RateioCriterio,
    RateioEscopo,
    RegraRateio,
    RegraRateioPesoUnidade,
)


def _ancestors(eap_by_id: dict[UUID, EAP], eap_id: UUID) -> list[UUID]:
    chain: list[UUID] = [eap_id]
    current = eap_by_id.get(eap_id)
    while current and current.parent_id:
        chain.append(current.parent_id)
        current = eap_by_id.get(current.parent_id)
    return chain


def _pesos_para_regra(
    regra: RegraRateio, unidades: list[Unidade], pesos_custom: dict[UUID, Decimal]
) -> dict[UUID, Decimal]:
    pesos: dict[UUID, Decimal] = {}
    for u in unidades:
        if regra.criterio == RateioCriterio.fracao_ideal:
            pesos[u.id] = u.fracao_ideal or Decimal("0")
        elif regra.criterio == RateioCriterio.area_privativa:
            pesos[u.id] = u.area_privativa_m2 or Decimal("0")
        elif regra.criterio == RateioCriterio.igualitario:
            pesos[u.id] = Decimal("1")
        elif regra.criterio == RateioCriterio.customizado:
            pesos[u.id] = pesos_custom.get(u.id, Decimal("0"))
    return pesos


def calcular_rateio(db: Session, obra_id: UUID) -> list[RateioCalculado]:
    """Recalcula o rateio e persiste em rateio_calculado (substitui o anterior)."""
    unidades = list(db.scalars(select(Unidade).where(Unidade.obra_id == obra_id)))
    if not unidades:
        return []

    eaps = list(db.scalars(select(EAP).where(EAP.obra_id == obra_id)))
    eap_by_id = {e.id: e for e in eaps}

    regras = list(
        db.scalars(
            select(RegraRateio).where(RegraRateio.obra_id == obra_id, RegraRateio.ativo.is_(True))
        )
    )
    regra_obra = next(
        (r for r in regras if r.escopo_tipo == RateioEscopo.obra_inteira), None
    )
    regras_por_eap: dict[UUID, RegraRateio] = {
        r.escopo_eap_id: r
        for r in regras
        if r.escopo_tipo == RateioEscopo.eap and r.escopo_eap_id is not None
    }

    # Carrega pesos customizados de todas as regras de uma vez.
    pesos_custom_por_regra: dict[UUID, dict[UUID, Decimal]] = defaultdict(dict)
    if regras:
        all_pesos = db.scalars(
            select(RegraRateioPesoUnidade).where(
                RegraRateioPesoUnidade.regra_rateio_id.in_([r.id for r in regras])
            )
        )
        for p in all_pesos:
            pesos_custom_por_regra[p.regra_rateio_id][p.unidade_id] = p.peso

    apropriacoes = list(
        db.scalars(select(ApropriacaoCusto).where(ApropriacaoCusto.obra_id == obra_id))
    )

    acumulado: dict[UUID, Decimal] = {u.id: Decimal("0") for u in unidades}

    for ap in apropriacoes:
        # Resolve a regra: procura por ancestral mais próximo, senão usa regra geral.
        regra: RegraRateio | None = None
        for eap_id in _ancestors(eap_by_id, ap.eap_id):
            if eap_id in regras_por_eap:
                regra = regras_por_eap[eap_id]
                break
        if regra is None:
            regra = regra_obra
        if regra is None:
            continue  # sem regra, não rateia

        pesos = _pesos_para_regra(regra, unidades, pesos_custom_por_regra.get(regra.id, {}))
        total = sum(pesos.values(), Decimal("0"))
        if total == 0:
            continue
        for uid, peso in pesos.items():
            quota = ap.valor * (peso / total)
            acumulado[uid] += quota

    # Substitui o cache: apaga consolidados anteriores (eap_id NULL).
    db.query(RateioCalculado).filter(
        RateioCalculado.obra_id == obra_id, RateioCalculado.eap_id.is_(None)
    ).delete()

    now = datetime.now(UTC)
    novos = [
        RateioCalculado(
            obra_id=obra_id,
            unidade_id=uid,
            eap_id=None,
            custo_acumulado=valor.quantize(Decimal("0.0001")),
            calculado_em=now,
        )
        for uid, valor in acumulado.items()
    ]
    db.add_all(novos)
    db.flush()
    return novos
