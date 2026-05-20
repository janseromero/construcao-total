# 9. Vendas

O módulo Vendas fecha o ciclo: você registra para quem cada apartamento foi vendido, por quanto e quando. Isso alimenta o relatório de margem e o VGV (Valor Geral de Vendas) da obra.

⚠️ **Apenas o Proprietário** tem acesso a este módulo. Operacional não vê a aba **Vendas** nem em modo leitura.

---

## 9.1. Escopo no MVP

O módulo de vendas é **propositalmente simples**. Cobre:

- Cadastro de **comprador** (cliente final que comprou um apartamento).
- Registro de **venda** ligada a uma unidade.
- Mudança de **status** da unidade (disponível, reservada, vendida, distratada).
- Cálculo automático de **VGV**, **margem por unidade** e **margem total**.

Fora do MVP (entram em ondas futuras):
- Fluxo de proposta → contrato → escritura.
- Comissão de corretor.
- Financiamento (associativo, SFH, repasse).
- Distrato com regras de retenção e devolução.
- Pipeline comercial.

Se você precisa de CRM imobiliário completo, integre o Construtor Total com a ferramenta certa para CRM. O nosso foco é o **custo e a margem**, não a venda em si.

---

## 9.2. Compradores

### Como cadastrar (via UI ou inline na venda)

Na aba **Vendas** da obra, quando você abre o modal de "registrar venda", há um campo de texto livre + botão "Criar" para criar um comprador novo na hora.

Alternativamente, via API:

```bash
POST /compradores
{
  "nome": "João da Silva",
  "cpf_cnpj": "123.456.789-00",
  "contato": "(11) 99999-8888",
  "email": "joao@email.com"
}
```

### Campos

| Campo | Obrigatório | Notas |
|-------|-------------|-------|
| Nome | sim | Nome completo (PF) ou razão social (PJ) |
| CPF/CNPJ | não | Recomendado para conferência |
| Contato | não | Telefone, WhatsApp |
| E-mail | não | |

⚠️ Não armazene dados pessoais sensíveis (RG, comprovantes) no Construtor Total — não é um sistema de KYC.

---

## 9.3. Status da unidade

Cada unidade tem um status derivado da venda mais recente:

| Status | Quando usar |
|--------|-------------|
| **disponível** | Ninguém comprou nem reservou (padrão) |
| **reservada** | Cliente sinalizou, ainda sem contrato definitivo. Aparece como "comprometida" no relatório de margem |
| **vendida** | Venda fechada, contrato assinado |
| **distratada** | Venda anterior foi cancelada — a unidade volta a ficar disponível |

⚠️ No MVP, **mover uma unidade entre status é manual** — você atualiza o registro de venda. Fluxos automáticos (reserva expira em 7 dias se não virou venda) entram em ondas futuras.

---

## 9.4. Registrar uma venda

1. Entre na obra → aba **Vendas**.
2. A tabela mostra todas as unidades com seu status atual.
3. Na linha da unidade, clique em **Registrar venda** (ou **Atualizar** se já houver venda).
4. No modal:
   - **Comprador** — escolha um existente ou crie novo no campo "Novo comprador".
   - **Preço tabela (R$)** — preço de tabela publicado.
   - **Preço final (R$)** — preço efetivo da venda (pode ter desconto).
   - **Data** — data da venda.
   - **Status** — vendida / reservada / disponível / distratada.
   - **Observações** — texto livre (forma de pagamento, financiamento, observações).
5. **Salvar**.

### Exemplo Residencial Aurora

| Apto | Comprador | Preço tabela | Preço final | Data | Status |
|------|-----------|--------------|-------------|------|--------|
| 101 | João da Silva | R$ 460.000 | R$ 450.000 | 2026-05-10 | vendida |
| 102 | (sem comprador ainda) | R$ 460.000 | — | — | disponível |
| 201 | Maria Costa | R$ 470.000 | R$ 470.000 | 2026-06-15 | vendida |
| 202 | Pedro Lima | R$ 470.000 | R$ 470.000 | 2026-07-01 | reservada |
| 301 | (disponível) | R$ 580.000 | — | — | disponível |
| 302 | (disponível) | R$ 580.000 | — | — | disponível |
| 401 | Ana Souza | R$ 720.000 | R$ 695.000 | 2026-08-20 | vendida |
| 402 | (disponível) | R$ 720.000 | — | — | disponível |

