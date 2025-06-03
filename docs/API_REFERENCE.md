# 📡 API 参考文档 / API Reference

本文档提供了CTF智能分析平台所有API端点的详细说明和使用示例。

---

## 📋 基础信息 / Basic Information

| 项目 | 值 |
|------|-----|
| **基础URL** | `http://localhost:8000` |
| **API版本** | `v2.1` |
| **数据格式** | JSON / Form Data |
| **认证方式** | 无 (当前版本) |
| **速率限制** | 暂无限制 |

### 🔗 在线文档

启动服务后，访问以下地址查看交互式API文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎯 核心分析API / Core Analysis API

### 📊 分析CTF题目

**端点**: `POST /api/analyze`

分析CTF题目并返回AI生成的解题思路和工具推荐。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `text` | string | 否 | 题目描述文本 |
| `file` | file | 否 | 上传的题目文件 |

**注意**: `text` 和 `file` 至少提供一个。

#### 请求示例

```bash
# 使用文本描述
curl -X POST http://localhost:8000/api/analyze \
  -F "text=这是一个SQL注入题目，请分析如何利用漏洞"

# 上传文件
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@challenge.txt"

# 同时提供文本和文件
curl -X POST http://localhost:8000/api/analyze \
  -F "text=这是一个逆向工程题目" \
  -F "file=@binary_file"
```

#### 响应示例

```json
{
  "id": 123,
  "description": "这是一个SQL注入题目，请分析如何利用漏洞",
  "type": "web",
  "ai_response": "根据题目描述，这是一个典型的SQL注入漏洞...",
  "recommended_tools": [
    {
      "id": 1,
      "name": "sqlmap",
      "description": "自动化SQL注入工具",
      "command": "sqlmap -u 'http://target.com/vulnerable.php?id=1' --dbs",
      "category": "web"
    }
  ],
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### 🔄 使用指定AI提供者分析

**端点**: `POST /api/analyze/with-provider`

使用指定的AI服务提供者进行分析，无需更改全局配置。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `text` | string | 否 | 题目描述文本 |
| `file` | file | 否 | 上传的题目文件 |
| `provider` | string | 否 | AI提供者 (`deepseek`, `siliconflow`, `local`, `openai_compatible`) |

#### 请求示例

```bash
curl -X POST http://localhost:8000/api/analyze/with-provider \
  -F "text=这是一个密码学题目" \
  -F "provider=deepseek"
```

---

## ⚙️ 配置管理API / Configuration Management API

### 📋 获取当前配置

**端点**: `GET /api/settings`

获取当前AI服务配置信息，API密钥会被掩码显示以保护敏感信息。

#### 响应示例

```json
{
  "provider": "deepseek",
  "deepseek_api_url": "https://api.deepseek.com/v1/chat/completions",
  "deepseek_model": "deepseek-chat",
  "deepseek_api_key": "sk-12345...",
  "siliconflow_api_url": "https://api.siliconflow.cn/v1/chat/completions",
  "siliconflow_model": "Qwen/QwQ-32B",
  "openai_compatible_api_url": "",
  "openai_compatible_model": "gpt-3.5-turbo",
  "local_model_path": "",
  "local_model_type": "auto",
  "local_model_device": "auto",
  "local_model_max_length": 4096,
  "local_model_temperature": 0.7
}
```

### 🔧 更新配置

**端点**: `POST /api/settings`

更新AI服务配置并实时应用新设置。

#### 请求体示例

```json
{
  "provider": "siliconflow",
  "siliconflow_api_key": "sk-new-api-key-here",
  "siliconflow_model": "Qwen/QwQ-32B"
}
```

#### 响应示例

```json
{
  "message": "配置更新成功"
}
```

### 🧪 测试连接

**端点**: `POST /api/test-connection`

测试AI服务连接状态，验证配置是否正确。

#### 请求体示例

```json
{
  "provider": "deepseek"  // 可选，不提供则测试当前配置
}
```

#### 响应示例

```json
{
  "message": "连接成功 - deepseek"
}
```

---

## 📚 历史记录API / History API

### 📋 获取历史记录

**端点**: `GET /api/history`

获取分析历史记录，支持分页。

#### 查询参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `skip` | integer | 0 | 跳过的记录数 |
| `limit` | integer | 20 | 返回的记录数限制 |

#### 请求示例

```bash
# 获取最新20条记录
curl http://localhost:8000/api/history

