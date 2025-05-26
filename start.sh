#!/bin/bash

echo "🚀 启动CTF智能分析平台..."

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️ 未找到 .env 文件，请先复制 .env.example 到 .env 并配置"
    exit 1
fi

# 启动后端服务
echo "🔧 启动后端服务..."
cd backend
python3 main.py &
BACKEND_PID=$!
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"

cd ..

# 等待后端启动
sleep 3

# 启动前端服务
echo "🎨 启动前端服务..."
cd frontend
npm start &
FRONTEND_PID=$!
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"

cd ..

echo "🎉 服务启动完成！"
echo "🌐 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 