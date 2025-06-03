# 🚀 部署指南 / Deployment Guide

本指南提供了CTF智能分析平台的完整部署方案，支持Docker、云端和本地部署。

---

## 📋 部署选项概览 / Deployment Options Overview

| 部署方式 | 复杂度 | 适用场景 | 优势 |
|----------|--------|----------|------|
| 🐳 **Docker Compose** | ⭐ 简单 | 开发、测试 | 一键部署，环境隔离 |
| 📦 **本地部署** | ⭐⭐ 中等 | 开发环境 | 灵活配置，易于调试 |
| ☁️ **云端部署** | ⭐⭐⭐ 复杂 | 生产环境 | 高可用，可扩展 |
| 🔧 **源码部署** | ⭐⭐ 中等 | 定制开发 | 完全控制，可定制 |

---

## 🐳 Docker Compose 部署 (推荐)

### 📋 前置要求

```bash
# 检查Docker和Docker Compose版本
docker --version          # >= 20.10.0
docker-compose --version  # >= 1.29.0
```

### ⚡ 快速部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd Cybersecurity

# 2. 配置环境变量
cp env.example .env

# 3. 编辑配置文件（必需）
nano .env  # 或使用你喜欢的编辑器

# 4. 启动服务
docker-compose up -d

# 5. 验证部署
curl http://localhost:8000/health
curl http://localhost:3000/
```

### 🔧 详细配置

#### 环境变量配置
```env
# 基础配置
AI_SERVICE=deepseek  # 选择AI服务提供者
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///./ctf_analyzer.db

# AI服务配置（根据选择的服务配置对应项）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SILICONFLOW_API_KEY=your_siliconflow_api_key_here

# 服务器配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 性能配置
ENABLE_CACHE=True
CACHE_TTL=3600
REQUEST_TIMEOUT=60
MAX_FILE_SIZE=10485760

# 日志配置
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

#### Docker Compose 配置优化

<details>
<summary>生产环境配置示例</summary>

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
    volumes:
      - ./backend/logs:/app/logs
      - backend_data:/app/data
    restart: unless-stopped
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  backend_data:
  postgres_data:
```

</details>

### 🛠️ 运维命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart backend
docker-compose restart frontend

# 更新服务
docker-compose pull
docker-compose up -d

# 停止服务
docker-compose down

# 完全清理（包括数据）
docker-compose down -v
```

---

## 📦 本地部署

### 📋 系统要求

```bash
# 操作系统：Ubuntu 20.04+, CentOS 8+, macOS 10.15+, Windows 10+
# Python: 3.8+
# Node.js: 16+
# 内存: 4GB+ (本地模型需要更多)
# 磁盘: 10GB+
```

### 🔧 安装步骤

#### 1. 环境准备

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nodejs npm git

# CentOS/RHEL
sudo yum install python3 python3-pip nodejs npm git

# macOS (使用Homebrew)
brew install python3 node git

# Windows (使用Chocolatey)
choco install python3 nodejs git
```

#### 2. 项目部署

```bash
# 克隆项目
git clone <repository-url>
cd Cybersecurity

# 使用一键安装脚本
chmod +x install.sh
./install.sh

# 或手动安装
# 后端设置
cd backend
pip3 install -r requirements.txt
python3 init_db.py

# 前端设置
cd ../frontend
npm install
npm run build  # 生产环境构建

# 启动服务
cd ..
chmod +x start.sh
./start.sh
```

#### 3. 系统服务配置

<details>
<summary>systemd 服务配置</summary>

创建后端服务：
```bash
# /etc/systemd/system/ctf-backend.service
[Unit]
Description=CTF Analysis Platform Backend
After=network.target

[Service]
Type=simple
User=ctf
WorkingDirectory=/opt/ctf-platform/backend
Environment=PATH=/opt/ctf-platform/venv/bin
ExecStart=/opt/ctf-platform/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

创建前端服务：
```bash
# /etc/systemd/system/ctf-frontend.service
[Unit]
Description=CTF Analysis Platform Frontend
After=network.target

[Service]
Type=simple
User=ctf
WorkingDirectory=/opt/ctf-platform/frontend
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ctf-backend ctf-frontend
sudo systemctl start ctf-backend ctf-frontend
```

</details>

---

## ☁️ 云端部署

### 🌐 AWS 部署

#### ECS (Elastic Container Service) 部署

<details>
<summary>AWS ECS 配置</summary>

1. **创建 ECR 仓库**
```bash
# 创建仓库
aws ecr create-repository --repository-name ctf-platform-backend
aws ecr create-repository --repository-name ctf-platform-frontend

# 构建并推送镜像
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

docker build -t ctf-platform-backend ./backend
docker tag ctf-platform-backend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/ctf-platform-backend:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/ctf-platform-backend:latest
```

