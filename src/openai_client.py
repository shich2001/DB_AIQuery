import requests
import json

def get_available_models(api_base_url, api_key):
    """
    获取可用的 OpenAI 模型。

    Args:
        api_base_url: OpenAI API 的基本 URL。
        api_key: OpenAI API 密钥。

    Returns:
        模型列表，如果出现错误则返回错误信息。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{api_base_url}/models", headers=headers)
        response.raise_for_status()  # 如果响应状态码不是 2xx，则引发异常
        models = response.json()
        return [model["id"] for model in models["data"]]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def send_request(api_base_url, api_key, model, schema, messages):
    """
    向 OpenAI API 发送请求。

    Args:
        api_base_url: OpenAI API 的基本 URL。
        api_key: OpenAI API 密钥。
        model: 要使用的模型。
        schema: 数据库模式。
        messages: 用户的自然语言请求。

    Returns:
        API 响应，如果出现错误则返回错误信息。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": messages,
    }
    try:
        response = requests.post(
            f"{api_base_url}/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"