import pymysql
from src import config

def connect_to_database():
    credentials = config.get_mysql_credentials()
    try:
        connection = pymysql.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"]
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fetch_nome_fantasia_by_reg_ans(nome_tabela, reg_ans_list):
    connection = connect_to_database()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        block_size = 100
        nomes_fantasia = set()

        for i in range(0, len(reg_ans_list), block_size):
            block = reg_ans_list[i:i + block_size]
            placeholders = ', '.join(['%s'] * len(block))
            query = f"SELECT Nome_Fantasia FROM {nome_tabela} WHERE Registro_ANS IN ({placeholders})"
            cursor.execute(query, block)

            resultados = cursor.fetchall()
            for linha in resultados:
                nomes_fantasia.add(linha[0])

        return list(nomes_fantasia)
    except pymysql.MySQLError as erro:
        print(f"Erro ao acessar o banco de dados: {erro}")
        return []
    finally:
        cursor.close()
        connection.close()
