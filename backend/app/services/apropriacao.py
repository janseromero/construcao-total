"""Regras de apropriação: validações antes de criar registros."""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.execucao import (
    ApropriacaoCusto,
    ApropriacaoOrigem,
    NotaFiscal,
    NotaFiscalItem,
    NotaFiscalStatus,
)


def valor_ja_apropriado(db: Session, *, origem_tipo: ApropriacaoOrigem, origem_id: UUID) -> Decimal:
    total = db.scalar(
        select(func.coalesce(func.sum(ApropriacaoCusto.valor), 0)).where(
            ApropriacaoCusto.origem_tipo == origem_tipo,
            ApropriacaoCusto.origem_id == origem_id,
        )
    )
    return Decimal(str(total or 0))


def validar_apropriacao_nf_item(
    db: Session, *, nf_item_id: UUID, novo_valor: Decimal
) -> None:
    item = db.get(NotaFiscalItem, nf_item_id)
    if item is None:
        raise ValueError("Item de NF não encontrado")
    ja = valor_ja_apropriado(db, origem_tipo=ApropriacaoOrigem.nota_fiscal_item, origem_id=nf_item_id)
    if (ja + novo_valor) > item.valor_total + Decimal("0.0001"):
        raise ValueError(
            f"Apropriação excede valor do item NF "
            f"(já apropriado R$ {ja}, novo R$ {novo_valor}, item R$ {item.valor_total})"
        )


def atualizar_status_nf(db: Session, nf_id: UUID) -> None:
    nf = db.get(NotaFiscal, nf_id)
    if nf is None:
        return
    itens = list(db.scalars(select(NotaFiscalItem).where(NotaFiscalItem.nota_fiscal_id == nf_id)))
    if not itens:
        return
    totalmente_apropriados = 0
    parcialmente = 0
    for item in itens:
        ja = valor_ja_apropriado(
            db, origem_tipo=ApropriacaoOrigem.nota_fiscal_item, origem_id=item.id
        )
        if ja >= item.valor_total - Decimal("0.0001"):
            totalmente_apropriados += 1
        elif ja > 0:
            parcialmente += 1
    if totalmente_apropriados == len(itens):
        nf.status = NotaFiscalStatus.totalmente_apropriada
    elif totalmente_apropriados + parcialmente > 0:
        nf.status = NotaFiscalStatus.parcialmente_apropriada
    else:
        nf.status = NotaFiscalStatus.pendente_apropriacao
