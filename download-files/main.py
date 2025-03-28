import requests
import os
from datetime import datetime

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
BASE_DIRECTORY = "download-files/ans-files"

def get_current_years():
    current_year = datetime.now().year
    return [current_year - 2, current_year - 1]

def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def download_zip_files(year):
    year_url = f"{BASE_URL}{year}/"
    year_directory = os.path.join(BASE_DIRECTORY, str(year))
    create_directory(year_directory)

    try:
        response = requests.get(year_url)
        response.raise_for_status()

        zip_links = [link for link in response.text.split('"') if link.endswith(".zip")]

        for zip_link in zip_links:
            download_zip_file(year_url, zip_link, year_directory)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {year_url}: {e}")

def download_zip_file(year_url, zip_link, year_directory):
    zip_url = f"{year_url}{zip_link}"
    try:
        response_zip = requests.get(zip_url)
        response_zip.raise_for_status()

        zip_path = os.path.join(year_directory, zip_link)
        with open(zip_path, "wb") as f:
            f.write(response_zip.content)

        print(f"Arquivo baixado: {zip_link} para {year_directory}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer download {zip_link}: {e}")

def main():
    create_directory(BASE_DIRECTORY)
    years = get_current_years()

    for year in years:
        download_zip_files(year)

    print("Download completo.")

if __name__ == "__main__":
    main()