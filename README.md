# 🚀 CTF智能分析平台 / CTF Intelligent Analysis Platform

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v2.1-green.svg)](https://github.com/your-repo/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

## 📖 项目简介 / Introduction

**CTF智能分析平台**是一个功能强大的多AI提供者CTF（Capture The Flag）题目智能分析平台，专为CTF学习者和参赛者设计。平台集成了先进的AI技术，支持Web、Pwn、Reverse、Crypto、Misc等所有主流CTF题型的智能分析和解题指导。

**🎉 v2.1 重大更新：全新网页端配置管理，一键切换AI服务！**

This project is a powerful multi-AI provider CTF challenge analysis platform designed for CTF learners and players. It integrates advanced AI technology to support intelligent analysis and guidance for all mainstream CTF categories including Web, Pwn, Reverse, Crypto, and Misc.

**🎉 v2.1 Major Update: Brand new web-based configuration management with one-click AI service switching!**

---

## ✨ 功能亮点 / Key Features

### 🎯 **智能分析引擎**
- 🤖 **多AI支持**: DeepSeek、硅基流动、OpenAI兼容API、本地模型
- 🧠 **智能题型识别**: 自动分析题目类型和特征
- 💡 **解题思路生成**: AI驱动的解题策略和步骤指导
- 🛠️ **工具推荐**: 针对性的CTF工具和命令建议

### ⚙️ **网页端配置管理** ⭐ **NEW**
- 🎨 **可视化设置**: 右上角齿轮图标，现代化Material-UI界面
- 🔄 **一键切换**: 无需重启，实时切换AI服务提供者
- 🔐 **安全管理**: API密钥安全显示和存储
- 🧪 **连接测试**: 内置测试功能验证配置有效性

### 🚀 **企业级功能**
- ⚡ **智能缓存**: 大幅提升响应速度，减少重复请求
- 📊 **性能监控**: 实时监控AI服务性能和系统状态
- 📝 **结构化日志**: 完整的操作记录和错误追踪
- 🏥 **健康检查**: 系统状态监控和故障诊断

### 💻 **用户体验**
- 📱 **响应式设计**: 支持桌面和移动端访问
- 📁 **多格式支持**: 文本、代码、文件上传分析
- 📈 **统计面板**: 题目类型分布和解题记录统计
- 🔍 **历史记录**: 完整的分析历史和解题轨迹

---

## 🛠️ 技术栈 / Tech Stack

### 前端架构
```
React 18 + TypeScript
├── Material-UI (MUI) - 现代化组件库
├── React Router - 路由管理
├── Axios - HTTP客户端
└── 响应式设计 - 移动端适配
```

### 后端架构
```
FastAPI + Python 3.8+
├── SQLAlchemy + SQLite - 数据持久化
├── 多AI提供者支持
│   ├── DeepSeek API
│   ├── 硅基流动 API
│   ├── 本地模型（transformers + torch）
│   └── OpenAI兼容API
├── 缓存系统 - 内存缓存优化
├── 日志系统 - 结构化日志记录
└── 配置管理 - 环境变量管理
```

### 部署方案
```
容器化部署
├── Docker & Docker Compose
├── 健康检查支持
├── 环境配置验证
└── 一键启动脚本
```

---

## 🚀 快速开始 / Quick Start

### 📋 前置要求 / Prerequisites

- **Node.js** 16+ & npm
- **Python** 3.8+
- **AI服务**: DeepSeek/硅基流动API密钥 **或** 本地AI模型

### ⚡ 一键启动 / One-Click Setup

```bash
# 1. 克隆项目
git clone <repository-url>
cd Cybersecurity

# 2. 配置环境变量
cp env.example .env

# 3. 运行安装脚本
chmod +x install.sh
./install.sh

# 4. 启动服务
chmod +x start.sh
./start.sh
```

### 🐳 Docker 部署 / Docker Deployment

```bash
# 快速启动
cp env.example .env
docker-compose up -d

# 检查服务状态
curl http://localhost:8000/health
```

### 🔧 手动安装 / Manual Installation

<details>
<summary>点击展开详细步骤</summary>

#### 后端设置
```bash
cd backend
pip3 install -r requirements.txt
python3 init_db.py
python3 main.py
```

#### 前端设置
```bash
cd frontend
npm install
npm start
```

</details>

---

## ⚙️ 配置管理 / Configuration

### 🎨 **网页端配置** (推荐)

1. **访问设置**: 打开 http://localhost:3000，点击右上角 ⚙️ 图标
2. **选择AI服务**: 从下拉菜单选择提供者
3. **填写配置**: 输入API密钥等信息
4. **测试连接**: 验证配置有效性
5. **保存应用**: 一键保存并应用新配置

![设置界面预览](docs/images/settings-preview.png)

### 📝 **环境变量配置**

<details>
<summary>点击查看完整配置选项</summary>

#### 基础配置
```env
# AI服务选择
AI_SERVICE=deepseek  # deepseek, siliconflow, local, openai_compatible
DEFAULT_AI_MODEL=deepseek-chat

# 服务器配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 数据库配置
DATABASE_URL=sqlite:///./ctf_analyzer.db

# 性能配置
DEBUG=False
LOG_LEVEL=INFO
REQUEST_TIMEOUT=60
MAX_FILE_SIZE=10485760
ENABLE_CACHE=True
CACHE_TTL=3600
```

#### DeepSeek配置
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_MODEL=deepseek-chat
```

#### 硅基流动配置
```env
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
SILICONFLOW_API_URL=https://api.siliconflow.cn/v1/chat/completions
SILICONFLOW_MODEL=Qwen/QwQ-32B
```

#### 本地模型配置
```env
LOCAL_MODEL_PATH=/path/to/local/model
LOCAL_MODEL_TYPE=auto
LOCAL_MODEL_DEVICE=auto  # auto, cpu, cuda
LOCAL_MODEL_MAX_LENGTH=4096
LOCAL_MODEL_TEMPERATURE=0.7
```

#### OpenAI兼容API配置
```env
OPENAI_COMPATIBLE_API_URL=http://localhost:8000/v1/chat/completions
OPENAI_COMPATIBLE_API_KEY=sk-your-key-here
OPENAI_COMPATIBLE_MODEL=gpt-3.5-turbo
```

</details>

---

## 📚 使用指南 / Usage Guide

### 🎯 **题目分析流程**

1. **输入题目**: 在主页面输入题目描述或上传文件
2. **AI分析**: 系统自动识别题型并调用AI进行分析
3. **获取建议**: 查看解题思路、工具推荐和学习资源
4. **记录历史**: 所有分析记录自动保存，支持历史查询

### 📊 **功能导航**

| 页面 | 功能 | 描述 |
|------|------|------|
| 🏠 **题目分析** | 主要功能 | AI驱动的题目分析和解题指导 |
| 📝 **历史记录** | 记录管理 | 查看和管理分析历史 |
| 📈 **统计信息** | 数据分析 | 题目类型分布和使用统计 |
| ⚡ **性能监控** | 系统监控 | AI服务性能和缓存状态 |
| ⚙️ **设置管理** | 配置管理 | AI服务配置和连接测试 |

### 🛠️ **支持的AI服务**

| 服务商 | 类型 | 特点 | 适用场景 |
|--------|------|------|----------|
| 🤖 **DeepSeek** | 在线API | 高质量推理，中英文支持 | 日常分析，快速响应 |
| 🧠 **硅基流动** | 在线API | 多模型支持，性价比高 | 批量分析，成本控制 |
| 💻 **本地模型** | 本地部署 | 数据私密，可定制化 | 离线环境，隐私保护 |
| 🔗 **OpenAI兼容** | 兼容API | 标准接口，易于扩展 | 第三方服务，灵活接入 |

---

## 🔍 API文档 / API Documentation

### 📡 **主要端点**

| 端点 | 方法 | 功能 | 说明 |
|------|------|------|------|
| `/api/analyze` | POST | 题目分析 | 主要分析功能 |
| `/api/settings` | GET/POST | 配置管理 | 获取/更新配置 |
| `/api/test-connection` | POST | 连接测试 | 测试AI服务连接 |
| `/api/history` | GET | 历史记录 | 获取分析历史 |
| `/api/stats` | GET | 统计信息 | 获取使用统计 |
| `/health` | GET | 健康检查 | 系统状态监控 |

### 📖 **详细文档**

启动服务后访问: http://localhost:8000/docs

---

## 📈 监控和调试 / Monitoring & Debugging

### 🏥 **健康检查**

```bash
# 检查服务状态
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "database": "healthy", 
  "ai_provider": "deepseek",
  "cache_enabled": true,
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### 📊 **性能监控**

访问性能监控页面查看：
- AI服务响应时间
- 缓存命中率
- 请求成功率
- 系统资源使用

### 📝 **日志系统**

```bash
# 查看应用日志
tail -f backend/logs/app.log

# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 🧪 测试和验证 / Testing & Validation

### ✅ **功能测试**

```bash
# 测试AI提供者配置
cd backend
python3 test_ai_providers.py

# 测试本地模型（如果使用）
python3 test_local_models.py

# 测试API端点
curl -X POST http://localhost:8000/api/analyze \
  -F "text=这是一个简单的CTF题目测试"
```

### 🔧 **故障排除**

<details>
<summary>常见问题解决方案</summary>

#### Q: 前端无法访问？
```bash
# 检查前端服务
ps aux | grep react-scripts
curl http://localhost:3000/

# 重启前端
cd frontend && npm start
```

#### Q: 后端API错误？
```bash
# 检查后端服务
ps aux | grep main.py
curl http://localhost:8000/health

# 查看详细日志
tail -f backend/logs/app.log
```

#### Q: AI服务连接失败？
1. 检查API密钥是否正确
2. 验证网络连接
3. 使用网页端设置测试连接
4. 查看错误日志获取详细信息

#### Q: 数据库错误？
```bash
# 重新初始化数据库
cd backend
python3 init_db.py
```

</details>

---

## 🤝 贡献指南 / Contributing

我们欢迎各种形式的贡献！

### 📝 **贡献方式**
- 🐛 报告Bug
- 💡 提出新功能
- 📖 改进文档
- 🔧 代码贡献

### 🔄 **开发流程**
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

---

## 📄 文档目录 / Documentation

- 📋 [**SETTINGS_GUIDE.md**](SETTINGS_GUIDE.md) - 设置功能详细指南
- 📖 [**API文档**](http://localhost:8000/docs) - 完整的API参考
- 🔧 [**部署指南**](#-docker-部署--docker-deployment) - Docker部署说明
- 🛠️ [**故障排除**](#-故障排除) - 常见问题解决

---

## 📄 许可证 / License

本项目采用 [Apache License 2.0](LICENSE) 许可证。

---

## 🙏 致谢 / Acknowledgments

感谢以下开源项目和服务提供商：

- [React](https://reactjs.org/) - 前端框架
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Material-UI](https://mui.com/) - UI组件库
- [DeepSeek](https://deepseek.com/) - AI服务提供商
- [硅基流动](https://siliconflow.cn/) - AI服务提供商

---

## 📞 支持与反馈 / Support & Feedback

- 🐛 **Bug报告**: [GitHub Issues](https://github.com/your-repo/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 **联系我们**: your-email@example.com

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个星星！**

**⭐ If this project helps you, please give us a star!**

Made with ❤️ by CTF Community

</div>