# 分页获取
curl http://localhost:8000/api/history?skip=20&limit=10
```

#### 响应示例

```json
[
  {
    "id": 123,
    "description": "SQL注入题目分析",
    "type": "web",
    "ai_response": "这是一个典型的SQL注入漏洞...",
    "recommended_tools": [...],
    "timestamp": "2024-01-01T12:00:00.000000"
  },
  ...
]
```

### 🗑️ 删除历史记录

**端点**: `DELETE /api/history/{question_id}`

删除指定的历史记录。

#### 路径参数

| 参数 | 类型 | 描述 |
|------|------|------|
| `question_id` | integer | 要删除的记录ID |

#### 请求示例

```bash
curl -X DELETE http://localhost:8000/api/history/123
```

#### 响应示例

```json
{
  "message": "删除成功"
}
```

---

## 🛠️ 工具推荐API / Tools API

### 📋 根据题型获取工具

**端点**: `GET /api/tools/{question_type}`

根据题目类型获取推荐的CTF工具。

#### 路径参数

| 参数 | 类型 | 描述 |
|------|------|------|
| `question_type` | string | 题目类型 (`web`, `pwn`, `reverse`, `crypto`, `misc`) |

#### 请求示例

```bash
curl http://localhost:8000/api/tools/web
```

#### 响应示例

```json
[
  {
    "id": 1,
    "name": "sqlmap",
    "description": "自动化SQL注入工具",
    "command": "sqlmap -u 'target_url' --dbs",
    "category": "web"
  },
  {
    "id": 2,
    "name": "burpsuite",
    "description": "Web应用安全测试工具",
    "command": "burpsuite",
    "category": "web"
  }
]
```

---

## 📈 统计信息API / Statistics API

### 📊 获取基础统计

**端点**: `GET /api/stats`

获取平台使用统计信息。

#### 响应示例

```json
{
  "total_questions": 150,
  "type_stats": {
    "web": 45,
    "pwn": 32,
    "reverse": 28,
    "crypto": 25,
    "misc": 20
  }
}
```

### ⚡ 获取性能统计

**端点**: `GET /api/stats/performance`

获取AI服务性能统计和系统配置信息。

#### 响应示例

```json
{
  "ai_performance": {
    "total_requests": 1000,
    "average_response_time": 2.5,
    "success_rate": 98.5,
    "cache_hit_rate": 75.2,
    "provider_stats": {
      "deepseek": {
        "requests": 800,
        "avg_time": 2.3,
        "success_rate": 99.1
      }
    }
  },
  "config": {
    "cache_enabled": true,
    "cache_ttl": 3600,
    "request_timeout": 60
  }
}
```

---

## 🧠 AI服务管理API / AI Service Management API

### 📋 获取可用提供者

**端点**: `GET /api/ai/providers`

获取所有可用的AI服务提供者列表。

#### 响应示例

```json
{
  "available_providers": [
    {
      "id": "deepseek",
      "name": "DeepSeek",
      "description": "DeepSeek AI服务"
    },
    {
      "id": "siliconflow",
      "name": "硅基流动",
      "description": "硅基流动AI服务"
    },
    {
      "id": "local",
      "name": "本地模型",
      "description": "本地部署的AI模型"
    },
    {
      "id": "openai_compatible",
      "name": "OpenAI兼容",
      "description": "OpenAI兼容API"
    }
  ],
  "current_provider": "deepseek",
  "current_provider_name": "DeepSeek"
}
```

### 🔄 切换AI提供者

**端点**: `POST /api/ai/switch`

切换当前使用的AI服务提供者。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `provider_type` | string | 是 | 提供者类型 |

#### 请求示例

```bash
curl -X POST http://localhost:8000/api/ai/switch \
  -F "provider_type=siliconflow"
