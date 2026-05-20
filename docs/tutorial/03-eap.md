# 3. EAP — Estrutura Analítica do Projeto

A EAP é a **espinha dorsal** do sistema. Ela define em que etapa/serviço cada centavo gasto na obra será classificado. Sem EAP montada, você não consegue lançar orçamento, nem apropriar nota fiscal, nem ver custo por etapa.

---

## 3.1. O que é EAP

EAP significa **Estrutura Analítica do Projeto**. É uma **árvore hierárquica** que decompõe a obra em etapas e sub-etapas, do mais geral ao mais específico.

Exemplo simplificado:

```
1   Serviços Preliminares
1.1   Tapume
1.2   Limpeza do terreno
2   Fundação
2.1   Escavação
2.2   Concreto
2.3   Armação
3   Estrutura
3.1   Pilares
3.2   Vigas
3.3   Lajes
4   Alvenaria
5   Instalações
5.1   Hidráulica
5.2   Elétrica
6   Acabamentos
6.1   Revestimento
6.2   Pintura
7   Limpeza final
```

Cada **folha** da árvore (nó que não tem filhos) é onde se apropriam custos. Os nós intermediários consolidam os totais.

---

## 3.2. Por que a EAP importa tanto

A EAP é usada para:

1. **Orçamento** — cada item do orçamento é vinculado a uma folha da EAP.
2. **Apropriação** — cada NF, medição, apontamento ou lançamento manual é classificado em uma folha da EAP.
3. **Comparativo orçado × realizado** — calculado por etapa raiz, rolando os totais das folhas.
4. **Regras de rateio** — você pode aplicar critérios diferentes para etapas diferentes (ex.: cobertura rateia só entre apartamentos do último andar).

⚠️ Tudo no sistema gira em torno da EAP. **Monte com calma** — vale a pena no início da obra.

---

## 3.3. Criar a EAP

1. Entre na obra → aba **EAP**.
2. Clique em **Nova etapa**.
3. Preencha:
   - **Etapa pai** — deixe `— Raiz —` para criar uma etapa de primeiro nível. Para criar uma sub-etapa, escolha o pai.
   - **Código** — sugerimos seguir a numeração padrão (`1`, `1.1`, `1.1.1`...).
   - **Nome** — ex.: `Fundação`, `Estrutura`, `Concreto`.
   - **Ordem** — opcional, para forçar ordenação quando a numeração não basta.
4. Clique em **Salvar**.

A árvore aparece na tela com indentação por nível.

💡 **Dica de ouro:** crie primeiro todas as raízes (1, 2, 3, ...) e depois desça nível por nível. É mais rápido que criar a raiz, depois seus filhos, depois voltar pra próxima raiz.

---

## 3.4. Modelo de EAP recomendado para edifícios residenciais

Use este template como ponto de partida. Adapte ao seu projeto.

```
1   Serviços Preliminares
1.1   Tapume e canteiro
1.2   Limpeza e demolição
1.3   Locação da obra
1.4   Sondagem

2   Fundação
2.1   Escavação
2.2   Forma
2.3   Armação
2.4   Concreto
2.5   Impermeabilização

3   Estrutura
3.1   Pilares
3.2   Vigas
3.3   Lajes
3.4   Escadas

4   Alvenaria e vedação
4.1   Alvenaria estrutural
4.2   Vedação interna
4.3   Vedação externa

5   Cobertura
5.1   Estrutura do telhado
5.2   Telhas
5.3   Calhas e rufos

6   Instalações
6.1   Hidráulica
6.2   Elétrica
6.3   Gás
6.4   Telefonia e dados
6.5   Para-raios

7   Esquadrias
7.1   Portas
7.2   Janelas

8   Revestimentos
8.1   Reboco interno
8.2   Reboco externo
8.3   Azulejos
8.4   Pisos cerâmicos
8.5   Pisos especiais
8.6   Rodapés

9   Pintura
9.1   Massa corrida
9.2   Pintura interna
9.3   Pintura externa

10   Áreas externas
10.1   Calçada
10.2   Muro
10.3   Portão
10.4   Paisagismo

11   Limpeza final

12   Custos indiretos
12.1   Engenharia e administração
12.2   Taxas, licenças e emolumentos
12.3   Seguro
12.4   Manutenção do canteiro
```

⚠️ **Custos indiretos (12) são importantes.** Não esqueça de classificar nele: ART do engenheiro, alvarás, ISS, IPTU da obra, vigia, taxa do contador, etc. Sem isso, sua margem por unidade vai ficar artificialmente alta.

---

## 3.5. Quão fundo devo descer?

**Regra prática:** desça até o nível onde você consegue lançar custos sem hesitar.

- **Bom:** `3.3 Lajes` — uma NF de concreto da laje é apropriada aqui.
- **Bom:** `8.4 Pisos cerâmicos` — todos os materiais e mão de obra de piso ficam aqui.
- **Exagero:** `3.3.1 Lajes do 1º pavimento`, `3.3.2 Lajes do 2º pavimento`... — desnecessário, vai te deixar perdido na hora de classificar a NF.

Em geral, **2–3 níveis** dão conta para construtora pequena. Grandes construtoras chegam a 5 níveis.

💡 Se ficar em dúvida entre lançar como folha ou criar mais um nível, **fique no nível mais alto**. É melhor ajustar pra cima do que pra baixo depois.

---

## 3.6. Editar e remover etapas

- **Remover** — botão **Remover** ao lado da etapa. Atenção: **remove toda a sub-árvore** (filhos, netos...). Confirme antes.
- **Renomear / mudar código** — não há edição direta no MVP. Remova e crie de novo (cuidado se já houver orçamento ou apropriação ligados).

⚠️ Se já houver **orçamento ou apropriação** vinculados à etapa, **o sistema bloqueia a remoção**. Isso é proposital — manter integridade histórica. Para mover custos, faça lançamentos de estorno.

---

## 3.7. Como a EAP é usada nas próximas telas

| Tela | Onde a EAP aparece |
|------|---------------------|
| Orçamento → itens | Você escolhe a folha da EAP para cada item orçado |
| Execução → apropriação | Modal "Apropriar" pede a folha da EAP |
| Apontamento de mão de obra | Operacional escolhe a folha onde apontar as horas |
| Lançamento manual | Proprietário escolhe a folha do custo avulso |
| Análise → orçado × realizado | Mostra totais por etapa raiz, rolando os totais das folhas |
| Regras de rateio | Você pode aplicar regra específica a uma sub-árvore |

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Não consigo remover uma etapa | Há orçamento ou apropriação vinculados | Estorne os lançamentos antes |
| EAP fica gigante e confusa | Você desceu demais nos níveis | Comece simples; refine depois |
| Esqueci de criar "Custos indiretos" | Comum | Crie agora; sem isso a margem fica errada |
| Nó pai aparece como folha no orçamento | Você criou item de orçamento num nó que depois recebeu filhos | Remova o item antigo e recrie no filho correto |
| Dois nós com mesmo código | Sistema permite, mas evite | Use código único; numeração ajuda a ordenar |

---

**Próximo passo:** [Capítulo 4 — Catálogo](04-catalogo.md), onde você cadastra fornecedores, insumos e composições que vão alimentar o orçamento.
