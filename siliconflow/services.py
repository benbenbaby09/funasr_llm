import requests
import librosa
import io
from loguru import logger

class Service:
    def __init__(self):
        api_key = "sk-obslycjygbbzmzocpnwgkpewovzbckzilgydmvotzzkhersn"
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        }

    def text_2_audio(self,text) -> str:
        self.__init__()
        url="https://api.siliconflow.cn/v1/audio/speech"
        payload = {
            "input": text,
            "response_format": "mp3",
            "sample_rate": 32000,
            "stream": True,
            "speed": 1,
            "gain": 0,
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            "voice": "FunAudioLLM/CosyVoice2-0.5B:diana"
        }
        logger.info(f"text_2_audio: {payload}")
        response = requests.request("POST", url, json=payload, headers=self.headers)

        logger.info(f"text_2_audio: {type(response.content)}")
        audio_bytes = response.content
        audio_data, sr = librosa.load(io.BytesIO(audio_bytes), sr=44100)  # 假设采样率是44100
        return (sr, audio_data)

    def audio_2_text(self,audio) -> str:
        self.__init__()
        url = "https://api.siliconflow.cn/v1/audio/transcriptions"

        s2t_files = {'file': ("audio.wav", audio, "audio/wav")}
        s2t_payload = {'model': "FunAudioLLM/SenseVoiceSmall"}

        response = requests.post(url,files=s2t_files, data=s2t_payload, headers=self.headers)
        logger.info(f"audio_2_text: {response.json()['text']}")
        return response.json()['text']


service = Service()