# MetaHub 本地大模型 - 使用指南

## ✅ 已部署

| 模型 | 大小 | 状态 |
|------|------|------|
| qwen2.5:7b | 4.6GB | ✅ 运行中 |

## 🚀 快速开始

### 1. 命令行对话
```bash
ollama run qwen2.5:7b
```

### 2. Python 调用
```python
import ollama

response = ollama.chat(model='qwen2.5:7b', messages=[
    {'role': 'user', 'content': '你好'}
])
print(response['message']['content'])
```

### 3. 使用预设角色
```bash
cd /Users/wanyview/clawd
python3 kai-meta-hub/llm/local_llm.py "用一句话介绍TIER"
```

## 📋 支持的任务

| 任务 | 命令 | 说明 |
|------|------|------|
| 总结 | summarize | 100字概括要点 |
| 分析 | analyze | 深入分析 + 洞见 |
| 扩展 | expand | 添加细节和例子 |
| 提问 | question | 生成3个好问题 |

## 🎯 集成到 Kai 系统

```python
from kai_meta_hub.llm.local_llm import LocalLLM, run_task

# 简单对话
llm = LocalLLM()
result = llm.chat("今天天气怎么样")

# Kai 角色分析
result = run_task("analyze", "什么是知识管理", role="kai")
```

## 📊 服务状态

```bash
# 检查服务
curl http://127.0.0.1:11434/api/tags

# 查看日志
tail -f /tmp/ollama.log
```

## 下一步

1. ✅ 本地大模型已就绪
2. ⏳ 可选：下载 qwen2.5:32b (更大模型)
3. ⏳ 可选：集成到 OpenClaw 配置
