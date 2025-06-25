#!/usr/bin/env python3
"""
测试上下文增强和多轮推理功能
"""

import asyncio
import json
import requests
from datetime import datetime

# 配置
API_BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_001"

def test_context_enhancement():
    """测试上下文增强功能"""
    print("=== 测试上下文增强功能 ===")
    
    # 1. 创建对话会话
    conversation_data = {
        "user_id": TEST_USER_ID,
        "initial_context": {
            "question_type": "web",
            "user_preferences": {
                "language": "zh",
                "analysis_style": "detailed"
            }
        }
    }
    
    response = requests.post(f"{API_BASE_URL}/api/conversations", json=conversation_data)
    if response.status_code == 200:
        conversation_id = response.json()["conversation_id"]
        print(f"✅ 创建对话成功: {conversation_id}")
    else:
        print(f"❌ 创建对话失败: {response.status_code}")
        return
    
    # 2. 第一次分析（使用上下文）
    analysis_request = {
        "description": "这是一个SQL注入题目，需要绕过登录验证",
        "question_type": "web",
        "ai_provider": "deepseek",
        "user_id": TEST_USER_ID,
        "conversation_id": conversation_id,
        "use_context": True
    }
    
    response = requests.post(f"{API_BASE_URL}/api/analyze", json=analysis_request)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 第一次分析成功")
        print(f"   响应长度: {len(result['response'])} 字符")
        print(f"   使用上下文: {result.get('conversation_id') == conversation_id}")
    else:
        print(f"❌ 第一次分析失败: {response.status_code}")
        return
    
    # 3. 第二次分析（继续对话）
    follow_up_request = {
        "description": "如何检测SQL注入点？",
        "question_type": "web",
        "ai_provider": "deepseek",
        "user_id": TEST_USER_ID,
        "conversation_id": conversation_id,
        "use_context": True
    }
    
    response = requests.post(f"{API_BASE_URL}/api/analyze", json=follow_up_request)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 第二次分析成功")
        print(f"   响应长度: {len(result['response'])} 字符")
        print(f"   对话连续性: {result.get('conversation_id') == conversation_id}")
    else:
        print(f"❌ 第二次分析失败: {response.status_code}")

def test_multi_round_conversation():
    """测试多轮对话功能"""
    print("\n=== 测试多轮对话功能 ===")
    
    # 创建新对话
    conversation_data = {
        "user_id": TEST_USER_ID,
        "initial_context": {"question_type": "crypto"}
    }
    
    response = requests.post(f"{API_BASE_URL}/api/conversations", json=conversation_data)
    if response.status_code != 200:
        print(f"❌ 创建对话失败: {response.status_code}")
        return
    
    conversation_id = response.json()["conversation_id"]
    print(f"✅ 创建对话: {conversation_id}")
    
    # 多轮对话测试
    conversation_flow = [
        {
            "description": "这是一个RSA加密题目，已知n和e，如何破解？",
            "question_type": "crypto"
        },
        {
            "description": "如果n很大怎么办？",
            "question_type": "crypto"
        },
        {
            "description": "有哪些常见的RSA攻击方法？",
            "question_type": "crypto"
        }
    ]
    
    for i, message in enumerate(conversation_flow, 1):
        analysis_request = {
            **message,
            "ai_provider": "deepseek",
            "user_id": TEST_USER_ID,
            "conversation_id": conversation_id,
            "use_context": True
        }
        
        response = requests.post(f"{API_BASE_URL}/api/analyze", json=analysis_request)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 第{i}轮对话成功")
            print(f"   问题: {message['description'][:30]}...")
            print(f"   响应长度: {len(result['response'])} 字符")
        else:
            print(f"❌ 第{i}轮对话失败: {response.status_code}")

def test_conversation_management():
    """测试对话管理功能"""
    print("\n=== 测试对话管理功能 ===")
    
    # 1. 获取用户对话列表
    response = requests.get(f"{API_BASE_URL}/api/conversations/user/{TEST_USER_ID}")
    if response.status_code == 200:
        conversations = response.json()["conversations"]
        print(f"✅ 获取对话列表成功，共 {len(conversations)} 个对话")
        
        for conv in conversations[:3]:  # 显示前3个
            print(f"   - {conv['id'][:8]}... ({len(conv['messages'])} 条消息)")
    else:
        print(f"❌ 获取对话列表失败: {response.status_code}")
    
    # 2. 获取特定对话详情
    if conversations:
        conversation_id = conversations[0]["id"]
        response = requests.get(f"{API_BASE_URL}/api/conversations/{conversation_id}")
        if response.status_code == 200:
            conversation = response.json()["conversation"]
            print(f"✅ 获取对话详情成功")
            print(f"   消息数量: {len(conversation['messages'])}")
            print(f"   创建时间: {conversation['created_at']}")
        else:
            print(f"❌ 获取对话详情失败: {response.status_code}")

def test_ai_provider_switching():
    """测试AI提供者切换"""
    print("\n=== 测试AI提供者切换 ===")
    
    # 1. 获取可用提供者
    response = requests.get(f"{API_BASE_URL}/api/ai/providers")
    if response.status_code == 200:
        providers = response.json()["providers"]
        print(f"✅ 获取AI提供者成功，共 {len(providers)} 个")
        
        for provider in providers:
            print(f"   - {provider['name']} ({provider['type']}) - {provider['status']}")
    else:
        print(f"❌ 获取AI提供者失败: {response.status_code}")
        return
    
    # 2. 测试不同提供者的分析
    test_providers = ["deepseek", "siliconflow", "qwen"]
    conversation_data = {
        "user_id": TEST_USER_ID,
        "initial_context": {"question_type": "web"}
    }
    
    response = requests.post(f"{API_BASE_URL}/api/conversations", json=conversation_data)
    if response.status_code != 200:
        print(f"❌ 创建对话失败: {response.status_code}")
        return
    
    conversation_id = response.json()["conversation_id"]
    
    for provider in test_providers:
        if any(p["type"] == provider for p in providers):
            analysis_request = {
                "description": "测试XSS漏洞检测",
                "question_type": "web",
                "ai_provider": provider,
                "user_id": TEST_USER_ID,
                "conversation_id": conversation_id,
                "use_context": True
            }
            
            response = requests.post(f"{API_BASE_URL}/api/analyze", json=analysis_request)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {provider} 分析成功")
                print(f"   响应长度: {len(result['response'])} 字符")
            else:
                print(f"❌ {provider} 分析失败: {response.status_code}")

def main():
    """主测试函数"""
    print("🚀 开始测试上下文增强和多轮推理功能")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API地址: {API_BASE_URL}")
    print("=" * 60)
    
    try:
        # 测试上下文增强
        test_context_enhancement()
        
        # 测试多轮对话
        test_multi_round_conversation()
        
        # 测试对话管理
        test_conversation_management()
        
        # 测试AI提供者切换
        test_ai_provider_switching()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 