def generate_create_table_query(columns, table_name='plano_saude_ativas'):
    create_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    for column in columns:
        create_query += f"  `{column}` VARCHAR(255),\n"
    create_query = create_query.rstrip(',\n') + '\n);'
    return create_query

def generate_insert_queries(csv_data, columns, table_name='plano_saude_ativas'):
    insert_queries = []
    for row in csv_data:
        values = [f"'{row[column].replace('\'', '\\\'')}'" for column in columns]
        insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({', '.join(values)});"
        insert_queries.append(insert_query)
    return insert_queries
