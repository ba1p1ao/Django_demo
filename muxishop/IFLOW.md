# MuxiShop 项目文档

## 项目概述

MuxiShop 是一个基于 Django REST Framework 和 Vue 3 的全栈电商平台，包含完整的商品管理、购物车、订单系统、用户认证、支付功能等电商核心功能。

### 技术栈

**后端 (Django REST Framework)**
- Django 4.2.5
- Django REST Framework (DRF)
- MySQL 数据库（连接池配置）
- Redis 缓存（用于验证码存储）
- JWT 认证（自定义实现）
- 支付宝沙箱支付集成

**前端 (Vue 3)**
- Vue 3.2.13
- Element Plus UI 组件库
- Vue Router 4.0.3（路由管理）
- Vuex 4.0.0（状态管理）
- Axios 1.4.0（HTTP 请求）
- vue3-seamless-scroll（无缝滚动）
- Less CSS 预处理器

### 项目架构

```
muxishop/
├── apps/                 # Django 应用模块
│   ├── address/         # 地址管理
│   ├── cart/            # 购物车
│   ├── comment/         # 评论系统
│   ├── goods/           # 商品管理
│   ├── menu/            # 菜单/分类
│   ├── order/           # 订单管理
│   ├── pay/             # 支付集成
│   ├── tools/           # 工具类
│   └── user/            # 用户管理
├── muxishop/            # Django 项目配置
├── muxishopweb/         # Vue 前端应用
├── muxishopwebdemo/     # Vue 前端演示应用
├── static/              # 静态文件
│   ├── captcha_code/    # 验证码图片
│   └── product_images/  # 商品图片
└── utils/               # 工具函数
    ├── CaptchaCode.py   # 验证码生成
    ├── JWTAuth.py       # JWT 认证
    ├── PasswordEncode.py # 密码加密
    └── ResponseMessage.py # 响应消息封装
```

## 构建和运行

### 后端 (Django)

**启动开发服务器**
```bash
# 确保已安装依赖
pip install django djangorestframework pymysql django-cors-headers redis pycryptodome jwt

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

**数据库配置**
- 数据库类型：MySQL
- 主机：127.0.0.1
- 端口：3306
- 数据库名：muxishop
- 用户：root
- 密码：123
- 连接池大小：10，最大溢出：30

**Redis 配置**
- 地址：redis://127.0.0.1:6379/1
- 超时时间：60 秒
- Key 前缀：muxishop_captcha

### 前端 (Vue 3)

**开发环境**
```bash
# 进入前端目录
cd muxishopweb  # 或 muxishopwebdemo

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

**生产构建**
```bash
# 构建生产版本
npm run build
```

## 开发约定

### 后端约定

1. **应用结构**
   - 每个 Django 应用包含：models.py、serializers.py、views.py、urls.py
   - 使用 REST Framework 的序列化器进行数据验证和序列化
   - 统一使用 `utils.ResponseMessage` 封装响应消息

2. **认证机制**
   - 使用 JWT 进行用户认证
   - Token 可通过请求头（Authorization: Bearer <token>）或查询参数（?token=xxx）传递
   - Token 默认过期时间：3600 秒（1小时）

3. **URL 路由**
   - 所有应用路由通过主 urls.py 的 include 引入
   - 路由前缀：/menu/, /goods/, /cart/, /user/, /order/, /address/, /comment/, /pay/, /tools/

4. **数据库模型**
   - 所有模型使用显式 db_table 名称（小写）
   - 时间字段使用 auto_now_add 设置创建时间
   - Decimal 字段用于金额（max_digits=10, decimal_places=2）

5. **跨域配置**
   - 允许所有域名跨域（CORS_ORIGIN_ALLOW_ALL = True）
   - 允许携带凭证（CORS_ALLOW_CREDENTIALS = True）

### 前端约定

1. **技术栈**
   - Vue 3 Composition API
   - Element Plus UI 组件库
   - Vuex 状态管理
   - Vue Router 路由管理

2. **代码结构**
   - src/views/：页面组件
   - src/components/：公共组件
   - src/router/：路由配置
   - src/store/：Vuex store
   - src/network/：网络请求封装（基于 Axios）
   - src/utils/：工具函数

3. **开发模式**
   - 使用 Less 进行样式编写
   - 遵循 Vue 3 最佳实践

### 支付配置

**支付宝沙箱环境**
- APPID：9021000158671301
- 开发环境：ALIPAY_DEBUG = True
- 网关：https://openapi-sandbox.dl.alipaydev.com/gateway.do
- 异步通知 URL：http://127.0.0.1:8000/pay/alipay/return
- 同步返回 URL：http://127.0.0.1:8000/pay/alipay/return

**密钥文件位置**
- 应用私钥：apps/pay/keys/private_key.txt
- 支付宝公钥：apps/pay/keys/alipay_key.txt

### 验证码配置

- 过期时间：5 分钟（CAPTCHA_EXPIRE_TIME = 5 * 60）
- 存储位置：Redis（数据库 1）
- Key 前缀：muxishop_captcha

### 国际化配置

- 语言：zh-hans（简体中文）
- 时区：Asia/Shanghai

### 静态文件配置

- 访问路径：/static/
- 静态文件目录：static/
- 商品图片 URL：http://localhost:8000/static/product_images/

## 核心功能模块

### 用户模块 (apps/user)
- 用户注册、登录
- JWT Token 生成和验证
- 用户信息管理

### 商品模块 (apps/goods)
- 商品列表、详情
- 商品分类（type_id）
- 价格管理（京东价、市场价、平台价）

### 购物车模块 (apps/cart)
- 添加商品到购物车
- 购物车商品管理

### 订单模块 (apps/order)
- 订单创建
- 订单状态管理
- 订单商品关联

### 支付模块 (apps/pay)
- 支付宝支付集成
- 支付回调处理
- 签名验证

### 地址模块 (apps/address)
- 用户地址管理
- 默认地址设置

### 评论模块 (apps/comment)
- 商品评论功能

### 菜单模块 (apps/menu)
- 商品分类/菜单管理

### 工具模块 (apps/tools)
- 辅助工具功能

## 注意事项

1. **安全性**
   - 生产环境需修改 SECRET_KEY
   - 关闭 DEBUG 模式
   - 配置 ALLOWED_HOSTS
   - 不要提交敏感信息到版本控制

2. **数据库**
   - 使用 MySQL 时需在项目主目录的 __init__.py 中添加：
     ```python
     from pymysql import install_as_MySQLdb
     install_as_MySQLdb()
     ```

3. **跨域**
   - 已禁用 CSRF 中间间（注释掉 'django.middleware.csrf.CsrfViewMiddleware'）

4. **认证**
   - 默认使用 JWTHeaderQueryParamAuthentication 认证类
   - 支持 Bearer Token 和查询参数两种方式

5. **图片处理**
   - 商品图片存储在 static/product_images/ 目录
   - 使用 DecimalEncoder 处理 Decimal 类型的 JSON 序列化