import sys
import os
from flask import Flask, jsonify
from download_files_ans.download_file import downloadFile
from src.file_processor import find_top_values
from src.db import fetch_nome_fantasia_by_reg_ans
from datetime import datetime

app = Flask(__name__)

@app.route('/top_values', methods=['GET'])
def get_top_values():
    # Baixar o arquivo e processar os dados
    downloadFile()

    last_year = datetime.now().year - 1
    quarter = 4
    path_csv = f"download_files_ans/ans_files/{last_year}/{quarter}T{last_year}.csv"

    top_values = find_top_values(path_csv, "VL_SALDO_FINAL")

    reg_ans_list = [item['REG_ANS'] for item in top_values]
    list = fetch_nome_fantasia_by_reg_ans("plano_saude_ativas", reg_ans_list)

    # Criar a resposta no formato JSON
    response = {
        "top_values": top_values,
        "operadoras": list
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
