#!/usr/bin/env python3
"""
本地AI模型测试脚本
用于测试本地模型的配置和功能
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_providers import LocalAIProvider, OpenAICompatibleProvider, TRANSFORMERS_AVAILABLE

load_dotenv()

def check_dependencies():
    """检查依赖包是否安装"""
    print("🔍 检查依赖包...")
    
    if not TRANSFORMERS_AVAILABLE:
        print("❌ 缺少必要依赖包")
        print("请安装以下包：")
        print("pip install torch transformers accelerate sentencepiece")
        return False
    
    print("✅ 依赖包检查通过")
    return True

def check_local_model_config():
    """检查本地模型配置"""
    print("\n🔧 检查本地模型配置...")
    
    model_path = os.getenv("LOCAL_MODEL_PATH")
    if not model_path:
        print("❌ LOCAL_MODEL_PATH 环境变量未设置")
        print("请在 .env 文件中设置本地模型路径")
        return False
    
    if not os.path.exists(model_path):
        print(f"❌ 模型路径不存在: {model_path}")
        return False
    
    print(f"✅ 模型路径: {model_path}")
    print(f"📊 设备配置: {os.getenv('LOCAL_MODEL_DEVICE', 'auto')}")
    print(f"🌡️ 温度设置: {os.getenv('LOCAL_MODEL_TEMPERATURE', '0.7')}")
    print(f"📏 最大长度: {os.getenv('LOCAL_MODEL_MAX_LENGTH', '4096')}")
    
    return True

def check_openai_compatible_config():
    """检查OpenAI兼容API配置"""
    print("\n🔧 检查OpenAI兼容API配置...")
    
    api_url = os.getenv("OPENAI_COMPATIBLE_API_URL")
    if not api_url:
        print("⚠️ OPENAI_COMPATIBLE_API_URL 环境变量未设置")
        print("如需使用OpenAI兼容API，请在 .env 文件中设置")
        return False
    
    print(f"✅ API地址: {api_url}")
    print(f"🔑 API密钥: {'已设置' if os.getenv('OPENAI_COMPATIBLE_API_KEY') else '未设置'}")
    print(f"🤖 模型名称: {os.getenv('OPENAI_COMPATIBLE_MODEL', 'gpt-3.5-turbo')}")
    
    return True

async def test_local_model():
    """测试本地模型"""
    print("\n🧪 测试本地模型...")
    
    try:
        provider = LocalAIProvider()
        
        test_description = "这是一个简单的Web CTF题目，存在SQL注入漏洞，需要绕过登录验证获取flag"
        print(f"📝 测试描述: {test_description}")
        
        result = await provider.analyze_challenge(test_description, "web")
        
        print("✅ 本地模型测试成功")
        print(f"📋 分析结果长度: {len(result)} 字符")
        print(f"📄 分析结果预览: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 本地模型测试失败: {str(e)}")
        return False

async def test_openai_compatible():
    """测试OpenAI兼容API"""
    print("\n🧪 测试OpenAI兼容API...")
    
    try:
        provider = OpenAICompatibleProvider()
        
        test_description = "这是一个简单的Web CTF题目，存在SQL注入漏洞，需要绕过登录验证获取flag"
        print(f"📝 测试描述: {test_description}")
        
        result = await provider.analyze_challenge(test_description, "web")
        
        print("✅ OpenAI兼容API测试成功")
        print(f"📋 分析结果长度: {len(result)} 字符")
        print(f"📄 分析结果预览: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI兼容API测试失败: {str(e)}")
        return False

def print_usage_tips():
    """打印使用提示"""
    print("\n💡 使用提示:")
    print("1. 本地模型推荐:")
    print("   - ChatGLM3-6B: 适合中等配置机器")
    print("   - Qwen-7B-Chat: 性能较好的中文模型")
    print("   - Baichuan2-7B-Chat: 另一个优秀的中文模型")
    
    print("\n2. 模型下载:")
    print("   - Hugging Face: https://huggingface.co/")
    print("   - ModelScope: https://modelscope.cn/")
    
    print("\n3. OpenAI兼容服务:")
    print("   - vLLM: 高性能推理服务")
    print("   - FastChat: 多模型聊天服务")
    print("   - Text Generation WebUI: 图形界面服务")
    
    print("\n4. 性能优化:")
    print("   - 使用GPU可显著提升推理速度")
    print("   - 量化模型可减少内存占用")
    print("   - 适当调整max_length和temperature参数")

async def main():
    """主函数"""
    print("🚀 CTF智能分析平台 - 本地模型测试工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print_usage_tips()
        return
    
    # 检查配置
    local_config_ok = check_local_model_config()
    openai_config_ok = check_openai_compatible_config()
    
    if not local_config_ok and not openai_config_ok:
        print("\n❌ 没有可用的配置，请参考使用提示进行配置")
        print_usage_tips()
        return
    
    # 测试本地模型
    if local_config_ok:
        local_success = await test_local_model()
    else:
        local_success = False
    
    # 测试OpenAI兼容API
    if openai_config_ok:
        openai_success = await test_openai_compatible()
    else:
        openai_success = False
    
    # 总结
    print("\n📊 测试总结:")
    print(f"   本地模型: {'✅ 成功' if local_success else '❌ 失败'}")
    print(f"   OpenAI兼容API: {'✅ 成功' if openai_success else '❌ 失败'}")
    
    if local_success or openai_success:
        print("\n🎉 恭喜！至少有一个提供者可以正常工作")
        print("现在可以在主程序中使用本地AI模型了")
    else:
        print("\n⚠️ 所有提供者测试失败，请检查配置")
    
    print_usage_tips()

if __name__ == "__main__":
    asyncio.run(main()) 