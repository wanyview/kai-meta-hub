# KaiHub × 附中矩阵 技术对接方案

> 版本：V1.0
> 制定时间：2026-02-17
> 状态：实施中

---

## 一、技术架构概览

### 1.1 KaiHub 技术架构

```
KaiHub/
├── capsule_service/         # 知识胶囊服务 (端口 8005)
│   ├── capsule_api.py       # 胶囊CRUD接口
│   ├── search_api.py       # 搜索接口
│   └── sync_api.py         # 同步接口
├── auth_service/           # 认证服务 (端口 8001)
│   ├── token_api.py        # Token管理
│   └── user_api.py         # 用户管理
├── debate_engine/          # 辩论引擎
│   ├── argument_gen.py     # 论点生成
│   ├── rebuttal_gen.py     # 反驳生成
│   └── debate_session.py   # 辩论会话管理
└── content_platform/       # 内容平台
    ├── article_api.py      # 文章接口
    └── podcast_api.py      # 播客接口
```

### 1.2 附中矩阵技术架构

```
Matrix-BNUHS-v2/
├── services/
│   ├── edumatrix.ts        # V1.2 主入口
│   ├── ecie.ts             # 环境上下文注入引擎
│   ├── mlep.ts             # 模块化逻辑演化协议
│   └── stam.ts             # 社交拓扑对齐模块
├── components/
│   ├── SimulationPanel.tsx  # 模拟面板
│   ├── ChatInterface.tsx    # 聊天接口
│   └── GeospatialView.tsx   # 地理空间视图
└── knowledge/
    ├── capsules/           # 知识胶囊
    └── integration/        # 集成模块
```

### 1.3 技术栈对比

| 组件 | KaiHub | 附中矩阵 | 对接方案 |
|------|--------|----------|----------|
| 后端语言 | Python | TypeScript | API对接 |
| 前端框架 | - | React | iframe嵌入 |
| 数据库 | PostgreSQL | PostgreSQL | 可共享 |
| LLM | 待定 | Google Gemini | 统一接入 |
| 存储 | 本地/OSS | 阿里云OSS | 对象存储对接 |

---

## 二、知识胶囊互通方案

### 2.1 数据模型统一

#### 2.1.1 统一胶囊格式

```typescript
interface UnifiedCapsule {
  // 基础信息
  id: string;              // 全局唯一ID
  source: 'kaihub' | 'matrix';  // 来源平台
  title: string;           // 标题
  content: string;          // 内容（Markdown格式）
  summary: string;          // 摘要
  
  // 分类信息
  category: string;         // 分类
  tags: string[];           // 标签
  keywords: string[];       // 关键词
  
  // 元数据
  author: {
    id: string;
    name: string;
    platform: string;
  };
  created_at: string;      // 创建时间
  updated_at: string;       // 更新时间
  
  // 质量指标
  metrics: {
    views: number;          // 浏览量
    likes: number;          // 点赞数
    citations: number;      // 引用数
    rating: number;         // 评分 (0-5)
    datm_score?: number;    // DATM评分
  };
  
  // 权限
  visibility: 'public' | 'private' | 'shared';
  sync_status: 'synced' | 'pending' | 'blocked';
}
```

#### 2.1.2 分类体系映射

| KaiHub 分类 | 附中矩阵分类 | 统一分类 |
|-------------|-------------|----------|
| AI辩论 | 学科学习 | 人工智能 |
| 知识胶囊 | 知识融合 | 知识管理 |
| 深度文章 | 研究报告 | 学术研究 |
| 播客音频 | 学习资源 | 音频内容 |

### 2.2 接口设计

#### 2.2.1 胶囊同步API

```python
# KaiHub 端 API
@app.route('/api/v1/capsule/sync', methods=['POST'])
def sync_capsule():
    """
    同步知识胶囊到附中矩阵
    """
    data = request.json
    capsule = UnifiedCapsule(**data)
    
    # 1. 数据验证
    validate_capsule(capsule)
    
    # 2. 内容审核
    if not content_review(capsule):
        return {'error': '内容审核未通过'}, 403
    
    # 3. 格式转换
    matrix_format = convert_to_matrix(capsule)
    
    # 4. 发送到附中矩阵
    response = requests.post(
        f'{MATRIX_API_URL}/api/v1/capsule/receive',
        json=matrix_format,
        headers={'Authorization': f'Bearer {SYNC_TOKEN}'}
    )
    
    # 5. 更新同步状态
    update_sync_status(capsule.id, response.status_code == 200)
    
    return response.json()
```

#### 2.2.2 胶囊拉取API

