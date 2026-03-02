#!/usr/bin/env python3
"""
MetaHub Podcast Generator - 元枢纽播客生成器
使用 edge-tts 生成高质量语音

功能:
- 解析 **角色:** 对话格式
- 支持不同角色使用不同音色
- 生成完整播客音频
"""

import os
import re
import asyncio
import argparse
import subprocess
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

# 配置音色
VOICE_MAP = {
    # 中文音色
    "Kai": "zh-CN-YunxiNeural",          # 沉稳男声
    "范维友": "zh-CN-XiaoxiaoNeural",    # 标准女声
    "default": "zh-CN-YunyangNeural",   # 男声
    
    # 英文音色 (备用)
    "en_male": "en-US-GuyNeural",
    "en_female": "en-US-JennyNeural",
}

class PodcastGenerator:
    def __init__(self, input_file, output_dir="output", voice_map=None):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.temp_dir = self.output_dir / "temp"
        self.voice_map = voice_map or VOICE_MAP
        
    def parse_script(self):
        """解析播客稿，提取对话"""
        content = self.input_file.read_text(encoding='utf-8')
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        self.title = title_match.group(1) if title_match else "Untitled"
        
        # 提取对话 **角色:** 文本
        pattern = r'\*\*([^*]+):\*\*\s*\n?(.*?)(?=\n\*\*|\n\n#|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        dialogues = []
        for speaker, text in matches:
            speaker = speaker.strip()
            # 清理文本
            text = re.sub(r'\[.*?\]', '', text)  # 移除 [音乐] 等标签
            text = re.sub(r'\n+', ' ', text)
            text = text.strip()
            
            if text and len(text) > 2:
                # 匹配音色
                voice = "zh-CN-YunxiNeural"  # 默认男声
                for name, v in self.voice_map.items():
                    if name in speaker:
                        voice = v
                        break
                
                dialogues.append({
                    "speaker": speaker,
                    "text": text,
                    "voice": voice
                })
        
        return dialogues
    
    async def generate_tts_edge(self, text, voice, output_file):
        """使用 edge-tts 生成语音"""
        import edge_tts
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file
    
    def generate_tts(self, text, voice, output_file):
        """同步调用TTS"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.generate_tts_edge(text, voice, output_file))
        finally:
            loop.close()
    
    def generate(self):
        """生成播客"""
        print(f"🎙️ MetaHub Podcast Generator")
        print(f"==============================")
        print(f"输入: {self.input_file}")
        print(f"")
        
        # 创建目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 解析
        dialogues = self.parse_script()
        print(f"📝 标题: {self.title}")
        print(f"💬 对话数: {len(dialogues)}")
        print(f"")
        
        # 生成语音
        audio_files = []
        for i, dialog in enumerate(dialogues):
            # 限制文本长度，避免API超时
            text = dialog["text"][:500] if len(dialog["text"]) > 500 else dialog["text"]
            
            output_file = self.temp_dir / f"part_{i:03d}.mp3"
            print(f"  [{dialog['speaker']}] {text[:40]}... ({dialog['voice']})")
            
            try:
                self.generate_tts(text, dialog["voice"], str(output_file))
                audio_files.append(output_file)
            except Exception as e:
                print(f"    ⚠️ 生成失败: {e}")
        
        # 合并音频
        if audio_files:
            final_output = self.output_dir / f"{self.title}.mp3"
            self.merge_audio(audio_files, final_output)
            print(f"")
            print(f"✅ 播客生成完成!")
            print(f"输出: {final_output}")
            return str(final_output)
        else:
            print(f"❌ 没有生成任何音频")
            return None
    
    def merge_audio(self, audio_files, output_file):
        """合并音频片段"""
        try:
            combined = AudioSegment.empty()
            silence = AudioSegment.silent(duration=500)  # 500ms静音间隔
            
            for af in audio_files:
                try:
                    segment = AudioSegment.from_mp3(str(af))
                    combined += segment + silence
                except Exception as e:
                    print(f"    ⚠️ 无法加载 {af}: {e}")
            
            if combined:
                combined.export(str(output_file), format="mp3")
                print(f"  📎 已合并 {len(audio_files)} 个片段")
        except Exception as e:
            print(f"  ⚠️ 合并失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="MetaHub Podcast Generator")
    parser.add_argument("input", help="播客稿 Markdown 文件")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    
    args = parser.parse_args()
    
    generator = PodcastGenerator(args.input, args.output)
    generator.generate()

if __name__ == "__main__":
    main()
