import re
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Tool
from schemas import ToolResponse
from data_service import data_service

def detect_question_type(description: str, filename: Optional[str] = None) -> str:
    """检测CTF题目类型"""
    description_lower = description.lower()
    
    # Web相关关键词
    web_keywords = [
        'sql', 'xss', 'csrf', 'lfi', 'rfi', 'ssrf', 'ssti', 'xxe',
        'upload', 'cookie', 'session', 'jwt', 'php', 'javascript',
        'http', 'url', 'web', 'server', 'apache', 'nginx', 'login',
        'injection', 'bypass', 'filter', 'waf'
    ]
    
    # Pwn相关关键词
    pwn_keywords = [
        'buffer', 'overflow', 'rop', 'shellcode', 'stack', 'heap',
        'format', 'string', 'canary', 'aslr', 'pie', 'nx', 'got',
        'plt', 'libc', 'gdb', 'pwntools', 'exploit', 'binary',
        'elf', 'x86', 'x64', 'arm'
    ]
    
    # Reverse相关关键词
    reverse_keywords = [
        'reverse', 'ida', 'ghidra', 'ollydbg', 'x64dbg', 'disasm',
        'decompile', 'unpack', 'upx', 'vmprotect', 'themida',
        'algorithm', 'keygen', 'crack', 'serial', 'license',
        'obfuscate', 'anti-debug'
    ]
    
    # Crypto相关关键词
    crypto_keywords = [
        'rsa', 'aes', 'des', 'md5', 'sha', 'hash', 'encrypt',
        'decrypt', 'cipher', 'key', 'crypto', 'prime', 'modular',
        'gcd', 'lcm', 'factorization', 'discrete', 'logarithm',
        'elliptic', 'curve', 'signature', 'certificate'
    ]
    
    # Misc相关关键词
    misc_keywords = [
        'steganography', 'stego', 'forensics', 'pcap', 'wireshark',
        'memory', 'dump', 'volatility', 'binwalk', 'strings',
        'hexdump', 'base64', 'morse', 'qr', 'barcode', 'image',
        'audio', 'video', 'zip', 'archive', 'password'
    ]
    
    # 文件扩展名检测
    if filename:
        filename_lower = filename.lower()
        if any(ext in filename_lower for ext in ['.php', '.html', '.js', '.jsp', '.asp']):
            return 'web'
        elif any(ext in filename_lower for ext in ['.exe', '.elf', '.bin', '.so']):
            return 'pwn'
        elif any(ext in filename_lower for ext in ['.pcap', '.pcapng', '.cap']):
            return 'misc'
        elif any(ext in filename_lower for ext in ['.jpg', '.png', '.gif', '.wav', '.mp3']):
            return 'misc'
    
    # 关键词匹配计分
    scores = {
        'web': sum(1 for keyword in web_keywords if keyword in description_lower),
        'pwn': sum(1 for keyword in pwn_keywords if keyword in description_lower),
        'reverse': sum(1 for keyword in reverse_keywords if keyword in description_lower),
        'crypto': sum(1 for keyword in crypto_keywords if keyword in description_lower),
        'misc': sum(1 for keyword in misc_keywords if keyword in description_lower)
    }
    
    # 返回得分最高的类型
    max_score = max(scores.values())
    if max_score > 0:
        return max(scores, key=scores.get)
    
    return 'unknown'

def get_recommended_tools(question_type: str, db: Session = None) -> List[ToolResponse]:
    """根据题目类型获取推荐工具"""
    # 使用data_service从文件获取工具
    tools = data_service.get_tools(category=question_type)
    
    # 转换为ToolResponse格式
    tool_responses = []
    for tool in tools:
        tool_response = ToolResponse(
            id=tool.get('id', 0),
            name=tool.get('name', ''),
            description=tool.get('description', ''),
            command=tool.get('command', ''),
            category=tool.get('category', '')
        )
        tool_responses.append(tool_response)
    
    return tool_responses

