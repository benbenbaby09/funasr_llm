import requests
import time
from tencent.sign import GenReqURL

class TencentDigitalHumanAPI:
    def __init__(self, api_key=None, secret_key=None):
        """
        初始化腾讯数字人接口类
        
        :param base_url: 接口基础URL
        :param api_key: 可选，API密钥
        :param secret_key: 可选，密钥
        """
        self.base_url = "https://gw.tvs.qq.com"
        self.appkey="41e3a94538b342eb979a57f79aa59dd6"
        self.access_token = '6234632ac29745d18db0a0c14cacb4ae'
        self.virtualmanProjectId="7bb615660733475cbe2a87efd2df02db"
        self.AssetVirtualmanKey="ace89ff1f10e4dc5b0ca2545734028e0"

    def create_session(self):
        """
        创建新的会话
        
        :return: 包含会话ID的响应，失败则返回None
        """
        create_session_url=f"{self.base_url}/v2/ivh/sessionmanager/sessionmanagerservice/createsessionbyasset"
        parameter1 = {
            'appkey': self.appkey,
            # 用户提供的时间戳应保证单位为秒且与当前时间相差不得超过五分钟
            # 示例时间戳:
            # 'timestamp': '1717639699'
            # 推荐使用下面的语句生成当前时间戳:
            'timestamp': int(time.time())  # 使用当前时间戳（单位：秒）
        }

        sign_url = GenReqURL(parameter1, self.access_token, create_session_url)
        print(sign_url)
        # url = f"https://gw.tvs.qq.com/v2/ivh/sessionmanager/sessionmanagerservice/createsession?appkey={self.appkey}&timestamp=1752894120&signature=eAzQq/fPRuo4SgTG77rw6pN/4zbZm9wMja6Njdlgh%2BI%3D"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "Header": {},
            "Payload": {
                "ReqId": "d7aa08da33dd4a662ad5be508c5b77cf",
                "VirtualmanProjectId": self.virtualmanProjectId,
                "AssetVirtualmanKey": self.AssetVirtualmanKey,
                "DriverType": 1,
                "UserId": "virtualhuman",
                "Protocol": "rtmp"
            }
        }
        print(data)
        
        try:
            response = requests.post(sign_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            self.session_id = result.get("session_id")
            return result
        except requests.RequestException as e:
            print(f"创建会话失败: {e}")
            return None

    def send_dialogue_text(self, text):
        """
        发送对话文本
        
        :param text: 要发送的对话文本
        :return: 包含回复的响应，失败则返回None
        """
        if not self.session_id:
            print("会话未创建，请先调用create_session方法")
            return None
        
        url = f"{self.base_url}/send_text"
        headers = {}
        if self.api_key:
            headers["API-Key"] = self.api_key
        
        data = {
            "session_id": self.session_id,
            "text": text
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"发送对话文本失败: {e}")
            return None

chat_api = TencentDigitalHumanAPI()