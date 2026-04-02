# 重构任务拆分

## 任务列表

### Task 1: 重命名目录结构
- **状态**: ✅ 已完成
- **描述**: 将 `app/model/` 重命名为 `app/models/`，将 `app/repo/` 重命名为 `app/repositories/`

### Task 2: 完善 Repository 基类
- **状态**: ✅ 已完成
- **描述**: 实现完整的 CRUD 基类方法
- **文件**: `app/repositories/repository.py`
- **已实现方法**: `get()`, `get_multi()`, `create()`, `update()`, `delete()` (软删除), `search()`, `get_by_field()`

### Task 3: 添加 Service 层
- **状态**: ✅ 已完成
- **描述**: 创建 UserService 处理用户相关业务逻辑
- **文件**: `app/services/user_service.py`

### Task 4: 完善 Schemas
- **状态**: ✅ 已完成
- **描述**: 添加完整的 User 相关 Pydantic schemas
- **文件**: `app/schemas/user.py`
- **已添加**: `UserCreate`, `UserUpdate`, `UserDetail`, `UserList`, `UserListResponse`

### Task 5: 重构 API 层
- **状态**: ✅ 已完成
- **描述**: 使用 APIRouter 规范重构登录模块
- **文件**: `app/api/v1/login/views.py`
- **新增**: `app/api/v1/deps.py`

### Task 6: 清理无用文件
- **状态**: ✅ 已完成
- **已删除**: `views2.py`, `decorator.py`, `view.py`, `users.py`

### Task 7: 更新 import 路径
- **状态**: ✅ 已完成
- **已更新**: 所有旧目录引用

### Task 8: 更新 CLAUDE.md
- **状态**: ✅ 已完成

### Task 9: 数据库表结构重构
- **状态**: ✅ 已完成
- **描述**: 清空旧迁移文件，重新生成 `tb_users` 表结构
- **文件**: `alembic/versions/472d2f95cd4e_init_tb_users.py`
- **表结构**:
  - `username` - varchar(50) NOT NULL
  - `name` - varchar(50) NOT NULL
  - `email` - varchar(100) NOT NULL UNIQUE
  - `created_at` - datetime NOT NULL
  - `updated_at` - datetime NOT NULL
  - `id` - int NOT NULL PRIMARY KEY AUTO_INCREMENT
  - `is_delete` - tinyint(1) NOT NULL DEFAULT 0

---

## API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/users/{user_id}` | 获取用户详情 |
| GET | `/users/` | 用户列表（分页） |
| POST | `/users/` | 创建用户 |
| PUT | `/users/{user_id}` | 更新用户 |
| DELETE | `/users/{user_id}` | 删除用户（软删除） |
| GET | `/users/search/` | 搜索用户 |

---

## 待办事项

- [ ] 添加 JWT 认证功能
- [ ] 集成 Redis 缓存
- [ ] 完善错误处理和日志记录
- [ ] 单元测试

---

## 验证方式

1. 启动应用：`uvicorn app.main:app --reload --port 8000`
2. 测试 CRUD API 端点
3. 运行 `alembic upgrade head` 确保数据库结构正确

---

## 今日完成

✅ 项目重构（目录结构 + 分层架构）
✅ 完善 Repository 基类（异步 CRUD）
✅ 添加 Service 层
✅ 完善 Schemas
✅ 重构 API 层（APIRouter）
✅ 清理无用文件
✅ 数据库迁移文件重建
✅ `tb_users` 表创建完成
