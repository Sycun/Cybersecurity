#!/bin/bash

# =============================================================================
# CTF智能分析平台启动脚本
# =============================================================================

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查环境变量文件
check_env_file() {
    if [ ! -f ".env" ]; then
        log_warning "未找到 .env 文件，正在从 .env.example 复制..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_success "已创建 .env 文件，请编辑配置后重新运行"
            log_info "请编辑 .env 文件，配置您的API密钥和其他设置"
            exit 1
        else
            log_error "未找到 .env.example 文件"
            exit 1
        fi
    fi
}

# 加载环境变量
load_env() {
    log_info "加载环境变量..."
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
        log_success "环境变量加载完成"
    else
        log_error "未找到 .env 文件"
        exit 1
    fi
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        log_error "npm 未安装"
        exit 1
    fi
    
    log_success "系统依赖检查完成"
}

# 检查端口占用
check_ports() {
    log_info "检查端口占用..."
    
    # 检查后端端口
    if lsof -Pi :${BACKEND_PORT:-8000} -sTCP:LISTEN -t >/dev/null ; then
        log_warning "后端端口 ${BACKEND_PORT:-8000} 已被占用"
        read -p "是否继续启动？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # 检查前端端口
    if lsof -Pi :${FRONTEND_PORT:-3000} -sTCP:LISTEN -t >/dev/null ; then
        log_warning "前端端口 ${FRONTEND_PORT:-3000} 已被占用"
        read -p "是否继续启动？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log_success "端口检查完成"
}

# 启动后端服务
start_backend() {
    log_info "启动后端服务..."
    
    cd backend
    
    # 检查Python依赖
    if [ ! -d "venv" ]; then
        log_info "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 安装依赖
    log_info "安装Python依赖..."
    pip install -r requirements.txt
    
    # 创建必要目录
    mkdir -p logs
    mkdir -p uploads
    mkdir -p backups
    
    # 启动后端服务
    log_info "启动后端服务 (端口: ${BACKEND_PORT:-8000})..."
    python3 main.py &
    BACKEND_PID=$!
    
    cd ..
    
    # 等待后端启动
    sleep 3
    
    # 检查后端是否启动成功
    if curl -s http://localhost:${BACKEND_PORT:-8000}/health > /dev/null; then
        log_success "后端服务启动成功"
    else
        log_error "后端服务启动失败"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
}

# 启动前端服务
start_frontend() {
    log_info "启动前端服务..."
    
    cd frontend
    
    # 检查Node.js依赖
    if [ ! -d "node_modules" ]; then
        log_info "安装Node.js依赖..."
        npm install
    fi
    
    # 设置环境变量
    export REACT_APP_API_URL=http://localhost:${BACKEND_PORT:-8000}
    export REACT_APP_BACKEND_URL=http://localhost:${BACKEND_PORT:-8000}
    export REACT_APP_API_TIMEOUT=${REQUEST_TIMEOUT:-60000}
    
    # 启动前端服务
    log_info "启动前端服务 (端口: ${FRONTEND_PORT:-3000})..."
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    
    # 等待前端启动
    sleep 5
    
    # 检查前端是否启动成功
    if curl -s http://localhost:${FRONTEND_PORT:-3000} > /dev/null; then
        log_success "前端服务启动成功"
    else
        log_warning "前端服务可能还在启动中，请稍后访问"
    fi
}

# 显示服务信息
show_service_info() {
    echo
    log_success "CTF智能分析平台启动完成！"
    echo
    echo "服务信息："
    echo "  后端API: http://localhost:${BACKEND_PORT:-8000}"
    echo "  前端界面: http://localhost:${FRONTEND_PORT:-3000}"
    echo "  API文档: http://localhost:${BACKEND_PORT:-8000}/docs"
    echo "  健康检查: http://localhost:${BACKEND_PORT:-8000}/health"
    echo
    echo "配置信息："
    echo "  AI服务: ${AI_SERVICE:-deepseek}"
    echo "  调试模式: ${DEBUG:-false}"
    echo "  缓存: ${ENABLE_CACHE:-true}"
    echo "  监控: ${ENABLE_MONITORING:-true}"
    echo
    echo "按 Ctrl+C 停止服务"
    echo
}

# 清理函数
cleanup() {
    log_info "正在停止服务..."
    
    # 停止后端
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        log_info "后端服务已停止"
    fi
    
    # 停止前端
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        log_info "前端服务已停止"
    fi
    
    log_success "所有服务已停止"
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    echo "=============================================================================="
    echo "                    CTF智能分析平台启动脚本"
    echo "=============================================================================="
    echo
    
    # 检查环境变量文件
    check_env_file
    
    # 加载环境变量
    load_env
    
    # 检查依赖
    check_dependencies
    
    # 检查端口占用
    check_ports
    
    # 启动后端服务
    start_backend
    
    # 启动前端服务
    start_frontend
    
    # 显示服务信息
    show_service_info
    
    # 等待用户中断
    wait
}

# 运行主函数
main "$@" 