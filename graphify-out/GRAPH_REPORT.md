# Graph Report - auto-ai-service  (2026-10-22)

## Corpus Check
- Corpus is ~1,934 words - fits in a single context window. You may not need a graph.

## Summary
- 125 nodes · 198 edges · 17 communities (16 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.84)
- Token cost: 44,065 input · 0 output

## Community Hubs (Navigation)
- README Architecture Concepts
- Services CRUD API
- Auth & Password Security
- DB Session & Current User
- App Config & Bootstrap
- ORM Models & Base
- Project Manifest

## God Nodes (most connected - your core abstractions)
1. `auto-ai-service` - 12 edges
2. `Base` - 9 edges
3. `Service` - 9 edges
4. `login()` - 8 edges
5. `update_service()` - 8 edges
6. `create_service()` - 7 edges
7. `User` - 7 edges
8. `get_current_user()` - 6 edges
9. `register()` - 6 edges
10. `_get_or_404()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `get_current_user()` --references--> `User`  [EXTRACTED]
  app/api/deps.py → app/models/user.py
- `register()` --calls--> `User`  [EXTRACTED]
  app/api/routes/auth.py → app/models/user.py
- `Service` --inherits--> `Base`  [EXTRACTED]
  app/models/service.py → app/db/base.py
- `Service` --inherits--> `TimestampMixin`  [EXTRACTED]
  app/models/service.py → app/db/base.py
- `get_current_user()` --calls--> `decode_access_token()`  [EXTRACTED]
  app/api/deps.py → app/core/security.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core Backend Stack** — readme_fastapi, readme_uvicorn, readme_sqlalchemy_2_0_orm, readme_alembic_migrations, readme_pydantic_v2_validation [EXTRACTED 1.00]
- **Authentication Flow** — readme_auth_endpoints, readme_jwt_bearer_auth, readme_argon2_password_hashing, readme_jwt_secret_key, readme_get_db_dependency [INFERRED 0.85]

## Communities (17 total, 1 thin omitted)

### Community 0 - "README Architecture Concepts"
Cohesion: 0.13
Nodes (22): Alembic Migrations, API /api/v1, Argon2 Password Hashing, Auth Endpoints (/auth/register, /auth/login, /auth/me), auto-ai-service, CORS, FastAPI, get_db / DbSession / CurrentUser Dependencies (+14 more)

### Community 1 - "Services CRUD API"
Cohesion: 0.22
Nodes (19): _commit_or_conflict(), create_service(), delete_service(), _get_or_404(), get_service(), list_services(), CurrentUser, DbSession (+11 more)

### Community 2 - "Auth & Password Security"
Cohesion: 0.18
Nodes (16): login(), DbSession, Depends, post, register(), create_access_token(), hash_password(), verify_password() (+8 more)

### Community 3 - "DB Session & Current User"
Cohesion: 0.17
Nodes (14): get_current_user(), DbSession, Depends, decode_access_token(), Raises jwt.PyJWTError if the token is invalid or expired., get_db(), Session, fixture (+6 more)

### Community 4 - "App Config & Bootstrap"
Cohesion: 0.20
Nodes (5): get_settings(), Settings, health(), get, BaseSettings

### Community 5 - "ORM Models & Base"
Cohesion: 0.36
Nodes (7): me(), CurrentUser, get, Base, TimestampMixin, User, DeclarativeBase

## Knowledge Gaps
- **7 isolated node(s):** `auto-ai-service`, `Pydantic v2 Validation`, `GET /health`, `pytest with In-memory SQLite`, `uv` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Base` connect `ORM Models & Base` to `Services CRUD API`, `DB Session & Current User`, `App Config & Bootstrap`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `get_current_user()` connect `DB Session & Current User` to `ORM Models & Base`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Service` connect `Services CRUD API` to `ORM Models & Base`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **What connects `auto-ai-service`, `Pydantic v2 Validation`, `GET /health` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `README Architecture Concepts` be split into smaller, more focused modules?**
  _Cohesion score 0.12987012987012986 - nodes in this community are weakly interconnected._