from ftplib import FTP
import os

def create_folder(directory='generate_queries_ans/result/'):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Pasta {directory} criada.")

def download_file_from_ftp(base_url, ftp_directory):
    create_folder()
    try:
        ftp = FTP(base_url)
        ftp.login() 

        ftp.cwd(ftp_directory)

        files = ftp.nlst()
        print("Arquivos disponíveis no FTP:", files)

        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            print("Erro: Nenhum arquivo CSV encontrado no diretório FTP.")
            return None

        file_name = csv_files[0]
        local_path = os.path.join('generate_queries_ans/result', file_name)
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {file_name}", local_file.write)
            print(f"Arquivo {file_name} baixado com sucesso.")
        
        ftp.quit()
        return file_name
    except Exception as e:
        print(f"Erro ao acessar o FTP: {e}")
        return None
