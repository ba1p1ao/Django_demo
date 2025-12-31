# 在线考试系统 - IFLOW 上下文文档

## 项目概述

这是一个基于 Django REST Framework 后端和 Vue 3 前端的在线考试系统。系统支持用户管理、题目管理、试卷管理、在线考试和考试记录统计等功能。

### 技术栈

**后端 (exam_system):**
- Python 3.10+
- Django 4.2.5
- Django REST Framework
- SQLite 数据库（开发环境）
- JWT 认证

**前端 (exam-frontend):**
- Vue 3.5.24
- Vite 7.2.4
- Element Plus UI 组件库
- Pinia 状态管理
- Vue Router 4.6.4
- Axios HTTP 客户端

## 项目结构

```
kaoshigunalimanager/
├── exam_system/                    # Django 后端项目
│   ├── apps/                       # Django 应用
│   │   ├── user/                   # 用户管理模块
│   │   ├── question/               # 题目管理模块
│   │   └── exam/                   # 试卷和考试模块
│   ├── exam_system/                # Django 项目配置
│   │   ├── settings.py             # 项目设置
│   │   ├── urls.py                 # 主路由配置
│   │   └── ...
│   ├── utils/                      # 工具模块
│   │   ├── JWTAuth.py              # JWT 认证
│   │   ├── PasswordEncode.py       # 密码加密
│   │   └── ResponseMessage.py      # 响应消息工具
│   ├── db.sqlite3                  # SQLite 数据库
│   └── manage.py                   # Django 管理脚本
└── exam-frontend/                  # Vue 前端项目
    ├── src/
    │   ├── api/                    # API 接口定义
    │   │   ├── user.js             # 用户相关 API
    │   │   ├── question.js         # 题目相关 API
    │   │   └── exam.js             # 考试相关 API
    │   ├── assets/                 # 静态资源
    │   ├── components/             # 公共组件
    │   ├── router/                 # 路由配置
    │   ├── stores/                 # Pinia 状态管理
    │   ├── utils/                  # 工具函数
    │   ├── views/                  # 页面视图
    │   ├── App.vue                 # 根组件
    │   └── main.js                 # 应用入口
    ├── package.json                # 前端依赖配置
    ├── vite.config.js              # Vite 配置
    └── ...
```

## API 接口文档

完整的 API 接口文档请参考 `API文档.md` 文件。主要接口包括：

### 基础信息
- **Base URL**: `http://localhost:8010/api`
- **认证方式**: Bearer Token
- **响应格式**: JSON

### 主要模块
1. **用户模块** (`/api/user/`)
   - 用户注册、登录、信息管理
   - JWT 认证

2. **题目模块** (`/api/question/`)
   - 题目增删改查
   - 支持单选、多选、判断、填空四种题型

3. **试卷模块** (`/api/exam/`)
   - 试卷创建、发布、管理
   - 随机组卷功能

4. **考试模块** (`/api/exam/`)
   - 开始考试、保存答案、提交试卷
   - 考试记录管理

5. **统计模块** (`/api/exam/`)
   - 考试成绩统计
   - 通过率分析

## 开发环境设置

### 后端设置

1. **安装依赖**：
   ```bash
   cd exam_system
   pip install -r requirements.txt  # 如果存在 requirements.txt
   # 或手动安装
   pip install django==4.2.5 djangorestframework django-cors-headers
   ```

2. **数据库迁移**：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **创建超级用户**：
   ```bash
   python manage.py createsuperuser
   ```

4. **运行开发服务器**：
   ```bash
   python manage.py runserver 8010
   ```

### 前端设置

1. **安装依赖**：
   ```bash
   cd exam-frontend
   npm install
   ```

2. **运行开发服务器**：
   ```bash
   npm run dev
   ```
   前端将在 `http://localhost:8090` 运行，并代理 API 请求到 `http://localhost:8010`

## 构建和部署

### 后端构建
```bash
cd exam_system
# 生产环境设置
# 修改 settings.py 中的 DEBUG = False
# 配置 ALLOWED_HOSTS
python manage.py collectstatic
```

### 前端构建
```bash
cd exam-frontend
npm run build
```
构建后的文件在 `dist/` 目录中。

## 开发约定

### 后端约定
1. **应用结构**：每个功能模块对应一个 Django 应用
2. **认证方式**：使用 JWT Token 认证
3. **响应格式**：统一使用 `ResponseMessage` 工具类返回 JSON 响应
4. **错误处理**：使用自定义异常类处理业务异常
5. **跨域配置**：已配置允许所有域名跨域访问（开发环境）

### 前端约定
1. **组件结构**：使用 Vue 3 Composition API
2. **状态管理**：使用 Pinia 进行状态管理
3. **UI 组件**：使用 Element Plus 组件库
4. **API 调用**：统一使用 `src/utils/request.js` 中的 axios 实例
5. **路由管理**：使用 Vue Router 4

## 数据库模型

### 用户模型 (User)
- 用户名、密码、昵称、角色（student/teacher）
- 头像、状态、创建时间

### 题目模型 (Question)
- 题目类型（single/multiple/judge/fill）
- 题目内容、选项、正确答案
- 分类、难度、分值、解析

### 试卷模型 (Exam)
- 试卷标题、描述、时长
- 总分、及格分、开始/结束时间
- 是否随机组卷、状态（draft/published/closed）

### 考试记录模型 (ExamRecord)
- 用户、试卷关联
- 考试成绩、是否通过
- 状态（not_started/in_progress/submitted/graded）
- 开始时间、提交时间

## 测试

### 后端测试
```bash
cd exam_system
python manage.py test
```

### 前端测试
```bash
cd exam-frontend
# 根据项目配置运行测试
```

## 常见问题

1. **跨域问题**：后端已配置 CORS，确保前端代理配置正确
2. **数据库问题**：首次运行需要执行数据库迁移
3. **端口冲突**：后端默认端口 8010，前端默认端口 8090
4. **JWT 认证**：登录后需要在请求头中添加 `Authorization: Bearer {token}`

## 项目状态

当前项目为开发版本，包含完整的用户管理、题目管理、试卷管理和在线考试功能。API 接口文档完整，前端界面使用 Element Plus 构建。

## 后续开发建议

1. **功能增强**：
   - 添加考试监控功能（防作弊）
   - 支持富文本题目编辑
   - 添加考试时间提醒
   - 支持试卷模板

2. **性能优化**：
   - 数据库查询优化
   - 前端代码分割
   - 缓存策略实现

3. **部署优化**：
   - Docker 容器化部署
   - Nginx 反向代理配置
   - 数据库迁移到 PostgreSQL/MySQL

4. **安全性增强**：
   - 密码强度验证
   - 登录失败限制
   - API 访问频率限制

## 相关文件

- `API文档.md`：完整的 API 接口文档
- `exam_system/`：Django 后端项目
- `exam-frontend/`：Vue 前端项目