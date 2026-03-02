# MetaHub 本地播客生成器 - 安装指南

## 当前状态

✅ **TTS 已可用** (edge-tts)
⏳ **FFmpeg 待安装** (用于合并音频)

## 安装 FFmpeg (macOS)

### 方法1: Homebrew (推荐)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```

### 方法2: MacPorts
```bash
sudo port install ffmpeg
```

### 方法3: 直接下载
访问 https://evermeet.cx/ffmpeg/ 下载 arm64 版本

---

## 使用方法

### 生成播客
```bash
cd /Users/wanyview/clawd
python3 kai-meta-hub/scripts/podcast_generator.py kai-meta-hub/podcast_episode_01_fan_weiyou_final.md
```

### 只生成前N段测试
```bash
python3 -c "
import asyncio
import edge_tts
import re
from pathlib import Path

content = Path('kai-meta-hub/podcast_episode_01_fan_weiyou_final.md').read_text()
pattern = r'\*\*([^*]+):\*\*\s*\n?(.*?)(?=\n\*\*|\n\n#|\Z)'
matches = re.findall(pattern, content, re.DOTALL)

async def gen():
    for i, (s, t) in enumerate(matches[:3]):
        s = s.strip()
        t = re.sub(r'\[.*?\]', '', t)
        t = re.sub(r'\n+', ' ', t).strip()[:200]
        v = 'zh-CN-YunxiNeural' if 'Kai' in s else 'zh-CN-XiaoxiaoNeural'
        out = f'kai-meta-hub/output/part_{i+1}_{s}.mp3'
        await edge_tts.Communicate(t, v).save(out)
        print(f'✓ {s}')
        
asyncio.run(gen())
"
```

### 音色选择
| 角色 | 音色 |
|------|------|
| Kai | zh-CN-YunxiNeural (沉稳男声) |
| 嘉宾 | zh-CN-XiaoxiaoNeural (标准女声) |
| 其他男声 | zh-CN-YunyangNeural |
| 其他女声 | zh-CN-XiaoxiaoNeural |

---

## 下一步

1. 安装 FFmpeg
2. 运行完整生成
3. 发送给你播放
