import pymysql
from config.config import get_mysql_credentials

def execute_queries(queries):
    try:
        credentials = get_mysql_credentials()
        connection = pymysql.connect(
            host=credentials['host'],
            user=credentials['user'],
            password=credentials['password'],
            database=credentials['database']
        )
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Queries executadas com sucesso no banco de dados.")
    except pymysql.MySQLError as e:
        print(f"Erro ao executar queries no banco de dados: {e}")


