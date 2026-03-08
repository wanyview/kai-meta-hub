<img src="./static/logo.png" alt="KAI-Meta-Hub Logo" width="200"/>

[![GitHub Stars](https://img.shields.io/github/stars/wanyview/kai-meta-hub?style=flat-square&color=DAA520)](https://github.com/wanyview/kai-meta-hub/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wanyview/kai-meta-hub?style=flat-square)](https://github.com/wanyview/kai-meta-hub/network)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)

> 知识图谱引擎 - 节点关联与路径查询

KAI-Meta-Hub是知识图谱核心引擎，支持动态节点/边构建、BFS路径查询、图谱分析等能力。为知识胶囊系统提供强大的关联分析支持。

---

## ✨ 特性

- **动态图谱**: 实时创建节点和边
- **路径查询**: BFS/A*路径搜索
- **图分析**: 度中心性、PageRank等
- **可视化**: 图谱可视化支持

---

## 🚀 快速开始

```bash
git clone https://github.com/wanyview/kai-meta-hub.git
cd kai-meta-hub
pip install -r requirements.txt
python api.py
```

服务启动: http://localhost:8892

---

## 📖 API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/nodes` | POST | 创建节点 |
| `/api/edges` | POST | 创建边 |
| `/api/path` | GET | 路径查询 |
| `/api/analyze` | GET | 图谱分析 |

---

*Built with ❤️ by KAI*
