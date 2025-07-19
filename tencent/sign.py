import hmac
import hashlib
import time
import base64
from urllib.parse import quote


# 用户可以在函数内部生成时间戳, 只需要传入appkey和accessToken即可获取访问接口所需的公共参数和签名
def GenSignature(signing_content, access_token):


    # 计算 HMAC-SHA256 值
    h = hmac.new(access_token.encode(), signing_content.encode(), hashlib.sha256)


    # 将 HMAC-SHA256 值进行 Base64 编码
    hash_in_base64 = base64.b64encode(h.digest()).decode()


    # URL encode
    encode_sign = quote(hash_in_base64)


    # 拼接签名
    signature = f"&signature={encode_sign}"


    return signature


def GenReqURL(parameter, access_token, base_url):
    # 按字典序拼接待计算签名的字符串
    signing_content = '&'.join(f'{k}={parameter[k]}' for k in sorted(parameter.keys()))


    # 计算签名
    signature = GenSignature(signing_content, access_token)


    # 拼接访问接口的完整 URL
    return f'{base_url}?{signing_content}{signature}'




def main():
    base_url = 'https://gw.tvs.qq.com/v2/ivh/interactdriver/interactdriverservice/command'
    access_token = '6234632ac29745d18db0a0c14cacb4ae'
    wss_url = 'wss://gw.tvs.qq.com/v2/ivh/interactdriver/interactdriverservice/command'


    # 示例一(访问需要提供 appkey 和 timestamp 参数的接口):
    # 用户按需填入生成签名所需的公共参数
    parameter1 = {
        'appkey': '41e3a94538b342eb979a57f79aa59dd6',
        # 用户提供的时间戳应保证单位为秒且与当前时间相差不得超过五分钟
        # 示例时间戳:
        # 'timestamp': '1717639699'
        # 推荐使用下面的语句生成当前时间戳:
        'timestamp': int(time.time())  # 使用当前时间戳（单位：秒）
    }
    url1 = GenReqURL(parameter1, access_token, base_url)
    # 使用示例时间戳输出应当如下:
    # Example 1:https://api.example.com/v2/ivh/example_uri?appkey=example_appkey&timestamp=1717639699&signature=aCNWYzZdplxWVo%2BJsqzZc9%2BJ9XrwWWITfX3eQpsLVno%3D
    print('Example 1:', url1)


    # 示例二(访问需要提供 appkey, requestID 和 timestamp 参数的接口):
    # 用户按需填入生成签名所需的公共参数
    parameter2 = {
        'appkey': '41e3a94538b342eb979a57f79aa59dd6',
        'requestid': 'example_requestid',
        # 用户提供的时间戳应保证单位为秒且与当前时间相差不得超过五分钟
        # 示例时间戳:
        # 'timestamp': '1717639699'
        # 推荐使用下面的语句生成当前时间戳:
        'timestamp': int(time.time())  # 使用当前时间戳（单位：秒）
    }
    url2 = GenReqURL(parameter2, access_token, wss_url)
    # 使用示例时间戳输出应当如下:
    # Example 2:wss://api.example.com/v2/ws/ivh/example_uri?appkey=example_appkey&requestid=example_requestid&timestamp=1717639699&signature=QVenICk0VHtHGYZKXM6IC%2BW1CjZC1joSr%2Fx0gfKKYT4%3D
    print('Example 2:', url2)


if __name__ == '__main__':
    main()