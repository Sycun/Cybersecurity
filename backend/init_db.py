#!/usr/bin/env python3
"""
数据库初始化脚本
运行此脚本来创建数据库表和初始化默认数据
"""

from database import engine, SessionLocal
from models import Base
from utils import init_default_tools

def init_database():
    """初始化数据库"""
    print("正在创建数据库表...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")
    
    # 初始化默认工具
    print("正在初始化默认工具...")
    db = SessionLocal()
    try:
        init_default_tools(db)
        print("✓ 默认工具初始化完成")
    except Exception as e:
        print(f"✗ 默认工具初始化失败: {e}")
    finally:
        db.close()
    
    print("数据库初始化完成！")

if __name__ == "__main__":
    init_database() 