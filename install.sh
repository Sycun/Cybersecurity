#!/bin/bash

# =============================================================================
# CTF智能分析平台安装脚本
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

# 检查系统要求
check_system_requirements() {
    log_info "检查系统要求..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "检测到 Linux 系统"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "检测到 macOS 系统"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        log_info "检测到 Windows 系统 (Git Bash/Cygwin)"
    else
        log_warning "未知操作系统: $OSTYPE"
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_info "Python版本: $PYTHON_VERSION"
        
        # 检查Python版本是否满足要求
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
            log_success "Python版本满足要求 (>= 3.8)"
        else
            log_error "Python版本过低，需要 3.8 或更高版本"
            exit 1
        fi
    else
        log_error "Python3 未安装"
        exit 1
    fi
    
    # 检查Node.js版本
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_info "Node.js版本: $NODE_VERSION"
        
        # 检查Node.js版本是否满足要求
        if node -e "const v = process.version; const major = parseInt(v.slice(1).split('.')[0]); exit(major >= 16 ? 0 : 1)" 2>/dev/null; then
            log_success "Node.js版本满足要求 (>= 16)"
        else
            log_error "Node.js版本过低，需要 16 或更高版本"
            exit 1
        fi
    else
        log_error "Node.js 未安装"
        exit 1
    fi
    
    # 检查npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        log_info "npm版本: $NPM_VERSION"
    else
        log_error "npm 未安装"
        exit 1
    fi
    
    # 检查Git
    if command -v git &> /dev/null; then
        log_success "Git 已安装"
    else
        log_warning "Git 未安装，某些功能可能受限"
    fi
    
    log_success "系统要求检查完成"
}

# 创建环境变量文件
setup_env_file() {
    log_info "设置环境变量文件..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_success "已创建 .env 文件"
            log_warning "请编辑 .env 文件，配置您的API密钥和其他设置"
        else
            log_error "未找到 .env.example 文件"
            exit 1
        fi
    else
        log_info ".env 文件已存在"
    fi
}

# 安装Python依赖
install_python_dependencies() {
    log_info "安装Python依赖..."
    
    cd backend
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    log_info "升级pip..."
    pip install --upgrade pip
    
    # 安装依赖
    log_info "安装Python依赖包..."
    pip install -r requirements.txt
    
    # 创建必要目录
    mkdir -p logs
    mkdir -p uploads
    mkdir -p backups
    mkdir -p static
    
    cd ..
    
    log_success "Python依赖安装完成"
}

# 安装Node.js依赖
install_node_dependencies() {
    log_info "安装Node.js依赖..."
    
    cd frontend
    
    # 检查package.json是否存在
    if [ ! -f "package.json" ]; then
        log_error "未找到 package.json 文件"
        exit 1
    fi
    
    # 安装依赖
    log_info "安装Node.js依赖包..."
    npm install
    
    cd ..
    
    log_success "Node.js依赖安装完成"
}

# 初始化数据库
initialize_database() {
    log_info "初始化数据库..."
    
    cd backend
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 运行数据库初始化脚本
    if [ -f "init_db.py" ]; then
        log_info "运行数据库初始化脚本..."
        python3 init_db.py
    else
        log_info "创建数据库表..."
        python3 -c "
from database import engine, Base
Base.metadata.create_all(bind=engine)
print('数据库表创建完成')
"
    fi
    
    cd ..
    
    log_success "数据库初始化完成"
}

# 设置权限
setup_permissions() {
    log_info "设置文件权限..."
    
    # 设置脚本执行权限
    chmod +x start.sh
    chmod +x install.sh
    
    # 设置目录权限
    chmod 755 backend/logs
    chmod 755 backend/uploads
    chmod 755 backend/backups
    
    log_success "权限设置完成"
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    # 检查后端依赖
    cd backend
    source venv/bin/activate
    
    # 检查关键Python包
    python3 -c "
import fastapi
import uvicorn
import sqlalchemy
import httpx
import dotenv
print('后端依赖验证通过')
"
    
    cd ..
    
    # 检查前端依赖
    cd frontend
    
    # 检查关键Node.js包
    if [ -d "node_modules/react" ] && [ -d "node_modules/@mui/material" ]; then
        log_success "前端依赖验证通过"
    else
        log_error "前端依赖验证失败"
        exit 1
    fi
    
    cd ..
    
    log_success "安装验证完成"
}

# 显示安装完成信息
show_completion_info() {
    echo
    log_success "CTF智能分析平台安装完成！"
    echo
    echo "下一步操作："
    echo "1. 编辑 .env 文件，配置您的API密钥和其他设置"
    echo "2. 运行 ./start.sh 启动服务"
    echo
    echo "配置说明："
    echo "  - AI_SERVICE: 选择AI服务提供者 (deepseek, siliconflow, local, openai_compatible)"
    echo "  - DEEPSEEK_API_KEY: DeepSeek API密钥"
    echo "  - SILICONFLOW_API_KEY: 硅基流动API密钥"
    echo "  - BACKEND_PORT: 后端服务端口 (默认: 8000)"
    echo "  - FRONTEND_PORT: 前端服务端口 (默认: 3000)"
    echo
    echo "服务地址："
    echo "  - 前端界面: http://localhost:${FRONTEND_PORT:-3000}"
    echo "  - 后端API: http://localhost:${BACKEND_PORT:-8000}"
    echo "  - API文档: http://localhost:${BACKEND_PORT:-8000}/docs"
    echo
    echo "更多信息请查看 README.md 文件"
    echo
}

# 主函数
main() {
    echo "=============================================================================="
    echo "                CTF智能分析平台安装脚本"
    echo "=============================================================================="
    echo
    
    # 检查系统要求
    check_system_requirements
    
    # 设置环境变量文件
    setup_env_file
    
    # 安装Python依赖
    install_python_dependencies
    
    # 安装Node.js依赖
    install_node_dependencies
    
    # 初始化数据库
    initialize_database
    
    # 设置权限
    setup_permissions
    
    # 验证安装
    verify_installation
    
    # 显示完成信息
    show_completion_info
}

# 运行主函数
main "$@" 