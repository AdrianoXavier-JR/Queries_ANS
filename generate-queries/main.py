from config.config import get_ftp_base_url, get_ftp_directory
from data.ftp_handler import download_file_from_ftp
from data.csv_handler import read_csv
from db.query_generator import generate_create_table_query, generate_insert_queries
from db.mysql_handler import execute_queries
from utils.file_utils import save_queries_to_file
import os

def main():
    base_url = get_ftp_base_url()
    ftp_directory = get_ftp_directory()

    downloaded_file = download_file_from_ftp(base_url, ftp_directory)

    if downloaded_file:
        csv_file_path = os.path.join('generate-queries/result', downloaded_file)

        csv_data = read_csv(csv_file_path)
        if not csv_data:
            print("Erro ao ler o arquivo CSV.")
            return

        columns = csv_data[0].keys()

        create_table_query = generate_create_table_query(columns)
        print("Query para criar a tabela:")
        print(create_table_query)

        insert_queries = generate_insert_queries(csv_data, columns)

        if insert_queries:
            save_queries_to_file([create_table_query] + insert_queries, 'generate-queries/result/queries.sql')

        if insert_queries:
            execute_queries([create_table_query] + insert_queries)
    else:
        print("Não foi possível prosseguir devido ao erro no download do arquivo.")

if __name__ == '__main__':
    main()
