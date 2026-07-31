# ATLAS 0.1.1 — Auditoria, prontidão de produção e guia de operação

## Resumo executivo

O ATLAS 0.1.1 conclui o escopo estável definido pelo briefing de finalização:
um framework de operação de engenharia assistida por IA, versionado no
repositório, portável entre sessões e com Claude Code e Codex compartilhando a
mesma memória, contratos, decisões, workflows e critérios de qualidade.

O resultado é adequado para produção dentro do escopo declarado do framework:

- Claude Code permanece o runtime canônico.
- Codex é um runtime suportado com paridade semântica validada.
- Gemini e Cursor permanecem experimentais.
- Os 394 assets governados atendem integralmente aos seis contratos canônicos;
  a dívida medida caiu de 2.402 violações para zero.
- Os 88 skills possuem formato nativo para Claude Code e wrappers nativos
  sincronizados para Codex.
- Distribuições cumulativa, incremental e recovery são determinísticas,
  verificáveis e compatíveis com aplicação manual.
- Atualizações incrementais detectam customizações locais antes de substituir
  ou apagar arquivos.
- CI e validação local usam o mesmo runner portável.

“Pronto para produção” não significa que arquivos Markdown executam trabalho
sozinhos. Agentes, skills, workflows, reviews e commands são especificações
governadas que um runtime de IA ou uma pessoa interpreta. Scripts, schemas,
políticas, testes, hashes e simuladores são a camada determinística.

## Identificação

| Item | Estado |
|---|---|
| Versão | `0.1.1` |
| Canal | stable, patch compatível com `0.1.x` |
| Branch de hardening | `release/0.1.1-production-hardening` |
| Base auditada | `309be90d5ca9a76daef42ab79fade69a50ac75b5` |
| Base do patch incremental | tag `v0.1.0`, commit `ce18265b0ece839a862240bb1a170e7532c7b7bd` |
| Runtime canônico | Claude Code |
| Runtime suportado | Codex |
| Runtimes experimentais | Gemini e Cursor |
| Ambiente local | Windows, Python 3.14.6 |
| PR, merge, tag e release | registrados na seção “Evidência de publicação” após a publicação |

## Estado encontrado e correções

### Bootstrap e skills dos runtimes

O repositório não possuía `CLAUDE.md`, e os 88 skills estavam em uma estrutura
Markdown legada que não era descoberta nativamente por Claude Code ou Codex.

Correções:

- `CLAUDE.md` raiz importa `@AGENTS.md` e define o bootstrap canônico.
- Skills canônicos migraram para `.claude/skills/<nome>/SKILL.md`, com
  frontmatter `name` e `description`.
- `.agents/skills/<nome>/SKILL.md` fornece wrappers gerados para Codex.
- `sync_native_skills.py --check` e o CI bloqueiam drift.
- O adapter Codex resolve o path real do orchestrator e todos os links
  canônicos.

