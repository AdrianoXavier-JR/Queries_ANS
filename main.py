import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))

from download_files_ans.download_file import downloadFile
from src.file_processor import find_top_values
from src.db import fetch_nome_fantasia_by_reg_ans
from datetime import datetime

def main():
    downloadFile()

    last_year = datetime.now().year - 1
    quarter = 4

    path_csv = f"download_files_ans/ans_files/{last_year}/{quarter}T{last_year}.csv"

    top_values = find_top_values(path_csv, "VL_SALDO_FINAL")

    reg_ans_list = [item['REG_ANS'] for item in top_values]

    list = fetch_nome_fantasia_by_reg_ans("plano_saude_ativas", reg_ans_list)

    print("As 10 operadoras com maiores despesas: ", list)

if __name__ == "__main__":
    main()
