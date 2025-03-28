import csv

def read_csv(csv_file_path):
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            return list(reader)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None
