# 本地AI模型部署指南

本指南将帮助您在CTF智能分析平台中配置和使用本地AI模型。

## 目录
- [系统要求](#系统要求)
- [支持的模型](#支持的模型)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [性能优化](#性能优化)
- [故障排除](#故障排除)
- [OpenAI兼容API](#openai兼容api)

## 系统要求

### 最低要求
- **CPU**: 4核心以上
- **内存**: 8GB以上
- **存储**: 20GB可用空间
- **Python**: 3.8+

### 推荐配置
- **CPU**: 8核心以上
- **内存**: 16GB以上（GPU模式）/ 32GB以上（CPU模式）
- **GPU**: NVIDIA GPU with 6GB+ VRAM
- **存储**: 50GB+ SSD

### GPU支持
- NVIDIA GPU（推荐）
- CUDA 11.8 或更高版本
- cuDNN 8.0+

## 支持的模型

### 推荐模型

| 模型名称 | 模型大小 | 内存需求 | 适用场景 | 下载链接 |
|---------|---------|----------|---------|----------|
| ChatGLM3-6B | 6B | 6GB+ GPU / 12GB+ CPU | 平衡性能和资源 | [HuggingFace](https://huggingface.co/THUDM/chatglm3-6b) |
| Qwen-7B-Chat | 7B | 8GB+ GPU / 16GB+ CPU | 更好的中文理解 | [HuggingFace](https://huggingface.co/Qwen/Qwen-7B-Chat) |
| Baichuan2-7B-Chat | 7B | 8GB+ GPU / 16GB+ CPU | 优秀的代码能力 | [HuggingFace](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat) |
| CodeLlama-7B | 7B | 8GB+ GPU / 16GB+ CPU | 专门的代码模型 | [HuggingFace](https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf) |

### 量化模型（节省内存）
- 使用INT4/INT8量化可将内存需求减少50-75%
- 推荐GPTQ或AWQ量化版本

## 安装步骤

### 1. 安装依赖

```bash
# 基础依赖
pip install torch transformers accelerate sentencepiece

# GPU支持（如果有NVIDIA GPU）
pip install torch --index-url https://download.pytorch.org/whl/cu118

# 可选：量化支持
pip install auto-gptq optimum
```

### 2. 下载模型

#### 方法1：使用Hugging Face

```bash
# 使用git-lfs下载
git lfs clone https://huggingface.co/THUDM/chatglm3-6b ./models/chatglm3-6b

# 或使用Python代码下载
python -c "
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('THUDM/chatglm3-6b', cache_dir='./models')
model = AutoModel.from_pretrained('THUDM/chatglm3-6b', cache_dir='./models')
"
```

#### 方法2：使用ModelScope（国内用户推荐）

```bash
pip install modelscope

# 下载模型
python -c "
from modelscope import snapshot_download
snapshot_download('ZhipuAI/chatglm3-6b', cache_dir='./models')
"
```

### 3. 配置环境变量

编辑 `.env` 文件：

```env
# 启用本地模型
AI_SERVICE=local

# 模型路径配置
LOCAL_MODEL_PATH=./models/chatglm3-6b
LOCAL_MODEL_TYPE=auto
LOCAL_MODEL_DEVICE=auto  # auto, cpu, cuda

# 性能参数
LOCAL_MODEL_MAX_LENGTH=4096
LOCAL_MODEL_TEMPERATURE=0.7
```

### 4. 测试配置

```bash
cd backend
python3 test_local_models.py
```

## 配置说明

### 环境变量详解

| 变量名 | 说明 | 可选值 | 默认值 |
|--------|------|--------|--------|
| `LOCAL_MODEL_PATH` | 模型文件路径 | 绝对或相对路径 | 必须设置 |
| `LOCAL_MODEL_TYPE` | 模型类型 | auto, chatglm, qwen, baichuan | auto |
| `LOCAL_MODEL_DEVICE` | 计算设备 | auto, cpu, cuda | auto |
| `LOCAL_MODEL_MAX_LENGTH` | 最大生成长度 | 1024-8192 | 4096 |
| `LOCAL_MODEL_TEMPERATURE` | 生成温度 | 0.1-2.0 | 0.7 |

### 设备选择策略

- `auto`: 自动检测，优先使用GPU
- `cpu`: 强制使用CPU（内存需求大但兼容性好）
- `cuda`: 强制使用GPU（需要NVIDIA GPU和CUDA）

## 性能优化

### 1. GPU优化

```env
# 启用GPU
LOCAL_MODEL_DEVICE=cuda

# 使用混合精度
# 在代码中自动启用torch.float16
```

### 2. 内存优化

```env
# 减少最大长度
LOCAL_MODEL_MAX_LENGTH=2048

# 使用量化模型
LOCAL_MODEL_PATH=./models/chatglm3-6b-int4
```

### 3. 推理优化

```python
# 在生成时使用更高效的参数
generation_config = {
    "do_sample": True,
    "top_k": 50,
    "top_p": 0.9,
    "temperature": 0.7,
    "max_new_tokens": 2048,
    "repetition_penalty": 1.1
}
```

## 故障排除

### 常见问题

#### 1. 内存不足 (CUDA out of memory)

**解决方案**:
```bash
# 使用CPU模式
LOCAL_MODEL_DEVICE=cpu

# 或减少最大长度
LOCAL_MODEL_MAX_LENGTH=1024

# 或使用量化模型
pip install auto-gptq
# 下载INT4量化版本
```

#### 2. 模型加载失败

**检查清单**:
- [ ] 模型路径正确
- [ ] 模型文件完整
- [ ] Python依赖已安装
- [ ] 足够的可用内存

```bash
# 检查模型文件
ls -la ./models/chatglm3-6b/

# 检查Python依赖
python -c "import torch, transformers; print('Dependencies OK')"

# 检查GPU可用性
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### 3. 生成结果质量差

**优化建议**:
```env
# 调整温度参数
LOCAL_MODEL_TEMPERATURE=0.3  # 更保守的生成

# 或
LOCAL_MODEL_TEMPERATURE=1.0  # 更创新的生成
```

#### 4. 推理速度慢

**解决方案**:
- 使用GPU：`LOCAL_MODEL_DEVICE=cuda`
- 减少生成长度：`LOCAL_MODEL_MAX_LENGTH=2048`
- 使用更小的模型
- 考虑使用vLLM等推理框架

### 调试命令

```bash
# 检查系统信息
nvidia-smi  # GPU信息
free -h     # 内存使用
df -h       # 磁盘空间

# 检查Python环境
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"

# 测试模型加载
python -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('$LOCAL_MODEL_PATH')
print('Tokenizer loaded successfully')
"
```

## OpenAI兼容API

除了直接加载本地模型，您还可以使用OpenAI兼容的API服务。

### 推荐服务

#### 1. vLLM
```bash
# 安装vLLM
pip install vllm

# 启动API服务
python -m vllm.entrypoints.openai.api_server \
    --model ./models/chatglm3-6b \
    --host 0.0.0.0 \
    --port 8000
```

#### 2. FastChat
```bash
# 安装FastChat
pip install fschat

# 启动API服务
python -m fastchat.serve.openai_api_server \
    --model-path ./models/chatglm3-6b \
    --host 0.0.0.0 \
    --port 8000
```

#### 3. Text Generation WebUI
```bash
# 克隆项目
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui

# 安装依赖
pip install -r requirements.txt

# 启动API模式
python server.py --api --model ./models/chatglm3-6b
```

### 配置OpenAI兼容API

```env
# 使用OpenAI兼容API
AI_SERVICE=openai_compatible

# API配置
OPENAI_COMPATIBLE_API_URL=http://localhost:8000/v1/chat/completions
OPENAI_COMPATIBLE_API_KEY=sk-no-key-required
OPENAI_COMPATIBLE_MODEL=chatglm3-6b
```

### 优势对比

| 方式 | 优势 | 劣势 |
|------|------|------|
| 直接加载 | 简单配置，集成度高 | 内存占用持续，启动慢 |
| vLLM | 高性能推理，支持并发 | 配置复杂，额外服务 |
| FastChat | 完整功能，Web界面 | 资源占用较高 |
| WebUI | 图形界面，功能丰富 | 主要面向交互使用 |

## 最佳实践

### 1. 开发环境
- 使用小模型或量化模型
- CPU模式进行开发测试
- 使用较短的max_length

### 2. 生产环境
- 使用GPU加速
- 配置适当的模型大小
- 监控内存和GPU使用率
- 设置合理的超时时间

### 3. 安全考虑
- 本地模型确保数据隐私
- 定期更新模型版本
- 监控生成内容质量

## 相关资源

- [Hugging Face模型库](https://huggingface.co/models)
- [ModelScope模型库](https://modelscope.cn/)
- [PyTorch官方文档](https://pytorch.org/docs/)
- [Transformers库文档](https://huggingface.co/docs/transformers/)
- [vLLM项目](https://github.com/vllm-project/vllm)
- [FastChat项目](https://github.com/lm-sys/FastChat)

---

如有其他问题，请参考项目README或提交Issue。 