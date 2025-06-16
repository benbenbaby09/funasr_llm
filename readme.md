# ASR 演示项目
本项目是一个自动语音识别（ASR）演示项目，结合了语音转录和大语言模型交互功能，用于模拟软件技术专家面试官对面试者回答的评估。

## 项目功能
1. **音频处理**：将输入的音频数据转换为 WAV 格式的字节流。
2. **语音转录**：使用 `paraformer-zh` 模型将音频文件转录为文本。
3. **智能评估**：结合 Ollama 平台的 `qwen2:7b` 模型，根据预期答案对面试者的回答进行评估并给出评分。

## 项目结构
```plaintext
.gradio\
  flagged\
    dataset1.csv
__pycache__\
  asr_funasr.cpython-312.pyc
index.py
readme.md
requirements.txt
```

## 依赖安装
在项目根目录下运行以下命令安装所需依赖：
```bash
pip install -r requirements.txt
```
依赖列表如下：
```plaintext
gradio
loguru
funasr
modelscope
torchaudio
openai
```

## 环境配置
需要设置以下环境变量：
- `OLLAMA_BASE_URL`：Ollama 服务的基础 URL，默认为 `http://localhost:11434/v1`。
- `OLLAMA_MODEL`：使用的 Ollama 模型，默认为 `qwen2:7b`。
- `OLLAMA_API_KEY`：Ollama 服务的 API 密钥，默认为 `ollama`。

## 运行项目
在项目根目录下运行以下命令启动项目：
```bash
python index.py
```
启动后，在浏览器中访问 `http://0.0.0.0:7860` 即可使用项目提供的 Gradio 界面。

## 核心函数说明
1. `process_audio(audio)`：将输入的音频数据转换为 WAV 格式的字节流。
2. `transcribe(audio_file, output='txt')`：使用 `paraformer-zh` 模型将音频文件转录为文本。
3. `chat_with_ollama(messages, callback=None)`：与 Ollama 服务进行交互，获取模型的回复。
4. `greet(question, audio_input, correct_answer, role, tips)`：整合音频处理、语音转录和模型交互功能，给出面试者回答的文本和 AI 评估结果。
        