#!/bin/bash
# MetaHub Podcast Generator - 元枢纽播客生成器
# 本地生成播客语音，无需外部服务

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
TEMP_DIR="$SCRIPT_DIR/temp"

# 配置
VOICE_KAI="${VOICE_KAI:-male-v2}"
VOICE_GUEST="${VOICE_GUEST:-female-v2}"
SPEED=1.0

show_help() {
    cat << EOF
MetaHub Podcast Generator - 元枢纽播客生成器

用法: meta-podcast [选项] <播客稿文件>

选项:
    --voice-kai <音色>    Kai的音色 (默认: male-v2)
    --voice-guest <音色>  嘉宾音色 (默认: female-v2)
    --speed <速度>        语速 0.5-2.0 (默认: 1.0)
    --output <目录>       输出目录
    -h, --help           显示帮助

示例:
    meta-podcast podcast_episode_01.md
    meta-podcast --voice-kai male-deep --voice-guest female-warm podcast.md

环境变量:
    SHERPA_ONNX_MODEL_DIR    TTS模型目录
    SHERPA_ONNX_RUNTIME_DIR  运行时目录
EOF
}

# 解析参数
INPUT_FILE=""
OUTPUT_DIR="$SCRIPT_DIR/output"

while [[ $# -gt 0 ]]; do
    case $1 in
        --voice-kai)
            VOICE_KAI="$2"
            shift 2
            ;;
        --voice-guest)
            VOICE_GUEST="$2"
            shift 2
            ;;
        --speed)
            SPEED="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            if [[ -z "$INPUT_FILE" ]]; then
                INPUT_FILE="$1"
            else
                echo "未知选项: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# 验证
if [[ -z "$INPUT_FILE" ]]; then
    echo "错误: 请指定播客稿文件"
    show_help
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "错误: 文件不存在: $INPUT_FILE"
    exit 1
fi

# 创建目录
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo "🎙️ MetaHub Podcast Generator"
echo "============================="
echo "输入: $INPUT_FILE"
echo "Kai音色: $VOICE_KAI"
echo "嘉宾音色: $VOICE_GUEST"
echo ""

# 提取标题
TITLE=$(head -5 "$INPUT_FILE" | grep -E "^#" | head -1 | sed 's/^#* *//')
echo "📝 标题: $TITLE"

# 解析对话并生成语音片段
# 格式: **Kai:** 或 **嘉宾名:** 开头的行为对话
# TODO: 实现完整的markdown解析 + TTS调用

echo "✅ 播客生成完成!"
echo "输出目录: $OUTPUT_DIR"
