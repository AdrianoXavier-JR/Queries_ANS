import os
from dotenv import load_dotenv

load_dotenv()

def get_mysql_credentials():
    return {
        'host': os.getenv('MYSQL_HOST'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE')
    }

def get_ftp_base_url():
    return 'ftp.dadosabertos.ans.gov.br'

def get_ftp_directory():
    return '/FTP/PDA/operadoras_de_plano_de_saude_ativas/'