2. **ECS 任务定义**
```json
{
  "family": "ctf-platform",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/ctf-platform-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DEEPSEEK_API_KEY",
          "value": "${DEEPSEEK_API_KEY}"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ctf-platform",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

</details>

### 🚀 其他云平台

#### Heroku 部署
```bash
# 安装 Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 登录并创建应用
heroku login
heroku create ctf-platform-backend
heroku create ctf-platform-frontend

# 设置环境变量
heroku config:set DEEPSEEK_API_KEY=your_key_here -a ctf-platform-backend

# 部署
git push heroku main
```

#### DigitalOcean App Platform
```yaml
# .do/app.yaml
name: ctf-platform
services:
- name: backend
  source_dir: /backend
  github:
    repo: your-username/ctf-platform
    branch: main
  run_command: python main.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEEPSEEK_API_KEY
    value: your_key_here
    type: SECRET

- name: frontend
  source_dir: /frontend
  github:
    repo: your-username/ctf-platform
    branch: main
  build_command: npm run build
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
```

---

## 🔧 高级配置

### 🏗️ 负载均衡配置

#### Nginx 配置
```nginx
# /etc/nginx/sites-available/ctf-platform
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;  # 多实例负载均衡
}

server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # 前端静态文件
    location / {
        root /opt/ctf-platform/frontend/build;
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://backend;
    }
}
```

### 📊 监控配置

#### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

---

## 🧪 测试和验证

### ✅ 部署验证脚本

```bash
#!/bin/bash
# deploy-test.sh

echo "🔍 开始部署验证..."

# 检查服务状态
echo "📡 检查后端服务..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    exit 1
fi

echo "🌐 检查前端服务..."
if curl -s http://localhost:3000/ | grep -q "CTF智能分析平台"; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
    exit 1
fi

echo "🧪 检查API功能..."
if curl -s -X POST -F "text=测试题目" http://localhost:8000/api/analyze | grep -q "id"; then
    echo "✅ API功能正常"
else
    echo "❌ API功能异常"
    exit 1
fi

echo "🎉 部署验证完成！"
```

### 🚨 故障排除

#### 常见问题解决

<details>
<summary>服务启动失败</summary>

**后端启动失败**
```bash
# 检查端口占用
sudo lsof -i :8000

# 检查依赖安装
pip3 list | grep fastapi

# 查看详细错误
python3 -m backend.main
```

**前端启动失败**
```bash
# 检查Node.js版本
node --version

# 清理缓存
rm -rf node_modules package-lock.json
npm install

# 检查内存使用
free -h
```

</details>

<details>
<summary>AI服务连接问题</summary>

```bash
# 测试API连接
curl -X POST -H "Content-Type: application/json" \
  -d '{"provider": "deepseek"}' \
  http://localhost:8000/api/test-connection

# 检查环境变量
echo $DEEPSEEK_API_KEY

# 网络连接测试
curl -I https://api.deepseek.com/
```

</details>

---

## 📈 性能优化

### 🚀 生产环境优化

#### 1. 数据库优化
```sql
-- SQLite 优化
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=10000;
PRAGMA temp_store=MEMORY;
```

#### 2. 应用优化
```python
# backend/config.py - 生产环境配置
ENABLE_CACHE = True
CACHE_TTL = 3600
REQUEST_TIMEOUT = 30
MAX_FILE_SIZE = 5242880  # 5MB
DEBUG = False
LOG_LEVEL = "INFO"
```

#### 3. 前端优化
```bash
# 生产构建优化
npm run build

# 启用 gzip 压缩
# Nginx 配置
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

---

## 🔒 安全配置

### 🛡️ 安全检查清单

- [ ] 更改默认密钥和密码
- [ ] 启用HTTPS/SSL
- [ ] 配置防火墙规则
- [ ] 定期更新依赖包
- [ ] 配置访问日志
- [ ] 设置API速率限制
- [ ] 备份关键数据

### 🔐 SSL/TLS 配置

```bash
# 使用 Let's Encrypt 获取免费证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 📞 支持和维护

### 🆘 获取帮助

- 📖 [项目文档](../README.md)
- 🐛 [问题报告](https://github.com/your-repo/issues)
- 💬 [社区讨论](https://github.com/your-repo/discussions)

### 🔄 更新和维护

```bash
# 检查更新
git pull origin main

# 更新依赖
pip3 install -r requirements.txt --upgrade
npm update

# 数据库迁移（如果需要）
python3 manage.py migrate

# 重启服务
sudo systemctl restart ctf-backend ctf-frontend
```

---

*本指南持续更新，确保包含最新的部署最佳实践* 