```typescript
// 附中矩阵端 API
interface CapsulePullRequest {
  category?: string;
  tags?: string[];
  limit?: number;
  offset?: number;
  since?: string;  // 更新时间筛选
}

@app.route('/api/v1/capsule/pull', methods=['POST'])
def pull_capsules():
    """
    从KaiHub拉取知识胶囊
    """
    filters = CapsulePullRequest(**request.json)
    
    # 1. 查询KaiHub
    capsules = query_kaihub(filters)
    
    # 2. 格式转换
    matrix_format = capsules.map(convert_to_matrix)
    
    # 3. 存储到本地
    save_to_database(matrix_format)
    
    return {
      'count': len(matrix_format),
      'capsules': matrix_format
    }
```

### 2.3 同步机制

#### 2.3.1 同步策略

```
同步类型：
├── 实时同步
│   └── 重要胶囊（审核通过后立即同步）
├── 定时同步
│   └── 每日凌晨2:00自动同步
└── 手动同步
    └── 用户触发（需审核）
```

#### 2.3.2 冲突处理

| 冲突类型 | 处理策略 |
|----------|----------|
| 同一胶囊被双方修改 | 以更新时间为准 |
| 分类标签冲突 | 保留双方标签 |
| 权限冲突 | 取更严格的权限设置 |

---

## 三、辩论引擎API方案

### 3.1 API设计

#### 3.1.1 发起辩论

```typescript
POST /api/v1/debate/start
Content-Type: application/json

{
  "topic": "AI会不会取代老师？",
  "position": "pro",  // pro = 正方, con = 反方
  "user_id": "matrix_student_001",
  "platform": "matrix",
  "difficulty": "medium",  // easy, medium, hard
  "role": "student"  // student, teacher
}

Response:
{
  "session_id": "debate_001",
  "topic": "AI会不会取代老师？",
  "position": "pro",
  "status": "started",
  "first_argument": {
    "content": "AI将彻底改变教育行业...",
    "confidence": 0.85,
    "sources": ["研究报告1", "案例2"]
  },
  "timer": {
    "total_seconds": 300,
    "remaining_seconds": 300
  }
}
```

#### 3.1.2 获取AI论点

```typescript
GET /api/v1/debate/{session_id}/argument

Response:
{
  "argument": {
    "id": "arg_001",
    "content": "从历史角度看，每一次技术革命都会取代部分传统职业...",
    "type": "historical",
    "confidence": 0.82,
    "supporting_evidence": [
      "工业革命取代了大量手工业者",
      "计算机取代了大量文员工作"
    ],
    "counter_points": [
      "但同时也创造了新的职业"
    ]
  },
  "suggestions_for_rebuttal": [
    "可以从教师的人文关怀角度反驳",
    "可以从个性化教育的局限性角度反驳"
  ]
}
```

#### 3.1.3 提交反驳

```typescript
POST /api/v1/debate/{session_id}/rebuttal
{
  "user_argument": "AI可以传授知识，但无法给予人文关怀..."
}

Response:
{
  "score": 85,
  "feedback": "论点清晰，但论据可以更充分",
  "ai_counter": {
    "content": "但AI可以通过情感计算模拟人文关怀...",
    "strength": 0.75
  },
  "round": 2,
  "timer_remaining": 180
}
```

#### 3.1.4 结束辩论

```typescript
POST /api/v1/debate/{session_id}/end

Response:
{
  "winner": "user",  // user, ai, draw
  "score": {
    "user": 82,
    "ai": 78
  },
  "summary": "在这场辩论中，用户提出了...",
  "key_points": [
    "AI在知识传授方面有优势",
    "人文关怀仍是教师的核心价值"
  ],
  "learning_suggestions": [
    "建议阅读：教育心理学",
    "建议阅读：AI伦理"
  ]
}
```

### 3.2 嵌入方案

#### 3.2.1 iframe嵌入

```tsx
// 附中矩阵组件中嵌入辩论引擎
import { DebateEmbed } from './components/DebateEmbed';

function LearningPage() {
  return (
    <div>
      <h2>AI辩论挑战</h2>
      <DebateEmbed
        apiBase="https://kaihub.example.com/api/v1"
        theme="light"
        onSessionEnd={(result) => {
          // 保存辩论结果到附中矩阵
          saveDebateResult(result);
        }}
      />
    </div>
  );
}
```

#### 3.2.2 API直接调用

```typescript
// 附中矩阵服务中直接调用API
import { KaiHubDebateAPI } from './services/kaihub_api';

class DebateService {
  private api: KaiHubDebateAPI;
  
  async startDebate(topic: string, studentId: string) {
    return this.api.startDebate({
      topic,
      user_id: studentId,
      platform: 'matrix'
    });
  }
}
```

---

## 四、用户认证与权限

### 4.1 统一认证方案

```
认证流程：

用户（附中矩阵登录）
    ↓
    附中矩阵 OAuth2.0
    ↓
    KaiHub 验证 Token
    ↓
    返回 KaiHub API 访问权限
```