---

## 9.5. Como o sistema decide qual venda é "ativa"

Uma unidade pode ter **várias linhas de venda** (vendida, depois distratada, depois vendida de novo). O sistema considera a **venda mais recente com status `vendida` ou `reservada`** como a "venda ativa" para fins de cálculo de margem.

Para distrato: registre uma nova venda com status `distratada` (mantém o histórico) — a unidade volta a ser computada como disponível.

---

## 9.6. Tabela de vendas e VGV

### VGV — Valor Geral de Vendas

A soma do preço final (ou preço tabela quando não há venda) de todas as unidades. É o "potencial total de receita" do empreendimento.

Aparece no **Resumo executivo** (Visão geral).

### VGV vendido vs. VGV potencial

| Métrica | Cálculo |
|---------|---------|
| **VGV vendido** | Soma dos preços finais de unidades com status `vendida` ou `reservada` |
| **VGV potencial** | Soma de preços tabela de todas as unidades |
| **VGV remanescente** | VGV potencial − VGV vendido |

No MVP, o resumo executivo mostra o VGV efetivo (vendido). VGV potencial e remanescente são derivados na próxima onda.

---

## 9.7. Margem realizada vs. margem projetada

O relatório **Margem por unidade** mostra:

- **Margem realizada** — para unidades já vendidas: `preço final − custo acumulado`.
- **Margem projetada** — para unidades não vendidas (e que têm preço tabela): `preço tabela − custo acumulado`.

⚠️ O custo acumulado **vai mudar até a obra terminar**. A margem mostrada é "até agora" — apartamentos ainda em obra terão margem aumentando à medida que apropriações cheguem.

---

## 9.8. Cenários comuns

### Desconto na venda
Cliente fechou no apto 101 com R$ 10.000 de desconto.
- **Preço tabela:** R$ 460.000 (mantenha).
- **Preço final:** R$ 450.000.
- Margem é calculada sobre preço final.

### Reserva → venda
Cliente reservou. Após 30 dias, fechou.
1. Reserva: status `reservada`, preço final em branco ou já com o valor combinado.
2. Conversão: atualize a mesma linha, status `vendida`, preço final preenchido, data atualizada.

### Distrato
Cliente desistiu, retornando sinal.
1. Mantenha o registro de venda original (não delete!).
2. Crie um novo registro: status `distratada`, observação com o motivo.
3. A unidade volta a aparecer como disponível.
4. Próxima venda: novo registro, status `vendida`.

### Permuta (terreno por apartamento)
Não há fluxo dedicado no MVP. Sugestão: registre como `vendida` com observação `"Permuta — terreno avaliado em R$ X"` e o preço final igual ao valor de avaliação.

---

## 9.9. Quem pode mexer

⚠️ **Apenas Proprietário.** Operacional não vê a aba e qualquer chamada à API retorna 403.

Por padrão recomendamos que **só uma pessoa** (o sócio comercial ou o próprio dono) cadastre vendas. Reduz erro e mantém a história limpa.

---

## 9.10. Auditoria

Toda mudança em uma venda fica registrada no audit log do sistema (entidade = "venda"). Isso é importante para construtoras que precisam justificar mudanças de preço/desconto a sócios ou bancos financiadores.

A consulta de audit log via UI entra na Onda 3. No MVP, consulte o banco diretamente.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Não vejo a aba Vendas | Você é Operacional | Peça para o Proprietário |
| Preço tabela = 0 e margem = custo negativo | Esqueceu de preencher preço tabela | Atualize |
| Aparecem duas vendas para a mesma unidade | Você cadastrou duplicado | Sistema permite mas não é ideal — use o mais recente |
| Margem aparece 100% (preço sem custo) | Nenhuma apropriação ainda | Normal no início; aguarde apropriações |
| Status `disponivel` mesmo após cadastrar venda | Esqueceu de mudar para `vendida` | Edite o status |
| Mostrei margem para Operacional sem querer | Não foi possível — sistema bloqueia | Reporte se aconteceu |

---

**Próximo passo:** [Capítulo 10 — Fluxo completo de uma obra](10-fluxo-completo.md), onde tudo se encaixa em uma sequência prática do início ao fim.
