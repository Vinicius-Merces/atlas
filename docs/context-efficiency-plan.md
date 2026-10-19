# Plano de eficiência de contexto

Data: 16/10/2026. Escopo: ATLAS, mantendo fontes canônicas, arquivos portáteis,
adapters compartilhados e resultados verificáveis.

## Etapa 1: orçamento e validade (implementada; validação e integração nesta sessão)

- Limite global verificável do pacote completo em caracteres, incluindo metadados.
  Caracteres não são tokens; não anunciar economia de tokens a partir dessa medida.
- Fontes obrigatórias preservadas; falhar quando o orçamento não comportar o núcleo.
- Registrar fontes adiadas e trechos truncados, sem apresentá-los como leitura completa.
- Conteúdo estável antes dos dados variáveis da tarefa, com hash próprio.
- Conferir integridade do pacote e hashes das fontes antes de gerar plano executável.
- Contexto legado sem manifesto exige opção explícita e indicação de não verificado.
- Aceite: testes de orçamento, alteração/remoção de fonte, adulteração do pacote,
  isolamento de caminhos e estabilidade do prefixo; validação full e CI aprovadas.

## Etapa 2: seleção mais precisa

Implementação entregue no incremento de 19/10: seleção lexical por seções Markdown
e símbolos Python AST, intervalos/linhas no manifesto e verificação de trechos.
Arquivos obrigatórios continuam integrais. Testes com informação além do prefixo
cobrem recuperação sintética; qualidade em projetos reais permanece por medir.

Substituir recortes iniciais por seleção de seções/símbolos relevantes. Acrescentar
mapa compacto de código e prioridades de leitura sob demanda. Preservar restrições,
interfaces e decisões completas; medir recuperação de informação em tarefas reais.
Aceite: localizar informação relevante fora do início do arquivo e manter a qualidade
em tarefas comparáveis, sem ampliar o orçamento global.

## Etapa 3: reuso incremental

Implementação entregue no mesmo incremento: cache descartável de intervalos,
isolado por raiz/identidade de projeto, conteúdo, consulta, orçamento, modo e versão
do extrator. Testes cobrem frio/quente, adulteração, symlinks e invalidação.
Não contém respostas nem ferramentas mutáveis; não comprova cache do provedor.

Reaproveitar extrações locais por hash de conteúdo, versão do extrator e parâmetros.
Invalidar dependências alteradas. Cache local é derivado, descartável e separado da
memória canônica. Evitar cache semântico de decisões ou respostas de ferramentas
mutáveis sem contrato explícito de validade.
Aceite: cache frio/quente equivalente, invalidação e isolamento entre projetos.

## Etapa 4: adapters e medição

Documentar capacidades de cache/compactação por runtime; usar métricas reais do
provedor quando disponíveis. ATLAS não controla o cache interno de um aplicativo
hospedado. Comparar tarefa, modelo e critérios iguais: entrada total, tokens em cache,
latência, custo observado, aceite e retrabalho. Não prometer economia percentual antes
de medir. Testar retomada após compactação preservando decisões e pendências.

## Referências primárias consultadas

- https://aider.chat/docs/repomap.html
- https://aider.chat/docs/usage/caching.html
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://hub.openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents
- https://agentskills.io/specification

Adotar conceitos com implementação própria; nenhuma dependência ou código externo
copiado. Popularidade é sinal de descoberta, não prova de qualidade.
