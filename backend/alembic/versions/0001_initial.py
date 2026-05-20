"""initial schema — Onda 1

Revision ID: 0001
Revises:
Create Date: 2026-05-20

"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # Tenant
    op.create_table(
        "tenant",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("razao_social", sa.String(200)),
        sa.Column("cnpj", sa.String(20), nullable=False, unique=True),
        sa.Column("plano", sa.String(20), nullable=False, server_default="free"),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    user_role = sa.Enum("proprietario", "operacional", name="user_role")
    user_role.create(op.get_bind())
    op.create_table(
        "user_account",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="operacional"),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
    )

    # Obra
    obra_status = sa.Enum("planejamento", "em_obra", "concluida", "pausada", name="obra_status")
    obra_status.create(op.get_bind())
    op.create_table(
        "obra",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("endereco", sa.String(500)),
        sa.Column("uf", sa.String(2), nullable=False),
        sa.Column("data_inicio_prevista", sa.Date),
        sa.Column("data_fim_prevista", sa.Date),
        sa.Column("data_inicio_real", sa.Date),
        sa.Column("data_fim_real", sa.Date),
        sa.Column("area_total_construida", sa.Numeric(14, 4)),
        sa.Column("area_terreno", sa.Numeric(14, 4)),
        sa.Column("em_afetacao", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("regime_tributario", sa.String(30)),
        sa.Column("status", obra_status, nullable=False, server_default="planejamento"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "tipologia",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("area_privativa_m2", sa.Numeric(14, 4), nullable=False),
        sa.Column("area_comum_proporcional_m2", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("descricao", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "unidade",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("tipologia_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tipologia.id", ondelete="SET NULL")),
        sa.Column("identificador", sa.String(50), nullable=False),
        sa.Column("andar", sa.Integer),
        sa.Column("bloco", sa.String(20)),
        sa.Column("fracao_ideal", sa.Numeric(12, 8), nullable=False, server_default="0"),
        sa.Column("area_privativa_m2", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "eap",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="CASCADE")),
        sa.Column("codigo", sa.String(50), nullable=False),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("nivel", sa.Integer, nullable=False, server_default="1"),
        sa.Column("ordem", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "cronograma_etapa",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="CASCADE"), nullable=False),
        sa.Column("data_inicio_prevista", sa.Date),
        sa.Column("data_fim_prevista", sa.Date),
        sa.Column("peso_financeiro_percentual", sa.Numeric(7, 4), nullable=False, server_default="0"),
        sa.Column("data_inicio_real", sa.Date),
        sa.Column("data_fim_real", sa.Date),
        sa.Column("percentual_concluido", sa.Numeric(7, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Catálogo
    fornecedor_tipo = sa.Enum("material", "servico", "equipamento", "misto", name="fornecedor_tipo")
    fornecedor_tipo.create(op.get_bind())
    op.create_table(
        "fornecedor",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("cnpj_cpf", sa.String(20)),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("tipo", fornecedor_tipo, nullable=False, server_default="material"),
        sa.Column("contato", sa.String(200)),
        sa.Column("observacoes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    insumo_tipo = sa.Enum("material", "mao_obra", "equipamento", name="insumo_tipo")
    insumo_tipo.create(op.get_bind())
    op.create_table(
        "insumo",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("codigo", sa.String(50), nullable=False),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("unidade", sa.String(10), nullable=False),
        sa.Column("tipo", insumo_tipo, nullable=False, server_default="material"),
        sa.Column("sinapi_codigo", sa.String(20)),
        sa.Column("custo_unitario_referencia", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "codigo", name="uq_insumo_codigo"),
    )

    op.create_table(
        "composicao",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("codigo", sa.String(50), nullable=False),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("unidade", sa.String(10), nullable=False),
        sa.Column("sinapi_codigo", sa.String(20)),
        sa.Column("custo_unitario_calculado", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "codigo", name="uq_composicao_codigo"),
    )

    op.create_table(
        "composicao_insumo",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("composicao_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("composicao.id", ondelete="CASCADE"), nullable=False),
        sa.Column("insumo_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("insumo.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("coeficiente", sa.Numeric(18, 6), nullable=False),
        sa.Column("custo_unitario_snapshot", sa.Numeric(18, 4), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    contrato_status = sa.Enum("vigente", "concluido", "rescindido", name="contrato_status")
    contrato_status.create(op.get_bind())
    op.create_table(
        "contrato",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("fornecedor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fornecedor.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("numero", sa.String(50), nullable=False),
        sa.Column("objeto", sa.Text, nullable=False),
        sa.Column("valor_total", sa.Numeric(18, 4), nullable=False),
        sa.Column("data_assinatura", sa.Date),
        sa.Column("data_inicio", sa.Date),
        sa.Column("data_fim_prevista", sa.Date),
        sa.Column("status", contrato_status, nullable=False, server_default="vigente"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Orçamento
    orcamento_status = sa.Enum("rascunho", "aprovado", "superado", name="orcamento_status")
    orcamento_status.create(op.get_bind())
    op.create_table(
        "orcamento",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("versao", sa.Integer, nullable=False),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("status", orcamento_status, nullable=False, server_default="rascunho"),
        sa.Column("data_aprovacao", sa.DateTime(timezone=True)),
        sa.Column("aprovado_por_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_account.id", ondelete="SET NULL")),
        sa.Column("custo_total_calculado", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("obra_id", "versao", name="uq_orcamento_obra_versao"),
    )

    op.create_table(
        "orcamento_item",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("orcamento_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orcamento.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("composicao_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("composicao.id", ondelete="SET NULL")),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("unidade", sa.String(10), nullable=False),
        sa.Column("quantidade", sa.Numeric(18, 6), nullable=False),
        sa.Column("custo_unitario", sa.Numeric(18, 4), nullable=False),
        sa.Column("custo_total", sa.Numeric(18, 4), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Execução
    nf_status = sa.Enum(
        "pendente_apropriacao", "parcialmente_apropriada", "totalmente_apropriada", "cancelada",
        name="nf_status",
    )
    nf_status.create(op.get_bind())
    op.create_table(
        "nota_fiscal",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="SET NULL"), index=True),
        sa.Column("fornecedor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fornecedor.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("numero", sa.String(50), nullable=False),
        sa.Column("serie", sa.String(10)),
        sa.Column("chave_acesso", sa.String(50)),
        sa.Column("data_emissao", sa.Date, nullable=False),
        sa.Column("valor_total", sa.Numeric(18, 4), nullable=False),
        sa.Column("valor_produtos", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("valor_servicos", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("valor_impostos", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("status", nf_status, nullable=False, server_default="pendente_apropriacao"),
        sa.Column("xml_original", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "chave_acesso", name="uq_nf_chave_acesso"),
    )

    op.create_table(
        "nota_fiscal_item",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nota_fiscal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("nota_fiscal.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("ncm", sa.String(10)),
        sa.Column("unidade", sa.String(10), nullable=False),
        sa.Column("quantidade", sa.Numeric(18, 6), nullable=False),
        sa.Column("valor_unitario", sa.Numeric(18, 4), nullable=False),
        sa.Column("valor_total", sa.Numeric(18, 4), nullable=False),
        sa.Column("insumo_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("insumo.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    apropriacao_origem = sa.Enum(
        "nota_fiscal_item", "medicao", "lancamento_manual", "apontamento_mao_obra",
        name="apropriacao_origem",
    )
    apropriacao_origem.create(op.get_bind())
    op.create_table(
        "apropriacao_custo",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("origem_tipo", apropriacao_origem, nullable=False),
        sa.Column("origem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("valor", sa.Numeric(18, 4), nullable=False),
        sa.Column("quantidade", sa.Numeric(18, 6)),
        sa.Column("data_competencia", sa.Date, nullable=False),
        sa.Column("descricao", sa.String(500)),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_account.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    medicao_status = sa.Enum("pendente", "aprovada", "paga", name="medicao_status")
    medicao_status.create(op.get_bind())
    op.create_table(
        "medicao",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("contrato_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contrato.id", ondelete="RESTRICT"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False),
        sa.Column("numero", sa.Integer, nullable=False),
        sa.Column("data_competencia", sa.Date, nullable=False),
        sa.Column("percentual_periodo", sa.Numeric(7, 4), nullable=False),
        sa.Column("valor_periodo", sa.Numeric(18, 4), nullable=False),
        sa.Column("descricao", sa.Text),
        sa.Column("status", medicao_status, nullable=False, server_default="pendente"),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "apontamento_mao_obra",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("data", sa.Date, nullable=False),
        sa.Column("insumo_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("insumo.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantidade", sa.Numeric(18, 4), nullable=False),
        sa.Column("custo_unitario_snapshot", sa.Numeric(18, 4), nullable=False),
        sa.Column("valor_total", sa.Numeric(18, 4), nullable=False),
        sa.Column("observacao", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "lancamento_manual",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("data", sa.Date, nullable=False),
        sa.Column("valor", sa.Numeric(18, 4), nullable=False),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("fornecedor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fornecedor.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Rateio
    rateio_escopo = sa.Enum("obra_inteira", "eap", name="rateio_escopo")
    rateio_escopo.create(op.get_bind())
    rateio_criterio = sa.Enum(
        "fracao_ideal", "area_privativa", "igualitario", "customizado", name="rateio_criterio"
    )
    rateio_criterio.create(op.get_bind())
    op.create_table(
        "regra_rateio",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("escopo_tipo", rateio_escopo, nullable=False),
        sa.Column("escopo_eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="CASCADE")),
        sa.Column("criterio", rateio_criterio, nullable=False),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("vigente_desde", sa.Date),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "regra_rateio_peso_unidade",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("regra_rateio_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("regra_rateio.id", ondelete="CASCADE"), nullable=False),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False),
        sa.Column("peso", sa.Numeric(18, 6), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "rateio_calculado",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("obra_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("obra.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("eap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("eap.id", ondelete="CASCADE")),
        sa.Column("custo_acumulado", sa.Numeric(18, 4), nullable=False),
        sa.Column("calculado_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Vendas
    op.create_table(
        "comprador",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("cpf_cnpj", sa.String(20)),
        sa.Column("contato", sa.String(200)),
        sa.Column("email", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    venda_status = sa.Enum(
        "disponivel", "reservada", "vendida", "distratada", name="venda_status"
    )
    venda_status.create(op.get_bind())
    op.create_table(
        "venda",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("comprador_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("comprador.id", ondelete="SET NULL")),
        sa.Column("preco_tabela", sa.Numeric(18, 4), nullable=False),
        sa.Column("preco_venda_final", sa.Numeric(18, 4)),
        sa.Column("data_venda", sa.Date),
        sa.Column("status", venda_status, nullable=False, server_default="disponivel"),
        sa.Column("observacoes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Audit
    audit_acao = sa.Enum("create", "update", "delete", "approve", "cancel", name="audit_acao")
    audit_acao.create(op.get_bind())
    op.create_table(
        "audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_account.id", ondelete="SET NULL")),
        sa.Column("entidade", sa.String(50), nullable=False, index=True),
        sa.Column("entidade_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("acao", audit_acao, nullable=False),
        sa.Column("payload_antes", postgresql.JSONB),
        sa.Column("payload_depois", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    for tbl in [
        "audit_log",
        "venda",
        "comprador",
        "rateio_calculado",
        "regra_rateio_peso_unidade",
        "regra_rateio",
        "lancamento_manual",
        "apontamento_mao_obra",
        "medicao",
        "apropriacao_custo",
        "nota_fiscal_item",
        "nota_fiscal",
        "orcamento_item",
        "orcamento",
        "contrato",
        "composicao_insumo",
        "composicao",
        "insumo",
        "fornecedor",
        "cronograma_etapa",
        "eap",
        "unidade",
        "tipologia",
        "obra",
        "user_account",
        "tenant",
    ]:
        op.drop_table(tbl)
    for enum_name in [
        "audit_acao",
        "venda_status",
        "rateio_criterio",
        "rateio_escopo",
        "medicao_status",
        "apropriacao_origem",
        "nf_status",
        "orcamento_status",
        "contrato_status",
        "insumo_tipo",
        "fornecedor_tipo",
        "obra_status",
        "user_role",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {enum_name}")
