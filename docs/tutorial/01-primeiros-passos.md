# 1. Primeiros passos

Vamos criar sua conta, entender os perfis e fazer um tour rápido pela interface.

---

## 1.1. Criar conta

1. Acesse a página inicial e clique em **Criar conta**.
2. Preencha:
   - **Nome da construtora** — ex.: `Construtora Aurora Engenharia Ltda`.
   - **CNPJ** — apenas números ou com pontuação, tanto faz. O sistema normaliza.
   - **Seu nome** — quem está criando a conta vira o **Proprietário** da construtora.
   - **E-mail** — será seu login.
   - **Senha** — mínimo 8 caracteres.
3. Clique em **Criar conta**.

Você é redirecionado direto para o painel autenticado. O sistema cria:
- Um **tenant** (sua construtora) — todos os dados que você lançar ficam isolados dentro dele.
- Um **usuário Proprietário** — você.

💡 Cada construtora é um tenant separado. Se você tiver duas empresas (uma para incorporação, outra para construção), faça duas contas com CNPJs diferentes.

---

## 1.2. Entrar (login)

Já tem conta? Clique em **Entrar** na página inicial.

1. Digite e-mail e senha.
2. Clique em **Entrar**.

A sessão dura **8 horas** por padrão. Depois disso, você precisa fazer login de novo.

---

## 1.3. Tour pela interface

Depois de logado, a tela é dividida em três áreas:

### Sidebar (lateral esquerda, fundo escuro)

Menu principal:
- **Dashboard** — visão geral das obras.
- **Obras** — lista completa.
- **Fornecedores** — catálogo do tenant.
- **Insumos** — materiais, mão de obra e equipamentos do tenant.

No rodapé da sidebar você vê seu nome, o nome da construtora e um badge amarelo com seu perfil (**Proprietário** ou **Operacional**).

O botão **Sair** está no rodapé da sidebar.

### Área principal

Mostra o conteúdo da página atual. Sempre que entrar em uma obra, aparecem **7 abas** no topo:

1. **Visão geral** — stats + resumo financeiro.
2. **Unidades** — apartamentos da obra.
3. **EAP** — árvore de etapas/serviços.
4. **Orçamento** — versionado.
5. **Execução** — NF, apropriação, apontamentos.
6. **Análise** — custo por unidade, margem, orçado × realizado.
7. **Vendas** — apenas para Proprietário.

### Cabeçalho da obra

Quando você está dentro de uma obra, o cabeçalho mostra:
- Nome da obra.
- UF (estado).
- Status (planejamento, em obra, concluída, pausada).
- Badge **Em afetação** se for o caso (gancho para Patrimônio de Afetação — fora do MVP).

---

## 1.4. Convidar um usuário Operacional

⚠️ No MVP, o convite é manual via banco. O fluxo de convite por e-mail entra na Onda 2. Para criar um Operacional manualmente, peça ajuda à equipe técnica ou crie via API:

```bash
# Via API (apenas para administradores técnicos)
POST /auth/login  # logar como Proprietário, pegar token
# Depois inserir usuário direto no banco com role = "operacional"
```

Quando o convite por UI estiver pronto, o fluxo será:
1. Em **Configurações → Usuários**, clicar em **Convidar**.
2. Informar nome e e-mail do convidado e o perfil.
3. O convidado recebe um link, define a senha e entra direto.

---

## 1.5. O que o perfil Operacional vê (e o que não vê)

| Pode | Não pode |
|------|----------|
| Cadastrar fornecedores, insumos e composições | Ver preço de venda das unidades |
| Cadastrar e editar EAP | Ver margem por unidade |
| Lançar NF, apropriações e apontamentos de mão de obra | Ver resumo executivo (VGV, margem total) |
| Ver orçado × realizado por etapa | Aprovar orçamento |
| Ver relatório de custo por unidade | Lançar custos manuais avulsos |

⚠️ No relatório de **Apontamentos**, o Operacional vê quantidades (horas, dias) mas **não vê o valor em reais** que aquele apontamento gerou. Isso é proposital.

---

## 1.6. Sair com segurança

Sempre que terminar de usar o sistema em um computador compartilhado, clique em **Sair** no rodapé da sidebar. Isso invalida sua sessão no navegador.

---

## Erros comuns nesta etapa

| Sintoma | Causa provável | Solução |
|---------|---------------|---------|
| "CNPJ já cadastrado" no signup | Outro usuário já criou conta com esse CNPJ | Faça login com a conta existente ou use outro CNPJ |
| "E-mail já cadastrado" no signup | E-mail já está em uso | Use outro e-mail ou recupere senha |
| Login retorna "Credenciais inválidas" | Senha errada ou e-mail digitado errado | Tente de novo; lembre que e-mail diferencia maiúsculas/minúsculas |
| Tela em branco após login | Token expirou | Faça login de novo |
| Sidebar não aparece | Você não está logado | O sistema redireciona para login automaticamente |

---

**Próximo passo:** [Capítulo 2 — Obras e unidades](02-obras-e-unidades.md).
