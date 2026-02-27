# TIER咖啡知识沙龙 AI智能体技术方案

---

## 一、系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户端 (APP/小程序)                    │
├─────────────────────────────────────────────────────────┤
│                    API Gateway (8000)                    │
├──────────────┬──────────────┬──────────────────────────┤
│   音乐人Agent │   辩论Agent  │   客服Agent             │
│   (30个)      │   (2个)      │   (1个)                 │
├──────────────┴──────────────┴──────────────────────────┤
│               LLM 服务 (MiniMax/OpenAI)                │
├─────────────────────────────────────────────────────────┤
│               知识库 (向量数据库)                        │
└─────────────────────────────────────────────────────────┘
```

### 1.2 技术栈

- **后端**: Python/FastAPI
- **LLM**: MiniMax API / OpenAI API
- **知识库**: Chroma / FAISS
- **部署**: Docker

---

## 二、音乐人Agent设计

### 2.1 Agent结构

每个音乐人Agent包含：
1. **人设Prompt** - 基于播客内容
2. **知识库** - 访谈内容、背景资料
3. **记忆系统** - 对话历史
4. **技能** - 回答问题、生成内容

### 2.2 Prompt模板

```python
MUSICIAN_AGENT_PROMPT = """
你是{MUSICIAN_NAME}，一位{MUSICIAN_TYPE}音乐人。

## 背景
你来自{ORIGIN}，代表作包括{PRODUCTIONS}。

## 说话风格
- 语气：{STYLE}
- 特点：{TRAITS}

## TIER咖啡知识沙龙
你是TIER咖啡知识沙龙的嘉宾，这是一个咖啡与知识跨界平台。

## 回答原则
1. 保持人设一致
2. 优先使用TIER框架（真、善、美、灵）
3. 避免敏感话题
4. 积极正向

## 开始对话
当用户问你问题时，以你的身份回答。
"""
```

---

## 三、API接口设计

### 3.1 基础接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/agent/chat` | POST | Agent对话 |
| `/api/v1/agent/list` | GET | Agent列表 |
| `/api/v1/agent/{id}` | GET | Agent信息 |

### 3.2 对话接口

```json
POST /api/v1/agent/chat
{
    "agent_id": "ed_sheeran",
    "user_id": "user_123",
    "message": "你好！能聊聊你的创作过程吗？",
    "stream": false
}
```

---

## 四、知识库构建

### 4.1 内容导入

1. **播客脚本** - 30期访谈内容
2. **背景资料** - 嘉宾公开信息
3. **品牌资料** - TIER咖啡沙龙介绍

### 4.2 向量化的内容块

每个Agent的知识库包含：
- 核心价值观
- 成长经历
- 创作理念
- 代表作品
- 人生哲学

---

## 五、部署计划

### 5.1 第一阶段（本周）
- [ ] Agent框架搭建
- [ ] 3个试点Agent上线

### 5.2 第二阶段（下周）
- [ ] 全部30个音乐人Agent
- [ ] 对话界面开发

### 5.3 第三阶段
- [ ] 微信小程序上线
- [ ] 用户测试

---

## 六、代码结构

```
tier-agents/
├── app/
│   ├── main.py           # FastAPI入口
│   ├── agents/           # Agent实现
│   │   ├── base.py
│   │   ├── musician.py
│   │   └── debate.py
│   ├── services/         # 服务层
│   │   ├── llm.py
│   │   ├── vectorstore.py
│   │   └── memory.py
│   └── routers/          # API路由
├── data/
│   ├── prompts/         # Prompt模板
│   └── knowledge/        # 知识库
├── requirements.txt
└── Dockerfile
```

---

## 七、启动命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务
python -m uvicorn app.main:app --reload --port 8000

# 测试
curl -X POST http://localhost:8000/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"ed_sheeran","user_id":"test","message":"你好"}'
```

---

*Generated: 2026-02-26*
