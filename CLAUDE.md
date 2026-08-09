# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure
- `Ejercicios de Authentication/`: Simple scripts related to authentication logic.
- `ORMs/`: Focuses on data modeling using Object-Relational Mapping.
- `postgresPython/`: A structured project implementing a Repository pattern for PostgreSQL interactions.
  - `db.py`: Database configuration and connection management.
  - `repositories.py`: Data access layer implementation.
- `Ejercicio Extra SQL python/`: Collection of utility scripts for database administration (backups, management, seeding).
- `test/`: General test suite or artifacts from testing processes.

## Development Commands
### Common Scripts
- Run a Python script: `python <path_to_file>.py`
- Example: `python postgresPython/main.py`

### Project Specifics
- The repository is structured as a collection of educational modules and practical exercises in Python.
- Different folders represent different learning paths (SQL, ORMs, Authentication).

## Technical Context
- **Language**: Python 3
- **Architecture Patterns**: Repository Pattern (in `postgresPython`), Model/Data Mapping (in `ORMs`).
- **Key technologies**: PostgreSQL, SQLAlchemy (implied by ORM folder).

## Context Navigation (Graphify)

### 3-Layer Query Rule
1. **First:** query `graphify-out/graph.json` or `graphify-out/wiki/index.md` to understand code structure and connections
2. **Second:** query the Obsidian vault for decisions, progress, and project context
3. **Third:** only read raw code files when editing or when the first two layers don't have the answer

### When to rebuild the graph
- After structural changes (new modules, major refactors)
- Headless: `graphify update .` (only processes modified files)
- Skill: `/graphify . --update` (same behavior, runs through the skill — also accepts `--obsidian` to refresh the vault)
- The graph is persistent — NO need to rebuild every session

### Do NOT
- Don't manually modify files inside `graphify-out/`
- Don't re-read the entire codebase if the graph already has the information
