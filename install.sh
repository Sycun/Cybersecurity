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

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
pip3 install -r requirements.txt
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
echo "📋 使用说明："
echo "1. 复制 .env.example 到 .env 并配置你的 DeepSeek API 密钥"
echo "2. 启动后端: cd backend && python3 main.py"
echo "3. 启动前端: cd frontend && npm start"
echo "4. 或者使用 Docker: docker-compose up -d"
echo ""
echo "🌐 访问地址: http://localhost:3000" 