import os
import csv
import pymysql
from ftplib import FTP
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# URL base do FTP
base_url = 'ftp.dadosabertos.ans.gov.br'

# Caminho do diretório onde o arquivo está localizado
ftp_directory = '/FTP/PDA/operadoras_de_plano_de_saude_ativas/'

# Função para criar a estrutura de pastas
def create_folder():
    folder_path = 'operadoras_ativas/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Pasta {folder_path} criada.')

# Função para baixar o arquivo CSV
def download_file():
    create_folder()
    
    try:
        # Conectar ao servidor FTP
        ftp = FTP(base_url)
        ftp.login()  # Login anônimo
        
        # Acessa o diretório onde o arquivo está localizado
        ftp.cwd(ftp_directory)
        
        # Lista os arquivos no diretório para verificar se o arquivo está lá
        files = ftp.nlst()  # Lista os arquivos e diretórios no diretório atual
        print("Arquivos disponíveis no FTP:", files)
        
        # Filtra os arquivos CSV disponíveis
        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            print("Erro: Nenhum arquivo CSV encontrado no diretório FTP.")
            return
        
        # Define o nome do arquivo dinamicamente
        file_name = csv_files[0]
        print(f"Arquivo selecionado: {file_name}")
        
        # Faz o download do arquivo
        local_path = os.path.join('operadoras_ativas', file_name)
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {file_name}", local_file.write)
            print(f"Arquivo {file_name} baixado com sucesso.")
        
        # Desconectar do servidor FTP
        ftp.quit()
        return file_name
    except Exception as e:
        print(f"Erro ao acessar o FTP: {e}")
        return None

# Função para gerar a query SQL para criar a tabela
def generate_create_table_query(csv_file_path):
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            columns = reader.fieldnames  # Obtém os nomes das colunas
            
            # Cria a query para criar a tabela
            table_name = 'plano_saude_ativas'
            create_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
            
            # Adiciona as colunas à query
            for column in columns:
                create_query += f"  `{column}` VARCHAR(255),\n"
            
            # Remove a última vírgula e fecha a query
            create_query = create_query.rstrip(',\n') + '\n);'
            return create_query
    except Exception as e:
        print(f"Erro ao gerar query de criação de tabela: {e}")

# Função para gerar queries de inserção no MySQL
def generate_insert_queries(csv_file_path):
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            columns = reader.fieldnames  # Obtém os nomes das colunas
            insert_queries = []
            
            # Para cada linha, cria uma query de inserção
            for row in reader:
                values = [f"'{row[column].replace('\'', '\\\'')}'" for column in columns]  # Escapa apóstrofos
                insert_query = f"INSERT INTO `plano_saude_ativas` ({', '.join(columns)}) VALUES ({', '.join(values)});"
                insert_queries.append(insert_query)
            
            return insert_queries
    except Exception as e:
        print(f"Erro ao gerar queries de inserção: {e}")

# Função para salvar as queries SQL em um arquivo
def save_queries_to_file(queries, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            for query in queries:
                f.write(query + '\n')
        print(f"Queries salvas no arquivo: {file_name}")
    except Exception as e:
        print(f"Erro ao salvar queries no arquivo: {e}")

# Função para executar as queries no MySQL (caso queira executar diretamente no banco)
def execute_queries(queries):
    try:
        # Carrega as credenciais do banco de dados do arquivo .env
        host = os.getenv('MYSQL_HOST')
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')
        
        if not all([host, user, password, database]):
            print("Erro: Credenciais do banco de dados não estão completamente definidas no .env")
            return

        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Queries executadas com sucesso no banco de dados.")
    except pymysql.MySQLError as e:
        print(f"Erro ao executar queries no banco de dados: {e}")

# Fluxo principal do código
downloaded_file = download_file()

if downloaded_file:
    # Caminho para o arquivo CSV
    csv_file_path = os.path.join('operadoras_ativas', downloaded_file)

    # Gerar query para criar a tabela
    create_table_query = generate_create_table_query(csv_file_path)
    if create_table_query:
        print("Query para criar a tabela:")
        print(create_table_query)

    # Gerar queries de inserção
    insert_queries = generate_insert_queries(csv_file_path)

    # Salvar as queries em um arquivo
    if insert_queries:
        save_queries_to_file([create_table_query] + insert_queries, 'queries.sql')

    # Caso queira executar as queries diretamente no MySQL
    if insert_queries:
        execute_queries([create_table_query] + insert_queries)
else:
    print("Não foi possível prosseguir devido ao erro no download do arquivo.")