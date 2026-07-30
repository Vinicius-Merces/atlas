# Claude Code Runtime

This directory contains the Claude Code implementation of ATLAS.

## Structure

- `agents/`: specialist and orchestration definitions
- `contracts/`: required interfaces and responsibilities
- `memory/`: stable project knowledge
- `rules/`: mandatory execution constraints
- `workflows/`: repeatable delivery processes
- `architecture/`: runtime-specific architecture guidance

Project-specific context should be added to memory rather than embedded into
global agent instructions.