```

#### 响应示例

```json
{
  "message": "成功切换到 siliconflow",
  "current_provider": "siliconflow"
}
```

---

## 💾 缓存管理API / Cache Management API

### 📊 获取缓存统计

**端点**: `GET /api/cache/stats`

获取缓存系统的统计信息。

#### 响应示例

```json
{
  "cache_enabled": true,
  "total_requests": 1000,
  "cache_hits": 750,
  "cache_misses": 250,
  "hit_rate": 75.0,
  "cache_size": 128,
  "ttl": 3600
}
```

### 🗑️ 清空缓存

**端点**: `POST /api/cache/clear`

清空所有缓存数据。

#### 响应示例

```json
{
  "message": "缓存已清空"
}
```

---

## 🏥 系统健康检查API / Health Check API

### 📋 健康状态检查

**端点**: `GET /health`

检查系统各组件的健康状态。

#### 响应示例

```json
{
  "status": "healthy",
  "database": "healthy",
  "ai_provider": "deepseek",
  "cache_enabled": true,
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### 📊 详细系统信息

**端点**: `GET /`

获取API基础信息。

#### 响应示例

```json
{
  "message": "CTF智能分析平台API",
  "version": "2.1.0"
}
```

---

## 🚨 错误响应 / Error Responses

### HTTP状态码

| 状态码 | 含义 | 描述 |
|--------|------|------|
| 200 | 成功 | 请求成功处理 |
| 400 | 请求错误 | 请求参数有误 |
| 404 | 未找到 | 资源不存在 |
| 413 | 文件过大 | 上传文件超出大小限制 |
| 500 | 服务器错误 | 内部服务器错误 |

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 常见错误示例

```json
// 400 - 请求参数错误
{
  "detail": "请提供题目描述或上传文件"
}

// 413 - 文件过大
{
  "detail": "文件大小超过限制 (10485760 bytes)"
}

// 500 - 服务器错误
{
  "detail": "分析失败: AI服务连接超时"
}
```

---

## 🔒 安全考虑 / Security Considerations

### 🛡️ 数据保护

- **API密钥掩码**: 获取配置时，API密钥会被掩码显示
- **文件大小限制**: 上传文件大小限制为10MB
- **输入验证**: 所有输入参数都经过验证和清理

### 🚧 访问控制

当前版本无认证机制，建议在生产环境中：
- 使用反向代理配置IP白名单
- 启用HTTPS加密传输
- 配置防火墙规则限制访问

---

## 📝 SDK和示例 / SDKs and Examples

### 🐍 Python示例

```python
import requests

# 基础配置
BASE_URL = "http://localhost:8000"

# 分析题目
def analyze_challenge(text):
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        data={"text": text}
    )
    return response.json()

# 获取历史记录
def get_history(skip=0, limit=20):
    response = requests.get(
        f"{BASE_URL}/api/history",
        params={"skip": skip, "limit": limit}
    )
    return response.json()

# 更新配置
def update_settings(settings):
    response = requests.post(
        f"{BASE_URL}/api/settings",
        json=settings
    )
    return response.json()

# 使用示例
result = analyze_challenge("这是一个SQL注入题目")
print(result)
```

### 🌐 JavaScript示例

```javascript
// 基础配置
const BASE_URL = 'http://localhost:8000';

// 分析题目
async function analyzeChallenge(text) {
  const formData = new FormData();
  formData.append('text', text);
  
  const response = await fetch(`${BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// 获取配置
async function getSettings() {
  const response = await fetch(`${BASE_URL}/api/settings`);
  return await response.json();
}

// 测试连接
async function testConnection(provider) {
  const response = await fetch(`${BASE_URL}/api/test-connection`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ provider })
  });
  
  return await response.json();
}

// 使用示例
analyzeChallenge('这是一个逆向工程题目')
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

---

## 📞 支持和反馈 / Support

如果您在使用API时遇到问题，请通过以下方式获取帮助：

- 📖 **文档**: [项目README](../README.md)
- 🐛 **Bug报告**: [GitHub Issues](https://github.com/your-repo/issues)
- 💡 **功能请求**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 **直接联系**: your-email@example.com

---

*本API文档持续更新，确保与最新版本保持同步* 