# 数据文件夹结构说明

本文件夹用于存储CTF智能分析平台的所有本地数据，替代了原有的数据库存储方式。

## 文件夹结构

```
data/
├── ai_models/          # AI模型文件存储
├── analysis_history/   # 分析历史记录
├── auto_solve/         # 自动解题记录
├── cache/             # AI响应缓存
├── challenges/        # CTF题目数据
│   ├── crypto/        # 密码学题目
│   ├── misc/          # 杂项题目
│   ├── pwn/           # 二进制题目
│   ├── reverse/       # 逆向工程题目
│   └── web/           # Web题目
├── configs/           # 配置文件
│   ├── tools.json     # 工具配置
│   ├── solve_templates.json  # 解题模板配置
│   └── user_config.json      # 用户配置
├── exports/           # 导出文件
└── README.md          # 本文件
```

## 数据文件说明

### 1. 题目数据 (challenges/)
- **存储位置**: `data/challenges/{type}/`
- **文件格式**: JSON
- **文件命名**: `challenge_{id}.json`
- **内容**: 题目描述、类型、AI分析结果、上传文件信息等

### 2. 分析历史 (analysis_history/)
- **存储位置**: `data/analysis_history/`
- **文件格式**: JSON
- **文件命名**: `history_{id}.json`
- **内容**: 分析记录、时间戳、题目ID等

### 3. 自动解题记录 (auto_solve/)
- **存储位置**: `data/auto_solve/`
- **文件格式**: JSON
- **文件命名**: `auto_solve_{id}.json`
- **内容**: 解题方法、代码、执行结果、flag等

### 4. AI响应缓存 (cache/)
- **存储位置**: `data/cache/`
- **文件格式**: JSON
- **文件命名**: `cache_{hash}.json`
- **内容**: AI分析结果、时间戳、缓存键等

### 5. 工具配置 (configs/tools.json)
- **存储位置**: `data/configs/tools.json`
- **文件格式**: JSON
- **内容**: 工具名称、描述、类别、使用说明等

### 6. 解题模板配置 (configs/solve_templates.json)
- **存储位置**: `data/configs/solve_templates.json`
- **文件格式**: JSON
- **内容**: 模板名称、类别、描述、代码模板、参数等

### 7. 用户配置 (configs/user_config.json)
- **存储位置**: `data/configs/user_config.json`
- **文件格式**: JSON
- **内容**: 用户偏好设置、AI提供者配置等

### 8. 导出文件 (exports/)
- **存储位置**: `data/exports/`
- **文件格式**: JSON/CSV
- **文件命名**: `export_{type}_{timestamp}.{format}`
- **内容**: 导出的历史记录、题目数据、配置等

## 数据管理

### 后端数据服务 (data_service.py)
- 提供统一的数据读写接口
- 支持JSON文件的增删改查操作
- 自动处理文件路径和命名
- 提供数据统计和导出功能

### 前端数据服务 (localDataService.ts)
- 提供前端数据访问接口
- 支持本地文件读写
- 与后端API保持一致的数据结构

## 改造完成的功能

✅ **题目数据**: 从数据库迁移到 `data/challenges/` 文件存储  
✅ **分析历史**: 从数据库迁移到 `data/analysis_history/` 文件存储  
✅ **自动解题**: 从数据库迁移到 `data/auto_solve/` 文件存储  
✅ **AI缓存**: 从内存缓存迁移到 `data/cache/` 文件存储  
✅ **工具配置**: 从数据库迁移到 `data/configs/tools.json` 文件存储  
✅ **解题模板**: 从数据库迁移到 `data/configs/solve_templates.json` 文件存储  
✅ **用户配置**: 从数据库迁移到 `data/configs/user_config.json` 文件存储  
✅ **导出功能**: 支持导出数据到 `data/exports/` 文件夹  

## 优势

1. **无数据库依赖**: 完全基于文件系统，无需配置数据库
2. **数据透明**: 所有数据以JSON格式存储，便于查看和编辑
3. **易于备份**: 整个data文件夹可以轻松备份和迁移
4. **版本控制友好**: JSON文件适合版本控制系统
5. **跨平台兼容**: 文件系统在所有操作系统上都可用

## 注意事项

1. 确保data文件夹有适当的读写权限
2. 定期备份重要的数据文件
3. 大量数据时注意文件系统的性能
4. JSON文件格式需要保持一致性 