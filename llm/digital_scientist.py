#!/usr/bin/env python3
"""
MetaHub 数字科学家系统
目标：通过知识沙龙产生知识胶囊

架构：
  知识沙龙 (输入) → 数字科学家 (分析) → 知识胶囊 (输出)
"""

import ollama
import json
import re
from pathlib import Path
from datetime import datetime

# 配置
MODEL = "qwen2.5:7b"
MEMORY_DIR = Path("/Users/wanyview/clawd/memory")
OUTPUT_DIR = Path("/Users/wanyview/clawd/kai-meta-hub/knowledge-capsules")

class DigitalScientist:
    """数字科学家 - 分析知识、产生洞见、生成胶囊"""
    
    def __init__(self, model=MODEL):
        self.model = model
        self.memory_dir = MEMORY_DIR
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def read_memory(self, keyword=None):
        """读取记忆库"""
        files = list(self.memory_dir.glob("*.md"))
        content = []
        
        for f in files:
            text = f.read_text(encoding='utf-8')
            if keyword is None or keyword.lower() in text.lower():
                content.append(f"# {f.stem}\n{text[:2000]}")
        
        return "\n\n---\n\n".join(content)
    
    def analyze_topic(self, topic, context=None):
        """分析主题，产生洞见"""
        system_prompt = """你是 Kai 数字科学家，擅长深度分析和产生洞见。
你的任务是从给定的主题中提取核心思想，发现联系，并产生新的洞见。

输出格式：
1. 核心观点 (100字)
2. 关键洞察 (3条)
3. 知识联系 (与已有知识的联系)
4. 胶囊素材 (可用于创建知识胶囊的要点)
"""
        prompt = f"""
主题：{topic}

{"相关背景：" + context if context else ""}

请深入分析这个主题，产生洞见。
"""
        
        response = ollama.chat(model=self.model, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ])
        
        return response['message']['content']
    
    def generate_capsule(self, topic, analysis, tags):
        """生成知识胶囊"""
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"capsule_{timestamp}_{topic[:20]}.md"
        
        capsule = f"""# 知识胶囊 - {topic}

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}
> 标签：{', '.join(tags)}
> 数字科学家：qwen2.5:7b

---

## 分析结果

{analysis}

---

## 胶囊要点

1. **{topic}的核心是什么？**
2. **这个知识可以应用在哪些场景？**
3. **它与哪些知识有关联？**

---

## 来源

- 知识沙龙讨论
- 数字科学家分析

---
*由 Kai 数字科学家生成*
"""
        
        output_file = self.output_dir / filename
        output_file.write_text(capsule, encoding='utf-8')
        
        return str(output_file)
    
    def run_full_cycle(self, topic, context=None, tags=None):
        """完整流程：分析 + 生成胶囊"""
        print(f"🔬 数字科学家工作中...")
        print(f"   主题: {topic}")
        
        # 1. 分析
        print("   📊 分析中...")
        analysis = self.analyze_topic(topic, context)
        print(f"   ✅ 分析完成")
        
        # 2. 生成胶囊
        print("   💊 生成知识胶囊...")
        tags = tags or ["AI", "知识管理", topic[:10]]
        capsule_file = self.generate_capsule(topic, analysis, tags)
        print(f"   ✅ 胶囊已保存: {capsule_file}")
        
        return {
            "topic": topic,
            "analysis": analysis,
            "capsule": capsule_file
        }

def demo():
    """演示"""
    print("🔬 MetaHub 数字科学家演示")
    print("=" * 50)
    
    scientist = DigitalScientist()
    
    # 示例主题
    topic = "AI时代的知识管理"
    result = scientist.run_full_cycle(
        topic=topic,
        context="知识需要流动、碰撞、才能产生新知",
        tags=["AI", "知识管理", "数字科学家"]
    )
    
    print(f"\n📦 生成的胶囊预览:")
    print(Path(result["capsule"]).read_text(encoding='utf-8')[:500])
    
    print("\n✅ 演示完成!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        scientist = DigitalScientist()
        scientist.run_full_cycle(topic)
    else:
        demo()