### 4.2 权限矩阵

| 功能 | 附中学生 | 附中老师 | KaiHub用户 | 游客 |
|------|---------|---------|-----------|------|
| 查看胶囊 | ✅ | ✅ | ✅ | ✅ |
| 同步胶囊 | ❌ | ✅ | ✅ | ❌ |
| 发起辩论 | ✅ | ✅ | ✅ | ❌ |
| 参与比赛 | ✅ | ✅ | ✅ | ❌ |
| 导出报告 | ✅ | ✅ | ✅ | ❌ |

---

## 五、数据统计

### 5.1 埋点设计

```typescript
// 辩论统计埋点
interface DebateEvent {
  event_type: 'start' | 'arg_submit' | 'rebuttal' | 'end';
  session_id: string;
  user_id: string;
  topic: string;
  duration: number;
  score?: number;
  timestamp: string;
}
```

### 5.2 统计指标

| 指标 | 定义 | 采集方式 |
|------|------|----------|
| 参与人数 | 发起辩论的独立用户数 | UserID去重 |
| 完成率 | 完成整场辩论的比例 | end/start |
| 平均时长 | 每场辩论的平均时间 | 会话时长 |
| 正反比 | 正方/反方选择比例 | 立场统计 |
| 评分分布 | 用户得分的分布 | 评分区间 |

---

## 六、部署架构

### 6.1 架构图

```
                              ┌─────────────────┐
                              │   附中矩阵前端   │
                              │   (React)       │
                              └────────┬────────┘
                                       │
                              ┌────────┴────────┐
                              │   API Gateway    │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
           │   知识胶囊API   │  │  辩论引擎API │  │   统计服务     │
           │   (KaiHub)     │  │   (KaiHub)  │  │   (共享)       │
           └────────────────┘  └─────────────┘  └────────────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                              ┌────────▼────────┐
                              │   附中矩阵后端   │
                              │   (TypeScript)   │
                              └──────────────────┘
```

### 6.2 域名规划

| 服务 | 域名 | 端口 |
|------|------|------|
| KaiHub主站 | kaihub.example.com | 443 |
| 知识胶囊API | api.kaihub.example.com/v1/capsule | 443 |
| 辩论引擎API | api.kaihub.example.com/v1/debate | 443 |
| 附中矩阵 | matrix.bnuhs.example.com | 443 |

---

## 七、实施计划

### 7.1 第1周：技术对接方案确认

| 日期 | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| 02-17 | 双方技术架构分析 | 技术团队 | 🔄 进行中 |
| 02-18 | 接口设计评审 | 技术团队 | ⏳ 待开始 |
| 02-19 | 数据模型统一 | 技术团队 | ⏳ 待开始 |
| 02-20 | 对接方案文档定稿 | 技术团队 | ⏳ 待开始 |

### 7.2 第2周：知识胶囊接口开发

| 日期 | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| 02-21 | 同步API开发 | 后端 | ⏳ |
| 02-22 | 拉取API开发 | 后端 | ⏳ |
| 02-23 | 数据格式转换 | 后端 | ⏳ |
| 02-24 | 单元测试 | 测试 | ⏳ |

### 7.3 第3周：辩论引擎API开发

| 日期 | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| 02-25 | 发起辩论API | 后端 | ⏳ |
| 02-26 | 论点生成API | 后端+AI | ⏳ |
| 02-27 | 反驳生成API | 后端+AI | ⏳ |
| 02-28 | 嵌入组件开发 | 前端 | ⏳ |

### 7.4 第4周：内部测试

| 日期 | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| 03-01 | 联调测试 | 双方 | ⏳ |
| 03-02 | 性能测试 | 测试 | ⏳ |
| 03-03 | 安全测试 | 安全 | ⏳ |
| 03-04 | 验收交付 | 双方 | ⏳ |

---

## 八、验收标准

### 8.1 功能验收

| 功能 | 验收标准 | 优先级 |
|------|----------|--------|
| 知识胶囊同步 | 同步成功率 > 95% | P0 |
| 辩论发起 | 响应时间 < 3秒 | P0 |
| 论点生成 | 生成成功率 > 99% | P0 |
| 数据统计 | 统计误差 < 1% | P1 |

### 8.2 性能验收

| 指标 | 目标值 |
|------|--------|
| API响应时间 | < 500ms (P95) |
| 并发连接数 | > 100 |
| 同步吞吐量 | > 100 胶囊/分钟 |

---

## 九、联系人

| 角色 | KaiHub | 附中矩阵 |
|------|--------|----------|
| 技术负责人 | 待定 | 待定 |
| 接口负责人 | 待定 | 待定 |
| 产品负责人 | 待定 | 待定 |

---

*文档版本：V1.0*
*最后更新：2026-02-17*