Essas decisões seguem as superfícies oficiais: Codex carrega instruções
duráveis de
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) e
skills de repositório em `.agents/skills/*/SKILL.md`, conforme
[Build skills](https://learn.chatgpt.com/docs/build-skills.md). Claude Code
carrega `CLAUDE.md` e suporta imports, conforme sua
[documentação de memória](https://code.claude.com/docs/en/memory).

### Contratos

O validador anterior confirmava apenas existência e conteúdo não vazio. Uma
auditoria efetiva encontrou 2.402 requisitos ausentes em 394 assets.

Correções:

- Agentes declaram missão, domínio, autoridade conservadora, escopo, limites,
  inputs, outputs, colaboração, qualidade e comportamento.
- Skills declaram propósito, domínio, gatilhos, inputs, outputs, dependências,
  limitações e validação.
- Workflows declaram trigger, objetivo, inputs, responsáveis, decisões,
  validação, falha, conclusão e o lifecycle completo.
- Reviews declaram escopo, evidência, findings, severidade, ações e outcome.
- Commands declaram argumentos, precondições, workflow, output e falha.
- `validate_contracts.py --mode strict` exige conformidade total.

Autoridade nunca implica autoaprovação, dispensa de review, promoção de release
ou expansão silenciosa de escopo.

### Schemas e CLIs

Schemas que antes aceitavam qualquer tipo passaram a definir propriedades,
tipos, enums, padrões, arrays e campos adicionais permitidos. Os validadores de
task envelope, handoff e execution result usam JSON Schema Draft 2020-12,
`FormatChecker`, paths de erro acionáveis e exit code não zero.

Os comandos de continuidade processam `--help` antes de qualquer escrita.
Validadores de runtime não usam `assert`, portanto continuam bloqueando falhas
sob `python -O`.

### Roteamento, contexto e execução

O roteador evoluiu de quatro rotas genéricas para 33 tipos:

`feature`, `bug`, `security`, `release`, `refactor`, `migration`,
`dependency`, `documentation`, `architecture`, `performance`, `data`, `ai`,
`mobile`, `integration`, `privacy`, `incident`, `infrastructure`, `adoption`,
`audit`, `testing`, `localization`, `analytics`, `design-system`, `cost`,
`continuity`, `parallel`, `policy`, `runtime`, `memory`, `product`,
`compatibility`, `deprecation` e `upgrade`.

O envelope inclui risco, runtime, paths afetados, critérios de aceitação e
restrições. O context builder deriva memória, contratos, agentes, workflow,
skills, reviews, declaração do runtime e fontes explícitas, registra hashes e
fontes ausentes. O planner resolve as capacidades reais e declara
`requires_external_execution: true`.

`build_golden_path.py` gera, em um diretório descartável:

- task envelope;
- context pack e manifest;
- execution plan;
- checkpoint;
- handoff entre runtimes;
- continuation plan;
- execution result;
- evidence record;
- manifest com hashes.

Ele gera e valida artefatos; não finge implementar uma feature.

### Continuidade e fontes canônicas

- ADRs são lidos somente de `framework/adr/`; fallback não mascara fonte
  canônica ausente.
- Project brief não confunde skills, templates ou exemplos com decisões.
- Resume packet não confunde schemas/templates com handoffs reais.
- Matching de paths funciona de forma consistente em Windows e Linux.
- Builders de project brief, session brief e resume packet preservam a
  separação entre memória durável e estado temporário.

### Adoção em projetos existentes

Copiar um pacote cumulativo por cima de um produto existente poderia
sobrescrever `README`, `LICENSE`, `AGENTS`, CI, `.gitignore`, versão e memória.

`plan_project_adoption.py` é read-only e classifica cada path como:

- `copy`;
- `identical`;
- `merge-required`;
- `review-required`.

Colisões retornam exit code `2`. Cópia cumulativa direta é destinada a
repositório vazio ou dedicado.

### Release e deploy manual

- A seleção de payload usa arquivos tracked e untracked não ignorados pelo Git.
- Caches, evidência local, reports, editor state, `dist`, segredos e symlinks
  são excluídos ou bloqueados.
- ZIPs usam ordem, timestamp, permissões e conteúdo textual normalizados.
- Manifest interno protege cada arquivo; checksum e manifest externos protegem
  o ZIP final.
- O patch incremental contém `base_sha256` para cada replace/delete.
- Preflight bloqueia:
  - add sobre target existente;
  - replace/delete ausente;
  - replace/delete modificado localmente;
  - hash ou mapping divergente;
  - path absoluto, traversal, drive Windows, UNC ou escape com backslash;
  - operação, target ou payload duplicado;
  - arquivo extra dentro de `CLAUDE-DIRECTORY`.
- Receipt começa como `pending`; `applied` ou `simulated` exige preflight
  aprovado e validação concreta.

### Evidência

Audit bundles agora registram:

- commit de origem e estado do repositório;
- lista deduplicada de records;
- SHA-256 canônico de cada record;
- hash do índice de records;
- quantidade e algoritmo;
- JSON válido;
- conformidade com schemas reconhecidos para evidence, receipt, checkpoint e
  handoff.

Hash correto com JSON ou receipt inválido não é mais aceito.

## Inventário

| Coleção | Quantidade |
|---|---:|
| Agentes, incluindo orchestrator | 87 |
| Skills canônicos | 88 |
| Wrappers nativos Codex | 88 |
| Workflows | 76 |
| Review gates | 68 |
| Commands | 71 |
| Contratos estáveis | 6 |
| Modelos em `framework/` | 80 |
| Scripts Python | 59 |
| Schemas | 31 |
| Políticas executáveis | 14 |
| Módulos de teste | 45 |
| Templates | 68 |
| Guias em `docs/` | 62 |

## O que o ATLAS pode fazer

### Conhecimento e arquitetura

- preservar memória de negócio, arquitetura, segurança, integrações, operação
  e contradições;
- registrar decisões em ADRs;
- validar fontes canônicas, links, freshness e drift;
- propor reconciliação sem promover hipótese a fato;
- expor navegação Obsidian sem criar uma segunda fonte de verdade;
- mapear repositório, dependências, dívida, roadmap, arquitetura corporativa,
  FinOps, observabilidade e ameaças.

### Planejamento e implementação governada

- decompor requisitos de produto e critérios de aceitação;
- rotear 33 tipos de tarefa para papel, workflow, skill, review e validação;
- classificar risco e acrescentar governance review em alto risco;
- montar contexto limitado, rastreado e revisável;
- produzir um execution plan específico para Claude Code ou Codex;
- orientar feature, bug fix, refactor, migração, dependência, integração, dados,
  IA, mobile, design system, analytics, conteúdo, localização e infraestrutura;
- registrar resultado, findings, assumptions, riscos e knowledge updates.

### Qualidade e governança

- aplicar reviews de arquitetura, segurança, privacidade, UX, QA, performance,
  dados, compatibilidade, documentação, compliance, release e operação;
- validar contratos, schemas, registry, documentação, links, políticas,
  runtime parity e package integrity;
- distinguir aprovado, aprovado com condições, changes required e blocked;
- impedir sucesso quando faltam evidência, autoridade ou gate obrigatório;
- avaliar políticas e exceções com severidade e expiração.

### Continuidade e colaboração

- criar checkpoints;
- transferir tarefas entre Claude Code e Codex;
- produzir continuation plans;
- fechar sessões e gerar resume packets;
- recuperar trabalho sem depender do chat anterior;
- decompor trabalho em workstreams;
- declarar resource claims;
- detectar conflitos de path, bloquear merge e reconciliar resultados.

### Release e operação

- gerenciar versões sem alterar documentos históricos;
- criar pacote cumulativo, incremental e recovery;
- representar `.claude` como `CLAUDE-DIRECTORY` no patch manual;
- listar add, replace e delete explicitamente;
- detectar customização local antes de overwrite/delete;
- simular instalação limpa e upgrade;
- validar checksum, manifest, root, contagens e paths;
- registrar preflight, deploy receipt, provenance e audit bundle;
- verificar tamper de artifacts e evidência.

### Adoção e referência

- planejar integração read-only em repositório ocupado;
- apontar merges obrigatórios;
- fornecer blueprints e exemplos como starters;
- operar como framework dedicado ou camada governada dentro de outro projeto.

## Arquitetura operacional

| Plano | Fonte canônica | Responsabilidade |
|---|---|---|
| Conhecimento | `.claude/memory/`, `framework/adr/`, `docs/`, `obsidian/` | fatos duráveis, decisões e navegação |
| Capacidades | `.claude/skills/`, `schemas/`, `templates/`, `framework/` | expertise, formatos e modelos |
| Execução | `.claude/agents/`, `.claude/workflows/`, `.claude/commands/`, `.atlas/` | responsabilidade, sequência e estado |
| Governança | `.claude/contracts/`, `.claude/reviews/`, `policies/`, `tests/` | invariantes, gates e assurance |
| Runtime | `CLAUDE.md`, `AGENTS.md`, `adapters/` e `.agents/skills/` | tradução de invocação sem bifurcar conhecimento |
| Distribuição | `release/`, `scripts/build_*`, manifests e checksums | entrega, migração e recovery |

## Fronteira de automação

| ATLAS automatiza | Runtime ou pessoa ainda decide |
|---|---|
| inventário, registry e maps | qual contexto é realmente relevante |
| rota inicial e risco padrão | correção do fallback e escopo final |
| context pack e hashes | fatos ausentes, contradições e fontes adicionais |
| execution-plan skeleton | estratégia concreta de implementação |
| validação estrutural e determinística | qualidade semântica da solução |
| seleção de reviews | julgamento e resolução dos findings |
| templates de evidência/continuidade | preencher apenas o que realmente ocorreu |
| packages e simulações | autorização para deploy e merge de customizações |

## Como trabalhar com o framework

### Preparação

```bash
python -m pip install --requirement requirements-test.txt
python scripts/validate_all.py --profile quick
```

Use `quick` durante iteração, `full` para concluir trabalho no framework e
`release` somente para preparação de distribuição.

### Claude Code

Inicie na raiz. O runtime lê `CLAUDE.md`, que importa `AGENTS.md`. Faça um
pedido com outcome, critérios e limites, por exemplo:

```text
/atlas-plan Adicionar exportação CSV ao dashboard, sem alterar o contrato
público atual; incluir testes, documentação e rollback.
```

Depois use o command/workflow apropriado e exija execution evidence.

### Codex

Inicie na raiz e peça:

```text
Leia AGENTS.md, o resume packet quando existir e a memória relevante.
Valide o estado real, siga adapters/codex/commands/atlas-plan.md e planeje:
adicionar exportação CSV ao dashboard sem quebrar o contrato público.
```

Para implementação, review e release use os entry points
`atlas-implement.md`, `atlas-review.md` e `atlas-release.md`.

### Ciclo explícito por CLI

```bash
python scripts/atlas_route.py \
  --task-type feature \
  --runtime codex \
  --summary "Adicionar exportação CSV" \
  --path src/export \
  --acceptance "CSV válido e testes verdes" \
  --output .atlas/tasks/export.task.json

python scripts/validate_task_envelope.py .atlas/tasks/export.task.json

python scripts/build_context_pack.py \
  --task-envelope .atlas/tasks/export.task.json \
  --output .atlas/tasks/export.context.md

python scripts/build_execution_plan.py \
  --task-envelope .atlas/tasks/export.task.json \
  --runtime codex \
  --output .atlas/tasks/export.plan.json
```

Revise os artefatos, execute o workflow real, rode os testes do produto e
registre o resultado:

```bash
python scripts/record_execution_result.py \
  --task-envelope .atlas/tasks/export.task.json \
  --runtime codex \
  --status completed \
  --summary "Exportação implementada e validada" \
  --changed-file src/export/service.py \
  --validation "pytest: passed" \
  --review "qa-review: approved"
```

### Golden path descartável

```bash
python scripts/build_golden_path.py \
  --output-dir .atlas/examples/golden-path \
  --runtime codex
```

Use para aprender o formato ou testar o lifecycle, não como prova de uma
implementação de produto.

### Pausa e retomada

```bash
python scripts/create_checkpoint.py \
  --task-envelope .atlas/tasks/export.task.json \
  --runtime codex \
  --output .atlas/tasks/export.checkpoint.json

python scripts/create_session_brief.py \
  --summary "Exportação implementada; falta review" \
  --runtime codex \
  --next-action "Executar QA review e concluir"

python scripts/build_resume_packet.py
```

Preencha placeholders com evidência real antes de versionar.

### Adoção em repositório existente

```bash
python scripts/plan_project_adoption.py \
  --target-root C:\caminho\do\projeto \
  --output adoption-plan.json \
  --markdown-output adoption-plan.md
```

Não faça bulk overwrite. Resolva cada `merge-required` e `review-required`.

### Release

```bash
python scripts/validate_all.py \
  --profile release \
  --incremental-base v0.1.0

python scripts/build_release.py --kind cumulative
python scripts/build_incremental_release.py --base v0.1.0
python scripts/build_release.py --kind recovery
```

Antes de aplicar o incremental:

```bash
python scripts/manual_deploy_preflight.py \
  --installed-root <atlas-0.1.0> \
  --patch-root <patch-extraido>
```

Qualquer conflito exige merge explícito. Nunca remova path que não apareça em
`FILES-TO-DELETE.md`.

## Evidência de validação local

Esta seção é atualizada após a reprodução final do source commit:

| Gate | Resultado |
|---|---|
| Version, registry, package e contratos | pendente da rodada final |
| Contratos estritos | 394 assets, 0 violações |
| Native skills | 88 Claude + 88 Codex, sem drift |
| Schemas | 31 registrados; total final pendente |
| Políticas | 14 registradas; total final pendente |
| Full pytest | total final pendente |
| Perfil full | total final pendente |
| Perfil release | total final pendente |
| Instalação, upgrade e recovery | pendente da rodada final 0.1.1 |
| Reprodutibilidade e hashes | pendente da rodada final 0.1.1 |

## Evidência de publicação

PR, checks hospedados, merge commit, tag `v0.1.1`, release e hashes dos assets
serão registrados aqui após confirmação direta no GitHub. Até lá, nenhuma
validação local é tratada como CI hospedado.

## Limitações explícitas

- Agentes, skills, workflows, reviews e commands precisam ser interpretados
  por um runtime ou pessoa; presença no disco não prova execução.
- A suíte não lança um processo real de Claude Code ou Codex; ela valida
  bootstrap, estrutura, mapas, schemas, lifecycle e paridade semântica.
- Gemini e Cursor são experimentais.
- Audit bundles usam SHA-256 e provenance, mas não assinatura criptográfica.
- CI principal prioriza Ubuntu/Python 3.12; compatibilidade Windows é exercida
  localmente e por testes de path, mas não por uma matrix hospedada.
- Cumulative/recovery são seguros para repositório vazio, dedicado ou
  recuperação controlada; use o adoption planner em produto existente.
- Blueprints são starters arquiteturais, não aplicações prontas.
- Não há SLA de suporte.

Essas limitações são fronteiras declaradas, não critérios de aceitação
ocultamente pendentes.

## Melhorias futuras opcionais

Sem bloquear 0.1.1:

- CI hospedada também em Windows e versões adicionais de Python;
- coverage, lint, type checking, dependency scanning e SBOM;
- teste de aceitação que inicializa runtimes reais quando suas CLIs estiverem
  disponíveis no ambiente;
- assinatura/atestado dos audit bundles e artifacts;
- empacotamento do framework como plugin instalável;
- âncora externa de evidência em serviço de transparência.

## Veredito

O planejamento está implementado dentro da arquitetura aprovada: repositório
como memória portável, Claude Code canônico, Codex suportado, conhecimento
compartilhado, adapters sem fork, contratos e reviews protegendo significado,
evidência protegendo confiança e pacotes incrementais protegendo o deploy
manual.

O release só é considerado publicado quando a seção de evidência remota estiver
preenchida com checks verdes, merge, tag, release e hashes verificados.
