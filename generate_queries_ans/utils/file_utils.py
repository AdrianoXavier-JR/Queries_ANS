import os

def save_queries_to_file(queries, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            for query in queries:
                f.write(query + '\n')
        print(f"Queries salvas no arquivo: {file_name}")
    except Exception as e:
        print(f"Erro ao salvar queries no arquivo: {e}")