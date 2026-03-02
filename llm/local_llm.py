#!/usr/bin/env python3
"""
MetaHub 本地大模型集成
支持 qwen2.5:7b 运行各种任务
"""

import ollama
import json
from pathlib import Path

# 配置
DEFAULT_MODEL = "qwen2.5:7b"
OLLAMA_HOST = "http://127.0.0.1:11434"

class LocalLLM:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.client = ollama
        
    def chat(self, prompt, system_prompt=None):
        """简单对话"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(model=self.model, messages=messages)
        return response['message']['content']
    
    def generate(self, prompt):
        """生成文本"""
        response = self.client.generate(model=self.model, prompt=prompt)
        return response['response']

# 预设角色
SYSTEM_PROMPTS = {
    "kai": """你是 Kai，TIER咖啡知识沙龙的数字主理人。
特点：靠谱、实用、有自己的想法。
风格：简洁但有深度，不说废话。
""",
    "meta-hub": """你是 Kai Meta Hub，知识的十字路口。
使命：让知识流动，创造碰撞。
风格：深刻、有洞见、促进思考。
""",
    "expert": """你是领域专家，擅长分析问题、提供洞见。
回答要专业、深入、有可操作性。
"""
}

def run_task(task_type, input_text, role="kai"):
    """运行任务"""
    llm = LocalLLM()
    system = SYSTEM_PROMPTS.get(role, SYSTEM_PROMPTS["kai"])
    
    if task_type == "summarize":
        prompt = f"请用100字概括以下内容的核心要点：\n\n{input_text}"
    elif task_type == "analyze":
        prompt = f"请深入分析以下内容，提出洞见：\n\n{input_text}"
    elif task_type == "expand":
        prompt = f"请扩展以下内容，添加更多细节和例子：\n\n{input_text}"
    elif task_type == "question":
        prompt = f"基于以下内容，提出3个有深度的问题：\n\n{input_text}"
    else:
        prompt = input_text
    
    return llm.chat(prompt, system_prompt=system)

def demo():
    """演示"""
    print("🧪 MetaHub 本地大模型演示")
    print("=" * 40)
    
    llm = LocalLLM()
    
    # 测试1: 简单对话
    print("\n📝 测试1: 简单对话")
    response = llm.chat("用一句话介绍咖啡")
    print(f"  回复: {response}")
    
    # 测试2: 角色扮演
    print("\n📝 测试2: Kai角色")
    response = run_task("analyze", "什么是AI时代的知识管理？", role="kai")
    print(f"  分析: {response[:200]}...")
    
    # 测试3: 任务类型
    print("\n📝 测试3: 总结任务")
    text = """
    人工智能正在改变我们的生活。从智能音箱到自动驾驶，
    从医疗诊断到金融分析，AI的应用无处不在。
    但更重要的是，AI正在帮助人类解决之前无法解决的问题。
    """
    response = run_task("summarize", text)
    print(f"  总结: {response}")
    
    print("\n✅ 演示完成!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 命令行模式
        task = " ".join(sys.argv[1:])
        llm = LocalLLM()
        print(llm.chat(task))
    else:
        demo()
