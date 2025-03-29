import csv

def try_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return 0

def find_top_values(file_csv, column, top_n=10):
    try:
        with open(file_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = list(reader)

            if column not in reader.fieldnames:
                raise KeyError(f"A coluna '{column}' não foi encontrada no arquivo CSV.")

            filtered_rows = [
                {k.strip('"'): v for k, v in row.items()}
                for row in rows
                if row.get('DESCRICAO', '') == 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
            ]

            seen_reg_ans = {}
            for row in filtered_rows:
                reg_ans_value = row.get('REG_ANS', '')
                if reg_ans_value not in seen_reg_ans:
                    seen_reg_ans[reg_ans_value] = row

            unique_rows = list(seen_reg_ans.values())

            sorted_rows = sorted(
                unique_rows,
                key=lambda x: try_float(x.get(column, '0')),
                reverse=True
            )

            return sorted_rows[:top_n]

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return []
