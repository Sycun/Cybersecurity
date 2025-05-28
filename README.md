# CTF智能分析平台 / CTF Intelligent Analysis Platform

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## 项目简介 / Introduction

本项目是一个支持多AI提供者的 CTF（Capture The Flag）题目智能分析平台，旨在帮助 CTF 学习者和参赛者高效分析和解答各类题目。平台支持 Web、Pwn、Reverse、Crypto、Misc 等所有主流 CTF 题型，集成 AI 解题思路、工具推荐、学习资源和比赛模式等功能。目前支持 DeepSeek 和硅基流动两个AI提供者。

This project is a multi-AI provider CTF (Capture The Flag) challenge analysis platform that helps CTF learners and players efficiently analyze and solve various types of challenges. It supports Web, Pwn, Reverse, Crypto, and Misc categories, integrating AI-driven solutions, tool recommendations, learning resources, and competition mode. Currently supports DeepSeek and SiliconFlow AI providers.

---

## 功能特性 / Features

- 🔍 智能题目分析（AI-powered challenge analysis）
- 🤖 多AI提供者支持（Multiple AI providers support）
  - DeepSeek API 集成
  - 硅基流动 API 集成
- 🛠️ 常用CTF工具命令推荐（CTF tool command suggestions）
- 📚 学习资源与Writeup推荐（Learning resources & writeups）
- ⏱️ 比赛模式与解题记录（Competition mode & solution records）
- 📁 支持文本、代码和文件上传分析（Text, code, and file upload support）
- 🔄 动态切换AI提供者（Dynamic AI provider switching）

---

## 技术栈 / Tech Stack

### 前端 / Frontend

- React 18 + TypeScript
- Material-UI (MUI)
- Axios

### 后端 / Backend

- FastAPI
- SQLAlchemy + SQLite
- DeepSeek API
- Python 3.8+

### 部署 / Deployment

- Docker & Docker Compose

---

## 快速开始 / Quick Start

### 前置要求 / Prerequisites

- Node.js 16+ & npm
- Python 3.8+
- AI API Key (DeepSeek 或 硅基流动)

### 一键安装 / One-click Install

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写你的 AI API 密钥（DeepSeek 或 硅基流动）

# 2. 运行安装脚本
chmod +x install.sh
./install.sh

# 3. 启动服务
chmod +x start.sh
./start.sh
```

### Docker 部署 / Docker Deployment

```bash
cp .env.example .env
# 编辑 .env 文件，填写你的 DeepSeek API 密钥

docker-compose up -d
```

### 手动安装 / Manual Installation

#### 后端 / Backend

```bash
cd backend
pip3 install -r requirements.txt
python3 init_db.py
python3 main.py
```

#### 前端 / Frontend

```bash
cd frontend
npm install
npm start
```

---

## 环境变量 / Environment Variables

请在根目录创建 `.env` 文件，参考 `.env.example`，配置如下变量：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DATABASE_URL=sqlite:///./ctf_analyzer.db
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 使用说明 / Usage

1. 访问 [http://localhost:3000](http://localhost:3000) 打开前端界面
2. 输入题目描述或上传相关文件
3. 系统自动识别题目类型并调用 AI 分析
4. 查看分析结果、工具推荐和解题建议
5. 使用推荐的工具命令进行实际操作

---

## 支持的题目类型 / Supported Challenge Types

- **Web**: SQL 注入、XSS、CSRF、文件上传等
- **Pwn**: 缓冲区溢出、ROP 链、堆漏洞等
- **Reverse**: 逆向工程、脱壳、算法分析等
- **Crypto**: 密码学、RSA、AES、哈希碰撞等
- **Misc**: 隐写术、编码解码、取证分析等

---

## 目录结构 / Project Structure

```
Cybersecurity/
├── backend/         # FastAPI 后端服务
├── frontend/        # React 前端项目
├── install.sh       # 一键安装脚本
├── start.sh         # 一键启动脚本
├── docker-compose.yml
├── env.example      # 环境变量示例
├── .gitignore
├── LICENSE
└── README.md
```

---

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request 来改进本项目！  
Feel free to submit Issues and Pull Requests to improve this project!

---

## 许可证 / License

Apache License 2.0.  
See [LICENSE](LICENSE) for details.

---

如需进一步补充（如API接口文档、前端页面截图等），请告知！

