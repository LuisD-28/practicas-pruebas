# Graph Report - .  (2026-08-09)

## Corpus Check
- Corpus is ~5,856 words - fits in a single context window. You may not need a graph.

## Summary
- 160 nodes · 241 edges · 11 communities (7 shown, 4 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.5)
- Token cost: 52,803 input · 0 output

## Community Hubs (Navigation)
- ORMs Exercise Managers & DB Setup
- Authorization Exercise Data Managers
- Authentication Core (DB + JWT)
- Authorization API Routes
- postgresPython Repository Pattern
- Project Documentation Overview
- SQL Admin Scripts (Backup/Seed)
- Authorization User Manager
- Authorization JWT Manager
- ORM Data Models

## God Nodes (most connected - your core abstractions)
1. `UserManager` - 11 edges
2. `UserManager` - 11 edges
3. `InvoiceManager` - 10 edges
4. `ProductManager` - 10 edges
5. `CarManager` - 10 edges
6. `PgManager` - 9 edges
7. `UserRepository` - 9 edges
8. `AddressManager` - 8 edges
9. `User` - 7 edges
10. `Product` - 7 edges

## Surprising Connections (you probably didn't know these)
- `CarManager` --uses--> `User`  [INFERRED]
  Ejercicios Extra de ORMs/managers/car_manager.py → 4. Ejercicio de Authorization/models.py
- `UserManager` --uses--> `User`  [INFERRED]
  Ejercicios Extra de ORMs/managers/user_manager.py → 4. Ejercicio de Authorization/models.py
- `test_user_manager()` --calls--> `UserManager`  [EXTRACTED]
  4. Ejercicio de Authorization/test_managers.py → 4. Ejercicio de Authorization/managers/user_manager.py
- `InvoiceManager` --uses--> `Invoice`  [INFERRED]
  4. Ejercicio de Authorization/managers/invoice_manager.py → 4. Ejercicio de Authorization/models.py
- `InvoiceManager` --uses--> `InvoiceItem`  [INFERRED]
  4. Ejercicio de Authorization/managers/invoice_manager.py → 4. Ejercicio de Authorization/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **postgresPython Repository Pattern Implementation** — claude_postgrespython, claude_db_py, claude_repositories_py, claude_repository_pattern [EXTRACTED 1.00]
- **Educational Learning Paths (SQL, ORMs, Authentication)** — claude_ejercicios_de_authentication, claude_orms, claude_ejercicio_extra_sql_python [EXTRACTED 1.00]

## Communities (11 total, 4 thin omitted)

### Community 0 - "ORMs Exercise Managers & DB Setup"
Cohesion: 0.11
Nodes (12): validate_and_create_schema(), validate_and_create_tables(), validate_connection(), run_exercise(), setup_database(), AddressManager, CarManager, UserManager (+4 more)

### Community 1 - "Authorization Exercise Data Managers"
Cohesion: 0.14
Nodes (9): InvoiceManager, ProductManager, Invoice, InvoiceItem, Product, Base, test_invoice_manager(), test_product_manager() (+1 more)

### Community 2 - "Authentication Core (DB + JWT)"
Cohesion: 0.14
Nodes (7): DB_manager, JWT_Manager, liveness(), login(), me(), route, register()

### Community 3 - "Authorization API Routes"
Cohesion: 0.23
Nodes (14): create_invoice(), create_product(), _get_current_payload(), _get_token_from_header(), _is_admin(), list_invoices(), list_products(), list_users() (+6 more)

### Community 5 - "Project Documentation Overview"
Cohesion: 0.14
Nodes (14): db.py, Ejercicio Extra SQL python, Ejercicios de Authentication, postgresPython/main.py, Model/Data Mapping, ORMs, postgresPython, PostgreSQL (+6 more)

### Community 9 - "ORM Data Models"
Cohesion: 0.60
Nodes (4): Address, Car, Base, User

## Knowledge Gaps
- **11 isolated node(s):** `Ejercicios de Authentication`, `db.py`, `repositories.py`, `Ejercicio Extra SQL python`, `test` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Authorization User Manager` to `ORMs Exercise Managers & DB Setup`, `Authorization Exercise Data Managers`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `UserManager` connect `Authorization User Manager` to `Authorization Exercise Data Managers`, `Authorization API Routes`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `UserManager` connect `ORMs Exercise Managers & DB Setup` to `Authorization User Manager`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `InvoiceManager` (e.g. with `Invoice` and `InvoiceItem`) actually correct?**
  _`InvoiceManager` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Ejercicios de Authentication`, `db.py`, `repositories.py` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ORMs Exercise Managers & DB Setup` be split into smaller, more focused modules?**
  _Cohesion score 0.11092436974789915 - nodes in this community are weakly interconnected._
- **Should `Authorization Exercise Data Managers` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._