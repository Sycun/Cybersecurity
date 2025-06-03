#!/bin/bash

echo "🚀 开始安装CTF智能分析平台..."

# 检查是否安装了Node.js和Python
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 询问用户是否需要安装本地模型支持
echo ""
echo "📋 选择AI提供者类型："
echo "1) 在线API（DeepSeek/硅基流动）- 推荐"
echo "2) 本地模型 - 需要更多依赖和计算资源"
echo "3) 全部安装"
read -p "请选择 (1-3，默认为1): " choice
choice=${choice:-1}

# 安装后端依赖
echo "📦 安装后端基础依赖..."
cd backend
pip3 install -r requirements.txt --no-deps || {
    echo "⚠️ 尝试安装基础依赖（不含本地模型支持）..."
    # 创建临时的基础requirements文件
    cat > requirements_basic.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.2
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
aiofiles==23.2.1
jinja2==3.1.2
EOF
    pip3 install -r requirements_basic.txt
}

# 根据用户选择安装本地模型依赖
if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    echo "🤖 安装本地模型支持依赖..."
    echo "⚠️ 注意：这可能需要几分钟时间，尤其是PyTorch..."
    
    # 检查CUDA可用性
    if command -v nvidia-smi &> /dev/null; then
        echo "🎮 检测到NVIDIA GPU，安装CUDA版本PyTorch..."
        pip3 install torch transformers accelerate sentencepiece --index-url https://download.pytorch.org/whl/cu118
    else
        echo "💻 未检测到NVIDIA GPU，安装CPU版本PyTorch..."
        pip3 install torch transformers accelerate sentencepiece --index-url https://download.pytorch.org/whl/cpu
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ 本地模型支持依赖安装成功"
    else
        echo "⚠️ 本地模型依赖安装失败，你仍可以使用在线API"
        echo "💡 可稍后手动安装：pip install torch transformers accelerate sentencepiece"
    fi
fi

if [ $? -eq 0 ]; then
    echo "✅ 后端依赖安装成功"
else
    echo "❌ 后端依赖安装失败"
    exit 1
fi

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 init_db.py
if [ $? -eq 0 ]; then
    echo "✅ 数据库初始化成功"
else
    echo "❌ 数据库初始化失败"
fi

cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo "✅ 前端依赖安装成功"
else
    echo "❌ 前端依赖安装失败"
    exit 1
fi

cd ..

echo "🎉 安装完成！"
echo ""
echo "📋 下一步配置："
echo "1. 复制 .env.example 到 .env：cp .env.example .env"
echo "2. 编辑 .env 文件，配置你的AI提供者："

if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    echo "   📡 在线API配置："
    echo "      - DEEPSEEK_API_KEY=your_api_key_here"
    echo "      - 或 SILICONFLOW_API_KEY=your_api_key_here"
fi

if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    echo "   🖥️ 本地模型配置："
    echo "      - AI_SERVICE=local"
    echo "      - LOCAL_MODEL_PATH=/path/to/your/model"
    echo "   💡 推荐模型："
    echo "      - ChatGLM3-6B (适合6GB+ GPU)"
    echo "      - Qwen-7B-Chat (适合8GB+ GPU)"
    echo "      - 下载地址：https://huggingface.co/ 或 https://modelscope.cn/"
fi

echo ""
echo "📝 验证安装："
echo "   启动服务后访问 http://localhost:3000"
echo "   在设置页面测试AI服务连接"

echo ""
echo "🚀 启动服务："
echo "   方式1: ./start.sh"
echo "   方式2: docker-compose up -d"
echo ""
echo "🌐 访问地址: http://localhost:3000" 