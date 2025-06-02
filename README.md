# CTF智能分析平台 / CTF Intelligent Analysis Platform

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## 项目简介 / Introduction

本项目是一个支持多AI提供者的 CTF（Capture The Flag）题目智能分析平台，旨在帮助 CTF 学习者和参赛者高效分析和解答各类题目。平台支持 Web、Pwn、Reverse、Crypto、Misc 等所有主流 CTF 题型，集成 AI 解题思路、工具推荐、学习资源和比赛模式等功能。支持 DeepSeek、硅基流动、本地部署模型和OpenAI兼容API等多种AI提供者。

This project is a multi-AI provider CTF (Capture The Flag) challenge analysis platform that helps CTF learners and players efficiently analyze and solve various types of challenges. It supports Web, Pwn, Reverse, Crypto, and Misc categories, integrating AI-driven solutions, tool recommendations, learning resources, and competition mode. Supports DeepSeek, SiliconFlow, local deployed models, and OpenAI-compatible APIs.

---

## 功能特性 / Features

- 🔍 智能题目分析（AI-powered challenge analysis）
- 🤖 多AI提供者支持（Multiple AI providers support）
  - DeepSeek API 集成
  - 硅基流动 API 集成
  - **本地部署模型支持（Local model support）**
  - **OpenAI兼容API支持（OpenAI-compatible API support）**
- 🛠️ 常用CTF工具命令推荐（CTF tool command suggestions）
- 📚 学习资源与Writeup推荐（Learning resources & writeups）
- ⏱️ 比赛模式与解题记录（Competition mode & solution records）
- 📁 支持文本、代码和文件上传分析（Text, code, and file upload support）
- 🔄 动态切换AI提供者（Dynamic AI provider switching）
- 🖥️ **本地私有化部署（Local private deployment）**

---

## 技术栈 / Tech Stack

### 前端 / Frontend

- React 18 + TypeScript
- Material-UI (MUI)
- Axios

### 后端 / Backend

- FastAPI
- SQLAlchemy + SQLite
- DeepSeek API / 硅基流动 API
- **本地AI模型支持（transformers + torch）**
- Python 3.8+

### 部署 / Deployment

- Docker & Docker Compose

---

## 快速开始 / Quick Start

### 前置要求 / Prerequisites

- Node.js 16+ & npm
- Python 3.8+
- AI API Key (DeepSeek 或 硅基流动) **或本地AI模型**

### 本地模型支持 / Local Model Support

如果你想使用本地部署的AI模型，请先安装相关依赖：

```bash
# 安装本地模型支持（可选）
pip install torch transformers accelerate sentencepiece
```

推荐的本地模型：
- **ChatGLM3-6B**: 适合中等配置机器
- **Qwen-7B-Chat**: 性能较好的中文模型  
- **Baichuan2-7B-Chat**: 另一个优秀的中文模型

### 一键安装 / One-click Install

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置AI提供者：
# - 在线API：填写 DeepSeek 或硅基流动 API 密钥
# - 本地模型：设置 AI_SERVICE=local 并配置 LOCAL_MODEL_PATH
# - OpenAI兼容：设置 AI_SERVICE=openai_compatible 并配置相关参数

# 2. 运行安装脚本
chmod +x install.sh
./install.sh

# 3. 测试本地模型（可选）
cd backend
python3 test_local_models.py

# 4. 启动服务
chmod +x start.sh
./start.sh
```

### Docker 部署 / Docker Deployment

```bash
cp .env.example .env
# 编辑 .env 文件，配置你的AI提供者

docker-compose up -d
```

### 手动安装 / Manual Installation

#### 后端 / Backend

```bash
cd backend
pip3 install -r requirements.txt
python3 init_db.py

# 测试AI提供者配置（可选）
python3 test_ai_providers.py
python3 test_local_models.py

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

### 基础配置
```env
# AI服务选择
AI_SERVICE=deepseek  # deepseek, siliconflow, local, openai_compatible

# 数据库和服务器配置
DATABASE_URL=sqlite:///./ctf_analyzer.db
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### DeepSeek配置
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

### 硅基流动配置
```env
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
SILICONFLOW_API_URL=https://api.siliconflow.cn/v1/chat/completions
```

### 本地模型配置
```env
LOCAL_MODEL_PATH=/path/to/local/model  # 本地模型路径
LOCAL_MODEL_DEVICE=auto  # auto, cpu, cuda
LOCAL_MODEL_TEMPERATURE=0.7
```

### OpenAI兼容API配置
```env
OPENAI_COMPATIBLE_API_URL=http://localhost:8000/v1/chat/completions
OPENAI_COMPATIBLE_API_KEY=sk-your-key-here
OPENAI_COMPATIBLE_MODEL=gpt-3.5-turbo
```

---

## 使用说明 / Usage

1. 访问 [http://localhost:3000](http://localhost:3000) 打开前端界面
2. 在AI提供者下拉菜单中选择你配置的提供者
3. 输入题目描述或上传相关文件
4. 系统自动识别题目类型并调用 AI 分析
5. 查看分析结果、工具推荐和解题建议
6. 使用推荐的工具命令进行实际操作

### 本地模型使用建议 / Local Model Usage Tips

1. **性能优化**：
   - 使用GPU可显著提升推理速度
   - 量化模型可减少内存占用
   - 适当调整temperature和max_length参数

2. **模型下载**：
   - Hugging Face: https://huggingface.co/
   - ModelScope: https://modelscope.cn/

3. **OpenAI兼容服务推荐**：
   - vLLM: 高性能推理服务
   - FastChat: 多模型聊天服务
   - Text Generation WebUI: 图形界面服务

---

## 支持的AI提供者 / Supported AI Providers

| 提供者 | 类型 | 特点 | 配置难度 |
|--------|------|------|----------|
| DeepSeek | 在线API | 专业代码分析，响应快 | 简单 |
| 硅基流动 | 在线API | 模型选择丰富，价格优惠 | 简单 |
| 本地模型 | 本地部署 | 数据隐私，可自定义 | 中等 |
| OpenAI兼容 | 本地/云端API | 灵活部署，标准接口 | 中等 |

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
│   ├── ai_providers.py      # AI提供者实现
│   ├── test_local_models.py # 本地模型测试脚本
│   └── ...
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

## 故障排除 / Troubleshooting

### 本地模型问题
```bash
# 测试本地模型配置
cd backend
python3 test_local_models.py

# 检查GPU可用性
python3 -c "import torch; print(torch.cuda.is_available())"
```

### 依赖安装问题
```bash
# 安装本地模型依赖
pip install torch transformers accelerate sentencepiece

# 如果遇到CUDA版本问题，访问：
# https://pytorch.org/get-started/locally/
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

