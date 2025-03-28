import requests
import os
import zipfile
from datetime import datetime

url_base = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

ano_atual = datetime.now().year

anos = [ano_atual - 2, ano_atual - 1]

diretorio_destino = "demonstracoes_contabeis"
os.makedirs(diretorio_destino, exist_ok=True)

for ano in anos:
    url_ano = f"{url_base}{ano}/"
    try:
        response = requests.get(url_ano)
        response.raise_for_status() 

        links_zip = [link for link in response.text.split('"') if link.endswith(".zip")]

        for link_zip in links_zip:
            url_zip = f"{url_ano}{link_zip}"
            try:
                response_zip = requests.get(url_zip)
                response_zip.raise_for_status()

                caminho_zip = os.path.join(diretorio_destino, link_zip)
                with open(caminho_zip, "wb") as f:
                    f.write(response_zip.content)

                print(f"Arquivo baixado: {link_zip}")

            except requests.exceptions.RequestException as e:
                print(f"Erro ao baixar {link_zip}: {e}")
            except zipfile.BadZipFile:
                print(f"Arquivo ZIP corrompido: {link_zip}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url_ano}: {e}")

print("Download e extração concluídos.")