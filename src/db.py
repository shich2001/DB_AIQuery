import psycopg2

def get_schema(config):
    """
    连接到 PostgreSQL 数据库并提取模式。

    Args:
        config: 包含数据库连接参数的字典。

    Returns:
        表示数据库模式的字符串。
    """
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()

        # 获取所有表名
        cur.execute(
            """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
            """
        )
        schemas = cur.fetchall()

        if not schemas:
            cur.close()
            conn.close()
            return "Error: No schema found in the database."

        # 如果只有一个模式，直接使用它
        if len(schemas) == 1:
            selected_schema = schemas[0][0]
        else:
            # 让用户选择模式
            print("\\nAvailable schemas:")
            for i, schema in enumerate(schemas):
                print(f"{i + 1}. {schema[0]}")

            while True:
                try:
                    schema_index = int(input("Please select a schema number: ")) - 1
                    if 0 <= schema_index < len(schemas):
                        selected_schema = schemas[schema_index][0]
                        break
                    else:
                        print("Invalid schema number.")
                except ValueError:
                    print("Please enter a valid number.")

        # 获取选定模式下的所有表名
        cur.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{selected_schema}'
            """
        )
        tables = cur.fetchall()

        schema_str = f"Schema: {selected_schema}\\n"
        for table in tables:
            table_name = table[0]
            schema_str += f"Table: {table_name}\\n"

            # 获取列信息
            cur.execute(
                f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                AND table_schema = '{selected_schema}'
                """
            )
            columns = cur.fetchall()
            for column in columns:
                column_name, data_type = column
                schema_str += f"  Column: {column_name} ({data_type})\\n"

        cur.close()
        conn.close()
        return schema_str

    except psycopg2.OperationalError as e:
        print(f"连接数据库时发生错误：{e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"发生未知错误：{e}")
        return f"Error: {e}"