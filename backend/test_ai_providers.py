#!/usr/bin/env python3
"""
AI提供者测试脚本
用于测试不同AI提供者的功能
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_providers import AIProviderFactory
from ai_service import AIService

load_dotenv()

async def test_ai_providers():
    """测试所有可用的AI提供者"""
    print("🧪 开始测试AI提供者...")
    
    # 获取可用的提供者
    available_providers = AIProviderFactory.get_available_providers()
    print(f"📋 可用的AI提供者: {available_providers}")
    
    # 测试题目
    test_description = "这是一个Web CTF题目，需要进行SQL注入攻击来获取flag"
    test_type = "web"
    
    for provider_key, provider_name in available_providers.items():
        print(f"\n🔧 测试 {provider_name} ({provider_key})...")
        
        try:
            # 创建AI服务实例
            ai_service = AIService(provider_type=provider_key)
            
            # 测试分析功能
            result = await ai_service.analyze_challenge(test_description, test_type)
            
            print(f"✅ {provider_name} 测试成功")
            print(f"📝 分析结果长度: {len(result)} 字符")
            print(f"📄 分析结果预览: {result[:200]}...")
            
        except Exception as e:
            print(f"❌ {provider_name} 测试失败: {str(e)}")
    
    print("\n🎉 AI提供者测试完成!")

async def test_provider_switching():
    """测试AI提供者切换功能"""
    print("\n🔄 测试AI提供者切换功能...")
    
    try:
        # 创建AI服务实例
        ai_service = AIService()
        
        # 获取当前提供者信息
        info = ai_service.get_provider_info()
        print(f"📊 当前提供者: {info['current_provider_name']} ({info['current_provider']})")
        
        # 尝试切换到其他提供者
        available_providers = list(info['available_providers'].keys())
        if len(available_providers) > 1:
            current = info['current_provider']
            target = next(p for p in available_providers if p != current)
            
            print(f"🔄 尝试切换到: {info['available_providers'][target]} ({target})")
            success = ai_service.switch_provider(target)
            
            if success:
                new_info = ai_service.get_provider_info()
                print(f"✅ 切换成功! 当前提供者: {new_info['current_provider_name']}")
            else:
                print("❌ 切换失败")
        else:
            print("ℹ️ 只有一个可用的提供者，无法测试切换功能")
            
    except Exception as e:
        print(f"❌ 提供者切换测试失败: {str(e)}")

def check_environment():
    """检查环境变量配置"""
    print("🔍 检查环境变量配置...")
    
    required_vars = {
        'AI_SERVICE': os.getenv('AI_SERVICE'),
        'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
        'SILICONFLOW_API_KEY': os.getenv('SILICONFLOW_API_KEY')
    }
    
    for var_name, var_value in required_vars.items():
        if var_value:
            if 'KEY' in var_name:
                print(f"✅ {var_name}: {'*' * 10}{var_value[-4:]}")
            else:
                print(f"✅ {var_name}: {var_value}")
        else:
            print(f"⚠️ {var_name}: 未设置")
    
    print()

async def main():
    """主函数"""
    print("🚀 CTF智能分析平台 - AI提供者测试")
    print("=" * 50)
    
    # 检查环境变量
    check_environment()
    
    # 测试AI提供者
    await test_ai_providers()
    
    # 测试提供者切换
    await test_provider_switching()

if __name__ == "__main__":
    asyncio.run(main()) 