"""Análise: custo por unidade, margem, orçado x realizado."""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.execucao import ApropriacaoCusto
from app.models.obra import EAP, Unidade
from app.models.orcamento import Orcamento, OrcamentoItem, OrcamentoStatus
from app.models.rateio import RateioCalculado
from app.models.venda import Venda, VendaStatus
from app.schemas.rateio import CustoUnidadeRow, MargemUnidadeRow, OrcadoVsRealizadoRow
from app.services.rateio import calcular_rateio


def custo_por_unidade(db: Session, obra_id: UUID, *, recalcular: bool = True) -> list[CustoUnidadeRow]:
    if recalcular:
        calcular_rateio(db, obra_id)
        db.commit()

    unidades = list(db.scalars(select(Unidade).where(Unidade.obra_id == obra_id)))
    rateios = {
        r.unidade_id: r.custo_acumulado
        for r in db.scalars(
            select(RateioCalculado).where(
                RateioCalculado.obra_id == obra_id, RateioCalculado.eap_id.is_(None)
            )
        )
    }
    rows: list[CustoUnidadeRow] = []
    for u in unidades:
        custo = rateios.get(u.id, Decimal("0"))
        area = u.area_privativa_m2 or Decimal("0")
        custo_m2 = (custo / area) if area > 0 else Decimal("0")
        rows.append(
            CustoUnidadeRow(
                unidade_id=u.id,
                identificador=u.identificador,
                area_privativa_m2=area,
                fracao_ideal=u.fracao_ideal,
                custo_acumulado=custo.quantize(Decimal("0.01")),
                custo_por_m2=custo_m2.quantize(Decimal("0.01")),
            )
        )
    return rows


def margem_por_unidade(db: Session, obra_id: UUID) -> list[MargemUnidadeRow]:
    custos = {r.unidade_id: r.custo_acumulado for r in custo_por_unidade(db, obra_id)}

    # Venda ativa (vendida ou reservada) mais recente por unidade.
    vendas = list(
        db.scalars(
            select(Venda)
            .join(Unidade, Unidade.id == Venda.unidade_id)
            .where(Unidade.obra_id == obra_id)
            .where(Venda.status.in_([VendaStatus.vendida, VendaStatus.reservada]))
        )
    )
    venda_por_unidade: dict[UUID, Venda] = {}
    for v in vendas:
        atual = venda_por_unidade.get(v.unidade_id)
        if atual is None or (v.created_at and atual.created_at and v.created_at > atual.created_at):
            venda_por_unidade[v.unidade_id] = v

    unidades = list(db.scalars(select(Unidade).where(Unidade.obra_id == obra_id)))
    rows: list[MargemUnidadeRow] = []
    for u in unidades:
        venda = venda_por_unidade.get(u.id)
        preco = venda.preco_venda_final or venda.preco_tabela if venda else None
        custo = custos.get(u.id, Decimal("0"))
        margem = (preco - custo) if preco is not None else None
        pct = ((margem / preco) * Decimal("100")) if (margem is not None and preco and preco > 0) else None
        rows.append(
            MargemUnidadeRow(
                unidade_id=u.id,
                identificador=u.identificador,
                custo_acumulado=custo,
                preco_venda=preco,
                margem_valor=margem,
                margem_percentual=(pct.quantize(Decimal("0.01")) if pct is not None else None),
            )
        )
    return rows


def orcado_vs_realizado(db: Session, obra_id: UUID) -> list[OrcadoVsRealizadoRow]:
    eaps = list(db.scalars(select(EAP).where(EAP.obra_id == obra_id)))
    eap_by_id = {e.id: e for e in eaps}
    children: dict[UUID | None, list[EAP]] = {}
    for e in eaps:
        children.setdefault(e.parent_id, []).append(e)

    def descendants(root: UUID) -> list[UUID]:
        out = [root]
        stack = [root]
        while stack:
            current = stack.pop()
            for c in children.get(current, []):
                out.append(c.id)
                stack.append(c.id)
        return out

    # Orçado: pega o orçamento aprovado da obra.
    orcamento = db.scalar(
        select(Orcamento).where(
            Orcamento.obra_id == obra_id, Orcamento.status == OrcamentoStatus.aprovado
        )
    )
    orcado_por_eap: dict[UUID, Decimal] = {}
    if orcamento:
        items = db.scalars(
            select(OrcamentoItem).where(OrcamentoItem.orcamento_id == orcamento.id)
        )
        for it in items:
            orcado_por_eap[it.eap_id] = orcado_por_eap.get(it.eap_id, Decimal("0")) + (
                it.custo_total or Decimal("0")
            )

    # Realizado por EAP folha
    realizado_rows = db.execute(
        select(ApropriacaoCusto.eap_id, func.coalesce(func.sum(ApropriacaoCusto.valor), 0)).where(
            ApropriacaoCusto.obra_id == obra_id
        ).group_by(ApropriacaoCusto.eap_id)
    ).all()
    realizado_por_eap: dict[UUID, Decimal] = {r[0]: Decimal(str(r[1])) for r in realizado_rows}

    rows: list[OrcadoVsRealizadoRow] = []
    # Roll up: para cada EAP raiz (parent_id IS NULL), soma de descendentes
    for root in children.get(None, []):
        desc_ids = descendants(root.id)
        orc = sum((orcado_por_eap.get(d, Decimal("0")) for d in desc_ids), Decimal("0"))
        real = sum((realizado_por_eap.get(d, Decimal("0")) for d in desc_ids), Decimal("0"))
        delta = real - orc
        pct = (real / orc * Decimal("100")) if orc > 0 else None
        rows.append(
            OrcadoVsRealizadoRow(
                eap_id=root.id,
                codigo=root.codigo,
                nome=root.nome,
                orcado=orc.quantize(Decimal("0.01")),
                realizado=real.quantize(Decimal("0.01")),
                delta=delta.quantize(Decimal("0.01")),
                percentual=(pct.quantize(Decimal("0.01")) if pct is not None else None),
            )
        )
    _ = eap_by_id  # mantém referência para debugger
    return rows