def get_default_tools(question_type: str) -> List[ToolResponse]:
    """获取默认工具列表"""
    default_tools = {
        'web': [
            {
                'id': 1,
                'name': 'Burp Suite',
                'description': 'Web应用安全测试工具',
                'command_template': 'burpsuite',
                'category': 'web_scanner'
            },
            {
                'id': 2,
                'name': 'SQLMap',
                'description': 'SQL注入检测和利用工具',
                'command_template': 'sqlmap -u "{url}" --batch',
                'category': 'sql_injection'
            },
            {
                'id': 3,
                'name': 'Dirb',
                'description': '目录和文件暴力破解工具',
                'command_template': 'dirb {url}',
                'category': 'directory_bruteforce'
            },
            {
                'id': 4,
                'name': 'Nikto',
                'description': 'Web服务器漏洞扫描器',
                'command_template': 'nikto -h {url}',
                'category': 'web_scanner'
            }
        ],
        'pwn': [
            {
                'id': 5,
                'name': 'GDB',
                'description': 'GNU调试器',
                'command_template': 'gdb {binary}',
                'category': 'debugger'
            },
            {
                'id': 6,
                'name': 'pwntools',
                'description': 'CTF框架和漏洞利用开发库',
                'command_template': 'python3 exploit.py',
                'category': 'exploit_framework'
            },
            {
                'id': 7,
                'name': 'checksec',
                'description': '二进制保护机制检查工具',
                'command_template': 'checksec {binary}',
                'category': 'binary_analysis'
            },
            {
                'id': 8,
                'name': 'ROPgadget',
                'description': 'ROP链构造工具',
                'command_template': 'ROPgadget --binary {binary}',
                'category': 'rop_analysis'
            }
        ],
        'reverse': [
            {
                'id': 9,
                'name': 'IDA Pro',
                'description': '专业逆向工程工具',
                'command_template': 'ida64 {binary}',
                'category': 'disassembler'
            },
            {
                'id': 10,
                'name': 'Ghidra',
                'description': 'NSA开源逆向工程工具',
                'command_template': 'ghidra',
                'category': 'disassembler'
            },
            {
                'id': 11,
                'name': 'strings',
                'description': '提取二进制文件中的字符串',
                'command_template': 'strings {binary}',
                'category': 'string_analysis'
            },
            {
                'id': 12,
                'name': 'file',
                'description': '文件类型识别工具',
                'command_template': 'file {binary}',
                'category': 'file_analysis'
            }
        ],
        'crypto': [
            {
                'id': 13,
                'name': 'SageMath',
                'description': '数学计算软件',
                'command_template': 'sage',
                'category': 'math_tool'
            },
            {
                'id': 14,
                'name': 'John the Ripper',
                'description': '密码破解工具',
                'command_template': 'john {hashfile}',
                'category': 'password_cracker'
            },
            {
                'id': 15,
                'name': 'Hashcat',
                'description': '高级密码恢复工具',
                'command_template': 'hashcat -m {mode} {hashfile} {wordlist}',
                'category': 'password_cracker'
            },
            {
                'id': 16,
                'name': 'OpenSSL',
                'description': '密码学工具包',
                'command_template': 'openssl {command}',
                'category': 'crypto_tool'
            }
        ],
        'misc': [
            {
                'id': 17,
                'name': 'Binwalk',
                'description': '固件分析工具',
                'command_template': 'binwalk {file}',
                'category': 'firmware_analysis'
            },
            {
                'id': 18,
                'name': 'Steghide',
                'description': '隐写术工具',
                'command_template': 'steghide extract -sf {file}',
                'category': 'steganography'
            },
            {
                'id': 19,
                'name': 'Wireshark',
                'description': '网络协议分析器',
                'command_template': 'wireshark {pcap_file}',
                'category': 'network_analysis'
            },
            {
                'id': 20,
                'name': 'Volatility',
                'description': '内存取证工具',
                'command_template': 'volatility -f {memory_dump} imageinfo',
                'category': 'memory_forensics'
            }
        ]
    }
    
    tools_data = default_tools.get(question_type, [])
    return [ToolResponse(**tool) for tool in tools_data]

def init_default_tools(db: Session):
    """初始化默认工具到数据库"""
    # 检查是否已经初始化
    if db.query(Tool).count() > 0:
        return
    
    all_tools = []
    for question_type in ['web', 'pwn', 'reverse', 'crypto', 'misc']:
        tools = get_default_tools(question_type)
        for tool_data in tools:
            tool = Tool(
                name=tool_data.name,
                description=tool_data.description,
                command_template=tool_data.command_template,
                applicable_types=question_type,
                category=tool_data.category,
                is_active=True
            )
            all_tools.append(tool)
    
    db.add_all(all_tools)
    db.commit() 