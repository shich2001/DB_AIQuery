from config import Config
from db import get_schema
from openai_client import get_available_models, send_request
import json
import logging

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filename="query_log.txt",  # 将日志输出到文件
    filemode="a",  # 追加模式
)


def get_input(prompt, default_value, is_secret=False):
    if is_secret and default_value:
        masked_default = (
            default_value[:2] + "*" * (len(default_value) - 4) + default_value[-2:]
        )
        prompt += f" (默认: {masked_default})"
    else:
        prompt += f" (默认: {default_value})"
    value = input(f"{prompt}: ")
    return value if value else default_value


def main():
    config = Config()

    # 尝试加载现有配置
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            existing_config = json.load(f)
    except FileNotFoundError:
        existing_config = config.get_config()  # 使用 Config 类的默认配置

    print("请配置PostgreSQL连接参数：")
    config.postgresql["host"] = get_input("主机", config.postgresql["host"])
    config.postgresql["port"] = int(
        get_input("端口", config.postgresql["port"])
    )  # 确保端口是整数
    config.postgresql["database"] = get_input("数据库", config.postgresql["database"])
    config.postgresql["user"] = get_input("用户名", config.postgresql["user"])
    config.postgresql["password"] = get_input(
        "密码", config.postgresql["password"], is_secret=True
    )

    print("\\n请配置OpenAI API参数：")
    config.openai["api_base_url"] = get_input(
        "API基本URL", config.openai["api_base_url"]
    )
    config.openai["api_key"] = get_input("API密钥", config.openai["api_key"], is_secret=True)
    config.openai["model"] = get_input("模型", config.openai["model"])

    postgresql_config = config.get_postgresql_config()
    openai_config = config.get_openai_config()

    # 打印 PostgreSQL 配置
    print("PostgreSQL 配置：", postgresql_config)

    print("\\n")  # 添加空行

    # 获取数据库模式
    schema = get_schema(postgresql_config)

    print("\\n")  # 添加空行

    if schema.startswith("Error"):
        print(f"获取数据库模式时出错：{schema}")
        return

    # 打印数据库模式
    print("数据库模式：")
    print(schema)
     # 记录数据库连接信息和模式
    logging.info(
        f"PostgreSQL Config: {postgresql_config}, Schema: \\n{schema}"
    )

    # 获取可用模型
    models = get_available_models(openai_config["api_base_url"], openai_config["api_key"])
    if isinstance(models, str) and models.startswith("Error"):
        print(f"获取模型列表时出错：{models}")
        return

    print("\\n可用模型：")
    for i, model in enumerate(models):
        print(f"{i + 1}. {model}")

    # 选择模型
    while True:
        try:
            model_index = int(input("请选择要使用的模型编号：")) - 1
            if 0 <= model_index < len(models):
                selected_model = models[model_index]
                break
            else:
                print("无效的模型编号。")
        except ValueError:
            print("请输入有效的数字。")

    # 比较配置
    current_config = {"postgresql": config.postgresql, "openai": config.openai}
    if current_config == existing_config:
        print("配置没有改变。")
    else:
        if input("是否要将配置保存到config.json？(y/n): ").lower() == "y":
            config.save()
            print("配置已保存。")

    # 初始化消息列表
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that translates natural language queries into SQL based on the provided schema.\\n\\nSchema:\\n{schema}",
        }
    ]

    # 持续对话循环
    while True:
        # 获取用户请求
        user_request = input("\\n请输入您的自然语言查询（或输入 'exit' 退出）：")
        if user_request.lower() == "exit":
            break

        # 记录用户请求
        logging.info(f"User Request: {user_request}")

        # 添加用户消息到消息列表
        messages.append({"role": "user", "content": user_request})

        # 发送请求
        response = send_request(
            openai_config["api_base_url"],
            openai_config["api_key"],
            selected_model,
            schema,
            messages,  # 发送整个消息列表
        )

        if isinstance(response, str) and response.startswith("Error"):
            print(f"发送请求时出错：{response}")
        else:
            print("\\nAPI 响应：")
            assistant_response = response["choices"][0]["message"]["content"]
            print(assistant_response)

            # 记录模型回答
            logging.info(f"Assistant Response: {assistant_response}")

            # 添加 API 响应到消息列表
            messages.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    main()