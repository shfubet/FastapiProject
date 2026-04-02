# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based async web application with MySQL (SQLAlchemy 2.0 async) and Redis. The API root path is `/api/v1`.

## Running the Application

```bash
cd /Users/duwei/project/FastapiProject
source env/bin/activate
python -m app.main
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload --port 8000
```

## Database Migrations (Alembic)

```bash
# Create a new migration
alembic revision --autogenerate -m "migration name"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

Migrations are in `alembic/versions/`. The migration environment uses async SQLAlchemy with `aiomysql`.

## Configuration

All configuration is managed via `configs/config.yaml` (loaded by `app/core/__init__.py`). Key sections:
- `service.port` - server port
- `mysql.url` - async MySQL connection string
- `redis` - Redis connection settings
- `logs` - logging configuration

## Architecture

### Layered Structure
- **API Layer**: `app/api/v1/` - FastAPI routers and views
- **Service Layer**: `app/services/` - Business logic
- **Repository Layer**: `app/repositories/` - Database access (Repository pattern)
- **Model Layer**: `app/models/` - SQLAlchemy ORM models
- **Schema Layer**: `app/schemas/` - Pydantic request/response schemas
- **Core Layer**: `app/core/` - Shared utilities (db, config, logger, exceptions, response)

### Key Components
- **Database**: `app/core/db.py` - async engine and session factory, `Session` type alias for dependency injection
- **Models**: `app/core/model.py` - `Base` (DeclarativeBase) and `BaseModel` (with id, created_at, updated_at, is_delete)
- **Exceptions**: `app/core/exceptions.py` - BusinessException hierarchy
- **Response**: `app/core/response.py` - JsonResponse with standard `{code, message, data}` format

### Database Models
Models inherit from `BaseModel` (in `app/core/model.py`) which provides:
- `id` (primary key, auto-increment)
- `created_at`, `updated_at` (with timezone)
- `is_delete` (logical delete flag)

### Adding New API Endpoints

1. Create/update model in `app/models/`
2. Create/update repository in `app/repositories/` extending `Repository`
3. Create/update schema in `app/schemas/`
4. Create/update service in `app/services/`
5. Add route in `app/api/v1/<module>/views.py`
6. Register router in `app/api/__init__.py`'s `init_router()`

### Logging
Use `from app.core.logger import logger`. Provides structured logging with `logger.info_with()`, `logger.error_with()`, etc.

## Dependencies

Key packages (in `env/`):
- FastAPI, uvicorn
- SQLAlchemy 2.0 (async with aiomysql)
- Alembic
- Pydantic
- PyYAML
- Redis support


## Skills
- gc: 执行 .claude/skills/git-commit/SKILL.md

## 进行中的需求

### 已完成
- [项目重构计划](docs/claude/REFACTOR_PLAN.md) - 重构目录结构和分层架构 ✅
  - 任务详情: [docs/claude/process.md](./docs/claude/process.md)

### 待完成
- [ ] 添加 JWT 认证功能
- [ ] 集成 Redis 缓存