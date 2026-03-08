"""
知识图谱API - kai-meta-hub
实现跨域关联、节点推理、可视化
"""
from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# 知识图谱存储
knowledge_graph = {
    "nodes": [],
    "edges": []
}

@app.route("/api/kg/add_node", methods=["POST"])
def add_node():
    """添加节点"""
    data = request.json
    node = {
        "id": data.get("id"),
        "label": data.get("label"),
        "type": data.get("type", "concept"),
        "properties": data.get("properties", {}),
        "created_at": datetime.now().isoformat()
    }
    knowledge_graph["nodes"].append(node)
    return jsonify({"success": True, "node": node})

@app.route("/api/kg/add_edge", methods=["POST"])
def add_edge():
    """添加边（关系）"""
    data = request.json
    edge = {
        "id": f"{data['source']}-{data['target']}",
        "source": data["source"],
        "target": data["target"],
        "relation": data.get("relation", "related"),
        "weight": data.get("weight", 1.0)
    }
    knowledge_graph["edges"].append(edge)
    return jsonify({"success": True, "edge": edge})

@app.route("/api/kg/query", methods=["POST"])
def query():
    """查询关联路径"""
    data = request.json
    source = data.get("source")
    target = data.get("target")
    max_depth = data.get("max_depth", 3)
    
    # BFS查找路径
    paths = []
    visited = set()
    queue = [(source, [source])]
    
    while queue and len(paths) < 10:
        node, path = queue.pop(0)
        if node == target:
            paths.append(path)
            continue
        if len(path) >= max_depth:
            continue
        
        for edge in knowledge_graph["edges"]:
            if edge["source"] == node and edge["target"] not in visited:
                visited.add(edge["target"])
                queue.append((edge["target"], path + [edge["target"]]))
    
    return jsonify({"paths": paths, "count": len(paths)})

@app.route("/api/kg/graph", methods=["GET"])
def get_graph():
    """获取完整图谱"""
    return jsonify(knowledge_graph)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8889)
