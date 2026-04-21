# MovieSite
tv-play是一个基于 Sanic 框架构建的影视网站后端服务。仅供个人娱乐，请勿商用。

## 技术栈

- **框架**: Sanic 21.0+
- **模板引擎**: Jinja2
- **数据库**: MySQL 5.7+ / MariaDB 10.0+
- **缓存**: Redis 5.0+
- **语言**: Python 3.8+

## 功能特性

- ✅ 首页展示 - 热门影视推荐
- ✅ 分类浏览 - 按类型筛选影视内容
- ✅ 播放页面 - 视频播放与详情展示
- ✅ 搜索功能 - 关键词搜索影视
- ✅ 404错误页面 - 友好的错误提示

## 项目结构

```
├── app.py                 # 应用入口
├── config.py              # 配置文件
├── extensions.py          # 扩展初始化
├── requirements.txt       # 依赖列表
├── init.sql               # 数据库初始化脚本
├── controllers/           # 控制器目录
│   ├── __init__.py
│   ├── home.py            # 首页控制器
│   ├── category.py        # 分类控制器
│   ├── play.py            # 播放控制器
│   └── search.py          # 搜索控制器
├── services/              # 服务层目录
│   ├── __init__.py
│   ├── api_service.py     # API服务
│   └── db_service.py      # 数据库服务
├── templates/             # 模板目录
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页模板
│   ├── category.html      # 分类页模板
│   ├── play.html          # 播放页模板
│   ├── search.html        # 搜索页模板
│   └── 404.html           # 404模板
└── static/                # 静态资源目录
    └── css/
        └── style.css      # 样式文件
```

## 部署方式

### 环境要求

- Python 3.8+
- MySQL 5.7+ 或 MariaDB 10.0+
- Redis 5.0+

### 1. 克隆项目

```bash
git clone https://gitee.com/lcyinsu_yinsuso/tv-play.git
cd MovieSite
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

#### 创建数据库和用户

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE tv CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'tv'@'localhost' IDENTIFIED BY 'E3CM6jKs8wCbXSx8';

-- 授权
GRANT ALL PRIVILEGES ON tv.* TO 'tv'@'localhost';
FLUSH PRIVILEGES;
```

#### 初始化数据表

```bash
mysql -u tv -p tv < init.sql
```

### 5. 配置 Redis

确保 Redis 服务已启动并运行在默认端口 `6379`。

### 6. 启动服务

```bash
# 开发模式
python app.py

# 或使用 sanic 命令
sanic app.app --host=0.0.0.0 --port=30001 --debug
```

### 7. 访问服务

启动后访问: `http://localhost:30001`

## 配置说明

配置文件位于 `config.py`：

```python
# 第三方API地址
API_URL = "" # 此处填写影视资源的API地址

# MySQL配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'tv',
    'password': 'E3CM6jKs8wCbXSx8',
    'db': 'tv',
    'charset': 'utf8mb4',
    'autocommit': True,
}

# Redis配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

# 缓存过期时间（秒）
CACHE_EXPIRE = 300

# 每页显示数量
PAGE_SIZE = 20
```

## 路由说明

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/category/<type_id>` | GET | 分类页 |
| `/play/<vod_id>` | GET | 播放页 |
| `/search` | GET | 搜索页 |

## 开发

### 安装开发依赖

```bash
pip install sanic sanic-jinja2 requests redis aiomysql
```

### 调试模式

```bash
python app.py  # debug=True 模式
```

## 生产部署建议

### 使用 Gunicorn（推荐）

```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:30001 --workers 4 --worker-class sanic.worker.GunicornWorker
```

### 使用 systemd 管理服务

创建 `/etc/systemd/system/moviesite.service`：

```ini
[Unit]
Description=MovieSite Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/MovieSite
ExecStart=/path/to/venv/bin/gunicorn app:app --bind 0.0.0.0:30001 --workers 4 --worker-class sanic.worker.GunicornWorker
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
systemctl daemon-reload
systemctl start moviesite
systemctl enable moviesite
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 本项目仅供学习交流使用，请遵守相关法律法规。
