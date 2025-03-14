# DB_AIQuery (v1.0.0)

本项目是一个连接到 PostgreSQL 数据库并允许用户使用自然语言进行查询的应用程序。它利用 OpenAI 兼容的 API 将自然语言查询转换为 SQL 查询，并返回结果。

## 功能

*   **连接到 PostgreSQL 数据库**：使用 `config.json` 中提供的连接参数连接到 PostgreSQL 数据库。
*   **数据库模式提取**：自动提取连接的数据库的模式（表名和列信息）。
*   **自然语言查询**：用户可以使用自然语言输入数据提取请求。
*   **OpenAI API 集成**：
    *   获取可用的 OpenAI 模型列表。
    *   将用户请求、数据库模式和对话历史发送到选定的 OpenAI 兼容模型。
    *   显示从 API 返回的 SQL 查询和执行结果。
*   **用户可配置设置**：通过 `config.json` 文件配置以下参数：
    *   PostgreSQL 连接参数（主机、端口、数据库名称、用户名、密码）。
    *   OpenAI API 基本 URL。
    *   OpenAI API 密钥。
    *   OpenAI 模型选择。

## 项目结构

```
智能数据库查找助手/
├── src/
│   ├── config.py      # 配置文件管理
│   ├── db.py         # 数据库连接和模式提取
│   ├── openai_client.py # OpenAI API 客户端
│   └── main.py       # 主程序逻辑和用户界面
└── README.md       # 项目说明
```

## 安装和配置
**从源代码运行：**
1.  **安装依赖项**：

    ```bash
    pip install psycopg2-binary requests
    ```
    使用`psycopg2-binary`而不是`psycopg2`以避免手动构建依赖。

2.  **配置 `config.json`**：

    在项目根目录下创建 `config.json` 文件，并填入以下内容：

    ```json
    {
        "postgresql": {
            "host": "localhost",
            "port": 5432,
            "database": "your_database_name",
            "user": "your_username",
            "password": ""
        },
        "openai": {
            "api_base_url": "https://api.openai.com/v1",
            "api_key": "",
            "model": "gpt-3.5-turbo"
        }
    }
    ```
     将占位符替换为您的实际值。“your_preferred_model”应该在运行程序时从可用模型列表中选择, **请注意，为了安全起见，`password` 和 `api_key` 字段已留空。在运行程序之前，您需要填写这些字段。**

3.  **获取 OpenAI API 密钥**：

    如果您还没有 OpenAI API 密钥，请访问 OpenAI 网站 ([https://platform.openai.com/](https://platform.openai.com/)) 注册并获取 API 密钥。

**从打包版本运行：**

1.  解压 `智能数据库查找助手.zip`。
2.  按照上述 “从源代码运行” 中的第 2 步和第 3 步配置 `config.json`。

## 使用说明

1.  **准备一个PostgreSQL数据库。** 例如，创建一个名为 `employees` 的数据库，其中包含一个名为 `employees` 的表，其中包含以下列：

    ```sql
    CREATE TABLE employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        department VARCHAR(255),
        salary INTEGER
    );

    INSERT INTO employees (name, department, salary) VALUES
    ('Alice', 'Engineering', 80000),
    ('Bob', 'Sales', 60000),
    ('Charlie', 'Engineering', 90000);
    ```

2.  **在 `config.json` 中配置数据库连接信息和 OpenAI API 信息。**

3.  **运行程序**：

    ```bash
    python src/main.py
    ```

4.  **按照提示输入配置信息。** 程序将显示可用的 OpenAI 模型, 并选择数据库结构。

5.  **选择一个模型。**

6.  **输入自然语言查询。** 例如：

    ```
    找出工程部门所有员工的姓名和工资。
    ```

7.  程序将显示生成的 SQL 查询和从数据库返回的结果。

## 注意事项

*   程序目前将所有对话历史发送给大模型，对于较长的对话或复杂的数据库模式，可能会超出token限制。
*   **为了安全起见，`config.json` 文件中的敏感信息（如密码和 API 密钥）已清空。在运行程序之前，请务必填写这些字段。**