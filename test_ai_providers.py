#!/usr/bin/env python3
"""
测试AI Provider多模型支持功能
"""

import sys
import os
sys.path.append('backend')

def test_ai_providers():
    """测试AI Provider工厂和配置"""
    try:
        # 模拟环境变量
        os.environ['AI_SERVICE'] = 'deepseek'
        
        # 测试Provider工厂
        from backend.ai_providers import AIProviderFactory
        
        print("=== AI Provider 多模型支持测试 ===\n")
        
        # 1. 测试获取可用Provider
        print("1. 获取可用AI提供者:")
        providers = AIProviderFactory.get_available_providers()
        for key, info in providers.items():
            print(f"   - {key}: {info['name']}")
            print(f"     描述: {info['description']}")
            print(f"     类型: {info['type']}")
            print(f"     支持语言: {', '.join(info['languages'])}")
            print(f"     最大tokens: {info['max_tokens']}")
            print(f"     功能: {', '.join(info['features'])}")
            print()
        
        # 2. 测试Provider创建
        print("2. 测试Provider创建:")
        try:
            provider = AIProviderFactory.create_provider('deepseek')
            print(f"   ✅ 成功创建 DeepSeek Provider")
        except Exception as e:
            print(f"   ❌ 创建 DeepSeek Provider 失败: {e}")
        
        try:
            provider = AIProviderFactory.create_provider('siliconflow')
            print(f"   ✅ 成功创建 硅基流动 Provider")
        except Exception as e:
            print(f"   ❌ 创建 硅基流动 Provider 失败: {e}")
        
        try:
            provider = AIProviderFactory.create_provider('openai_compatible')
            print(f"   ✅ 成功创建 OpenAI兼容 Provider")
        except Exception as e:
            print(f"   ❌ 创建 OpenAI兼容 Provider 失败: {e}")
        
        # 3. 测试新添加的Provider
        print("\n3. 测试新添加的Provider:")
        new_providers = ['qwen', 'glm', 'llama']
        for provider_type in new_providers:
            try:
                provider = AIProviderFactory.create_provider(provider_type)
                print(f"   ✅ 成功创建 {provider_type} Provider")
            except Exception as e:
                print(f"   ❌ 创建 {provider_type} Provider 失败: {e}")
        
        print("\n=== 测试完成 ===")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装必要的依赖包")
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_ai_providers() 