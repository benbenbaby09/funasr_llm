import os
import gradio as gr

from funasr import AutoModel

from loguru import logger
from openai import OpenAI

from datetime import datetime

def save_audio(audio):
    # 获取音频数据（采样率, 音频数组）
    sr, audio_data = audio

    # 生成唯一文件名（时间戳 + .wav）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"recorded_audio_{timestamp}.wav"

    # 使用 scipy.io.wavfile 保存为 WAV 文件
    from scipy.io import wavfile
    wavfile.write(output_path, sr, audio_data)

    return os.path.abspath(output_path)

def chat_with_ollama(messages: list[dict], callback=None):
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
    model = os.getenv('OLLAMA_MODEL', 'qwen2:7b')
    logger.debug(f"chat with ollama: {base_url}, model: {model}")

    client = OpenAI(
        base_url=base_url,
        api_key=os.getenv('OLLAMA_API_KEY', 'ollama')
    )

    response = client.chat.completions.create(
        model=model,
        stream=False,
        temperature=0.1,
        messages=messages
    )
    logger.debug(f"chat with ollama: {response}")
    # full_content = ""
    # for chunk in response:
    #     content = chunk.choices[0].delta.content
    #     logger.debug(f"chat with ollama: {content}")
    #     # await callback(content)
    #     full_content += content
    return response.choices[0].message.content

def process_audio(audio):
    # audio 是一个元组 (sample_rate, audio_data)
    sample_rate, audio_data = audio

    # 将 numpy 数组转换为 WAV bytes
    from scipy.io.wavfile import write
    import io
    
    wav_bytes = io.BytesIO()
    write(wav_bytes, sample_rate, audio_data)
    audio_bytes = wav_bytes.getvalue()
    
    return audio_bytes

def transcribe(audio_file: bytes, output: str = "txt"):
    model = AutoModel(model="paraformer-zh",  vad_model="fsmn-vad", punc_model="ct-punc",disable_update=True)
    res = model.generate(input = audio_file,
            batch_size_s=300,
            hotword='魔搭')
    output = res[0]['text'] # 提取文本内容
    logger.info(f"transcribe output:{output},audio_file len:{audio_file.__len__()}")
    return output

#输入文本处理程序
def greet(question, audio_input, correct_answer, role, tips: str, ):
    # 保存音频文件并获取路径
    file_path=save_audio(audio_input)

    # 保存音频文件并获取路径
    audio_bytes = process_audio(audio_input)
    # 调用模型进行处理
    audio_ouput = transcribe(audio_bytes)
    # audio_ouput="Java是吃的"
    logger.info(f"greet: {question}, {audio_ouput}, {correct_answer}, {role}, {tips},{file_path}")
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": tips.format(question = question,correct_answer=correct_answer,answer=audio_ouput)}, 
    ]
    logger.info(f"chat with ollama: {messages}")
    content = chat_with_ollama(messages)

    return [f"{audio_ouput}",f"{content}"]

#接口创建函数
#fn设置处理函数，inputs设置输入接口组件，outputs设置输出接口组件
#fn,inputs,outputs都是必填函数
demo = gr.Interface(fn=greet,
    inputs=[
            gr.Textbox(label="面试官提问", value="用一句话回答java是什么语言.", placeholder="输入提问..."),
            gr.Audio(label="面试者回答",sources="microphone"),
            gr.Textbox(label="预期答案", value="Java 是一种 跨平台、面向对象 的编程语言，通过 JVM 虚拟机 实现 一次编写，到处运行."),
            gr.Textbox(label="AI角色", value="你是一名资深的软件技术专家面试官，你是java之父詹姆斯·高斯林,严格根据提供的正确答案与面试者的回答进行评估，按照要求给出评估结果.", placeholder="输入角色..."),
            gr.Textbox(label="AI提示词", value="我向面试者提了一个问题:{question}；预期答案：{correct_answer}；面试者回答:{answer}；请帮我评估一下是否正确，给个评分，满分是100分(准确性占40分，如果错误则0分;创造性占30分;深度占30分，错别字不扣分)，请给出最终的得分，并判断是否及格(60分及格)", placeholder="输入提示词..."),
    ],
    outputs=[gr.Textbox(label="面试者回答文本"),gr.Textbox(label="AI评估")])

#demo.launch(server_name='0.0.0.0',server_port=443,ssl_certfile="./../keys/ai.suanputao.com.pem", ssl_keyfile="./../keys/ai.suanputao.com.key", ssl_verify=False)
demo.launch(server_name='0.0.0.0')