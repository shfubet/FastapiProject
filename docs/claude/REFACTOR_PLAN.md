# 项目重构计划

## 背景

当前项目结构存在以下问题：
1. **视图注册不规范** - 直接使用 `@app.get()` 而非 `@router.get()`
2. **Service 层缺失** - `app/service/` 目录为空，业务逻辑混在视图中
3. **Repository 层不完整** - 只有 `get()` 方法，缺少 `create/update/delete/get_multi` 等
4. **Schema 不完整** - 只有 `UserDetail`，缺少 `UserCreate/UserUpdate/UserList`
5. **views2.py 是空壳** - 需要清理或完善
6. **Redis 未集成** - 配置了但未使用

## 重构目标

保持 FastAPI 最佳实践的分层架构：
```
API Layer (Routers) -> Service Layer -> Repository Layer -> Model Layer
                           -> Schema Layer (Pydantic)
```

## 新目录结构

```
app/
├── __init__.py
├── main.py                 # 保持不变
├── api/
│   ├── __init__.py         # create_app 工厂
│   └── v1/
│       ├── __init__.py     # init_router 路由注册
│       ├── deps.py         # 依赖注入 (get_db, get_current_user 等)
│       └── login/
│           ├── __init__.py
│           ├── views.py    # 使用 APIRouter 规范注册
│           └── schemas.py  # 登录相关 Pydantic schemas
├── core/
│   ├── __init__.py         # 配置加载
│   ├── config.py           # Pydantic 配置模型
│   ├── db.py               # SQLAlchemy async engine & session
│   ├── exceptions.py       # 业务异常
│   ├── response.py         # JsonResponse
│   └── logger.py           # 结构化日志
├── models/                 # 改为 models (不是 model)
│   ├── __init__.py
│   └── user.py
├── repositories/           # 改为 repositories
│   ├── __init__.py
│   └── user_repository.py
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── user.py             # UserCreate, UserUpdate, UserDetail, UserList
│   └── response.py         # 通用分页响应
├── services/               # service 层
│   ├── __init__.py
│   └── user_service.py
└── utils/                  # 工具函数
    ├── __init__.py
    └── security.py         # 密码哈希、JWT 等
```

## 实施步骤

### Step 1: 重命名目录
- `app/model/` → `app/models/`
- `app/repo/` → `app/repositories/`

### Step 2: 完善 Repository 层 (`app/repositories/repository.py`)
实现基类 CRUD 方法：
- `get()` - 获取单个
- `get_multi()` - 分页列表
- `create()` - 创建
- `update()` - 更新
- `delete()` - 软删除 (is_delete=True)
- `search()` - 条件搜索

### Step 3: 添加 Service 层 (`app/services/`)
- `UserService` - 用户相关业务逻辑
- 与 Repository 交互，处理业务规则

### Step 4: 完善 Schemas (`app/schemas/user.py`)
- `UserCreate` - 创建用户请求
- `UserUpdate` - 更新用户请求
- `UserDetail` - 用户详情响应
- `UserList` - 用户列表响应

### Step 5: 重构 API 层 (`app/api/v1/`)
- 使用 `APIRouter` 替代直接装饰 FastAPI 实例
- View 只负责 HTTP 逻辑，调用 Service 层
- 添加 `deps.py` 存放依赖注入函数

### Step 6: 清理无用文件
- 删除 `views2.py`
- 删除 `app/core/decorator.py`
- 删除 `app/core/view.py`
- 删除注释掉的死代码

### Step 7 (暂不实施): Redis 集成
用户选择暂不添加 Redis 集成

### Step 8 (暂不实施): JWT 认证
用户选择暂不添加 JWT 认证

## 关键文件修改清单

| 文件 | 操作 |
|------|------|
| `app/model/` → `app/models/` | 重命名 |
| `app/repo/` → `app/repositories/` | 重命名 |
| `app/repositories/repository.py` | 重写，完整 CRUD |
| `app/repositories/user_repository.py` | 更新 import 路径 |
| `app/schemas/users.py` → `app/schemas/user.py` | 重写，添加完整 schemas |
| `app/api/v1/login/views.py` | 使用 APIRouter 重构 |
| `app/api/v1/deps.py` | 新增 |
| `app/services/user_service.py` | 新增 |
| `app/core/decorator.py` | 删除 |
| `app/core/view.py` | 删除 |
| `app/api/v1/login/views2.py` | 删除 |

**注**：用户选择暂不添加 JWT 认证和 Redis 集成

## 验证方式

1. 启动应用：`python -m app.main` 或 `uvicorn app.main:app --reload`
2. 测试健康检查端点
3. 测试 CRUD API 端点
4. 运行 Alembic 迁移确保数据库结构正确
