# Visão Geral  

Este repositório contém um conjunto de arquivos SQL relacionados a consultas na base de dados da Agência Nacional de Saúde Suplementar (ANS). As consultas foram organizadas para facilitar a análise de dados sobre operadoras, beneficiários e outros aspectos relevantes da regulação da saúde suplementar.  

## Requisitos  

Para executar as consultas, é necessário um banco de dados compatível com SQL. No desenvolvimento deste projeto, foi utilizado **MySQL 8.0**.  

## Modo de Uso  

1. Clone o repositório:  
   ```
   git clone https://github.com/AdrianoXavier-JR/Queries_ANS.git
   ```

2. Conecte-se ao banco de dados MySQL.  

3. Execute os seguintes scripts na ordem indicada:  
   ```sh
   python generate_queries.py
   python main.py
   ```

4. Os arquivos CSV de 2023 e 2024 serão salvos na pasta:  
   ```
   /download_files_ans/ans_files/
   ```
   O script SQL gerado será salvo em:  
   ```
   /generate_queries_ans/result/queries.sql
   ```

5. Foi criado um endpoint HTTP `GET` no `main.py` para disponibilizar os dados ao front-end. Rode o main.py e para consumir a API, basta acessar:  
   ```
   http://127.0.0.1:5000/top_values
   ```

6. A collection do Postman para testes pode ser acessada em:  
   [Collection no Postman](https://drive.google.com/file/d/19oTshWx_-cFKijb4_3Baq2S7GjxrPnv1/view?usp=sharing)  

7. Esta API foi utilizada no front-end disponível neste repositório:  
   [Front-end do projeto](https://github.com/AdrianoXavier-JR/Front_List_ANS)  

---
