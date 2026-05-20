# 10. Fluxo completo de uma obra — Residencial Aurora

Este capítulo amarra todo o tutorial. É um passo a passo de **uma obra inteira** no sistema, da criação ao fechamento, na sequência que você vai usar na prática.

Use este capítulo como **roteiro** ao operar uma obra real.

---

## Fase 1 — Preparação (antes da obra começar)

### 1.1. Criar conta da construtora
- [Cap. 1](01-primeiros-passos.md) — `Construtora Aurora Engenharia Ltda`, CNPJ, e-mail e senha.
- Você vira **Proprietário** automaticamente.

### 1.2. Cadastrar fornecedores básicos
- [Cap. 4](04-catalogo.md#41-fornecedores)
- Mínimo: 5 fornecedores frequentes (depósito, concreteira, empreiteiro de pintura, locadora, engenheiro).

### 1.3. Cadastrar insumos principais
- [Cap. 4](04-catalogo.md#42-insumos)
- Mínimo: 15 insumos (cimento, areia, brita, bloco, vergalhão, pedreiro, servente, mestre, engenheiro, eletricista, encanador, betoneira).

### 1.4. Criar a obra
- [Cap. 2](02-obras-e-unidades.md#22-criar-a-obra)
- `Residencial Aurora`, SP, em planejamento, datas previstas, áreas.

### 1.5. Montar a EAP
- [Cap. 3](03-eap.md#34-modelo-de-eap-recomendado-para-edifícios-residenciais)
- Use o template padrão (12 etapas raízes) e adapte ao seu projeto.
- Tempo: 30 minutos.

### 1.6. Cadastrar unidades com fração ideal
- [Cap. 2](02-obras-e-unidades.md#24-unidades--os-apartamentos-individuais)
- 8 unidades do Residencial Aurora, com fração ideal somando 1,0.

### 1.7. Cadastrar regras de rateio específicas (opcional)
- [Cap. 7](07-rateio.md#73-definir-uma-regra-específica-por-eap-via-api-no-mvp)
- Cobertura → custos da etapa "5. Cobertura" só vão para aptos 401 e 402.
- Lazer/paisagismo → igualitário entre todas.

---

## Fase 2 — Orçamento base (antes do primeiro tijolo)

### 2.1. Criar orçamento v1 (rascunho)
- [Cap. 5](05-orcamento.md#53-criar-o-primeiro-orçamento)
- Nome: `Orçamento base`.

### 2.2. Adicionar itens — todas as etapas
- [Cap. 5](05-orcamento.md#54-adicionar-itens)
- Use insumos do catálogo e/ou composições.
- Não esqueça **custos indiretos** (engenharia, alvarás, ART, taxas).
- Inclua uma linha de **contingência** (5–10% do total).

### 2.3. Revisar com o engenheiro/sócio
- Compare custo total com o VGV potencial. Margem mínima aceitável?
- Compare custo por m² com benchmarks (R$ 2.500–4.000/m² para residencial padrão em SP, varia muito).

### 2.4. Aprovar v1
- [Cap. 5](05-orcamento.md#56-aprovar-o-orçamento)
- A partir daqui, todo realizado é comparado com este orçamento.

### 2.5. Tabela inicial de vendas
- [Cap. 9](09-vendas.md#94-registrar-uma-venda)
- Cadastre preços tabela das 8 unidades (status `disponivel`).
- Calcule margem esperada — relatório de **Margem por unidade** mostrará margem projetada.

---

## Fase 3 — Execução (durante a obra)

### 3.1. Dia a dia da equipe de campo (perfil Operacional)
**Diário ou semanal:**
- [Cap. 6](06-execucao.md#63-apontamento-de-mão-de-obra) — apontar horas trabalhadas dos funcionários CLT/diaristas (Pedreiro João, 8h em Alvenaria do apto 201, etc).

### 3.2. Dia a dia do administrativo (perfil Operacional ou Proprietário)
**Quando chega cada NF:**
1. [Cap. 6](06-execucao.md#61-notas-fiscais) — lançar a NF com fornecedor, número, data, valor, itens.
2. [Cap. 6](06-execucao.md#62-apropriação--o-ato-central-do-sistema) — apropriar cada item à EAP correta. Se a NF tem itens variados, faça split.

### 3.3. Custos sem NF (perfil Proprietário)
- [Cap. 6](06-execucao.md#64-lançamento-manual-de-custo)
- Alvarás, ISS, ART, IPTU da obra, multas, taxa do contador.

### 3.4. Acompanhamento semanal (Proprietário)
- Aba **Análise → Orçado × Realizado** — alguma etapa estourando?
- Aba **Análise → Custo por unidade** — evolução de custo por apartamento.

### 3.5. Revisões de orçamento
- Se uma etapa estoura mais de 20%, **considere fazer revisão (v2)**.
- [Cap. 5](05-orcamento.md#57-criar-uma-revisão-v2-v3)
- Lance v2 ajustado, aprove. A v1 vira `superado`.

### 3.6. Vendas durante a obra
- [Cap. 9](09-vendas.md) — atualize status das unidades à medida que reservas viram vendas.
- Cliente desistiu? Registre `distratada`.

---

## Fase 4 — Quando uma fase grande termina

Marcos típicos:

- **Fim da fundação** — primeiro grande momento de checagem.
- **Estrutura concluída** — outro marco.
- **Final de obra civil, antes de acabamentos** — talvez uma revisão de orçamento.

Em cada marco:
1. Recalcule rateio.
2. Compare custo por unidade com o esperado.
3. Compare orçado × realizado.
4. Revise tabela de vendas — preços ainda fazem sentido?
5. Documente lições aprendidas para a próxima obra.

---

## Fase 5 — Fechamento da obra

### 5.1. Última leva de NFs e apontamentos
- Limpe tudo que estiver pendente em `pendente_apropriacao`.

### 5.2. Recalcule rateio
- Aba **Análise** → **Recalcular rateio**.

### 5.3. Revise margem por unidade (Proprietário)
- [Cap. 8](08-analise.md#82-margem-por-unidade)
- Qual apartamento deu mais lucro? Qual deu menos? Por quê?

### 5.4. Status final
- Mude status da obra para `concluida` ([Cap. 2.6](02-obras-e-unidades.md#26-mudar-status-da-obra)).
- Confira que todas as unidades vendidas estão como `vendida` (não esqueça nenhuma reservada).

### 5.5. Exportar relatórios (Onda 2)
- Para arquivo (PDF/Excel) — entra na Onda 2.

### 5.6. Análise pós-obra (fora do sistema)
- Margem realizada × margem esperada — comparativo.
- Custo por m² — comparar com a próxima obra que está orçando.
- Quais fornecedores entregaram bem? Quais não?
- A EAP usada deu conta da granularidade? Ajustar template para próxima obra.

---

## Checklist mensal — versão resumida

Cole isto no seu painel. Sugestão de rotina mensal:

**Segunda feira de cada mês:**
- [ ] Lançar todas as NFs do mês anterior.
- [ ] Apropriar todas (status `pendente_apropriacao` deve estar zerado).
- [ ] Conferir apontamentos de mão de obra completos.
- [ ] Lançar custos indiretos do mês (alvarás, contador, IPTU).
- [ ] Recalcular rateio.
- [ ] Revisar **Análise → Orçado × Realizado** — alguma etapa precisa atenção?
- [ ] Atualizar status de vendas (reservas que viraram venda, distratos).
- [ ] Apresentar resumo executivo aos sócios.

---

## Tempo estimado para uma construtora pequena

| Atividade | Frequência | Tempo |
|-----------|------------|-------|
| Setup inicial (cap. 1–4) | Uma vez por obra | 4–8 horas |
| Orçamento v1 (cap. 5) | Uma vez por obra | 4–10 horas |
| Lançar NF + apropriar | Por NF | 2–4 minutos |
| Apontamento mão de obra | Diário/semanal | 5–10 minutos |
| Lançamento manual | Por custo | 1 minuto |
| Revisão Análise | Semanal | 10 minutos |
| Recalcular rateio | Quando precisar | < 5 segundos |
| Fechamento de obra | Uma vez por obra | 2 horas |

---

## Anti-padrões a evitar

1. **Lançar tudo de uma vez no fim do mês.** Apropriação fica imprecisa, NFs perdidas. **Lance toda semana, ou ao receber.**
2. **Pular custos indiretos.** Margem aparece artificialmente alta. **Inclua sempre alvarás, taxas, ART, engenharia.**
3. **Não cadastrar contingência.** Toda obra tem imprevisto. **Reserve 5–10%.**
4. **Versões de orçamento aos montes.** Mais de 4–5 versões = você não tinha plano. **Replaneja.**
5. **EAP profunda demais.** Lançar fica chato, ninguém usa direito. **Comece raso.**
6. **Esquecer de aprovar orçamento.** Sem aprovado, orçado × realizado vazio. **Aprove cedo, mesmo que aproxime.**
7. **Operacional registrando venda.** Ele não tem nem acesso, mas se tentar usar API: **403**.
8. **Custos lançados em obra errada.** Difícil de remover. **Confira sempre a obra ativa antes de lançar.**

---

## Onde buscar ajuda

| Pergunta | Onde |
|----------|------|
| Como funciona X módulo? | [Tutorial — capítulos 1–9](README.md) |
| O que significa Y termo? | [Glossário](glossario.md) |
| API HTTP | `http://localhost:8000/docs` |
| Bug ou comportamento estranho | Abra issue no GitHub (`janseromero/construcao-total`) |
| Dúvida de negócio (rateio, fração ideal) | Consulte o memorial descritivo da incorporação |

---

**Parabéns!** Você completou o tutorial. Comece sua primeira obra real — sugerimos começar com um empreendimento de menor porte para se acostumar com o fluxo, depois evoluir.

Bem-vindo ao Construtor Total. 🟨
