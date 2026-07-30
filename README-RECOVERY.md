# Recuperação manual da pasta .claude

Este pacote existe porque pastas iniciadas por ponto podem ficar ocultas ou ser
ignoradas em alguns fluxos de extração, seleção e upload manual.

## Aplicação

1. Extraia este ZIP.
2. Localize a pasta visível `CLAUDE-DIRECTORY`.
3. Envie ou copie essa pasta inteira para a raiz do repositório.
4. Renomeie `CLAUDE-DIRECTORY` para `.claude`.
5. Confirme que existe o arquivo `.claude/registry.json`.
6. Confirme que existem as subpastas:
   - `.claude/agents`
   - `.claude/commands`
   - `.claude/contracts`
   - `.claude/memory`
   - `.claude/reviews`
   - `.claude/skills`
   - `.claude/workflows`

Se o GitHub não permitir renomear a pasta diretamente pela interface, faça a
renomeação localmente no VS Code ou no Explorador de Arquivos e depois envie a
pasta já renomeada usando Git.
