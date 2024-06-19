def process_conditions(conditions):
    clauses = []
    table_name = ""
    for condition in conditions:
        for key, value in condition.items():
            if key == 'Subject':
                subject = value
            elif key == 'Object':
                obj = value
            elif key == 'Preposision':
                table_name = value
            elif key == 'NUM':
                num_condition = list(value.values())[0][0]
                clauses.append(f"{subject} BETWEEN {num_condition}")
            elif key == 'Relations':
                relation = list(value.values())[0]
                clauses.append(f"{subject} BETWEEN {relation}")
    return table_name, " AND ".join(clauses)

def build_clauses(dic_section):
    clauses = []
    table_name = ""
    for condition_group in dic_section:
        for key, value in condition_group.items():
            table_name, clause = process_conditions(value)
            clauses.append(clause)
    return table_name, " AND ".join(clauses)

def build_sql_query(dic_main):
    main_clauses = []
    and_clauses = []
    or_clauses = []
    table_name = ""

    if 'MAIN' in dic_main and dic_main['MAIN']:
        table_name, main_clause = build_clauses(dic_main['MAIN'])
        main_clauses.append(f"({main_clause})")
    
    if 'AND' in dic_main and dic_main['AND']:
        _, and_clause = build_clauses(dic_main['AND'])
        and_clauses.append(f"({and_clause})")
    
    if 'OR' in dic_main and dic_main['OR']:
        _, or_clause = build_clauses(dic_main['OR'])
        or_clauses.append(f"({or_clause})")
    
    where_clause = " AND ".join(main_clauses)
    
    if and_clauses:
        where_clause += " AND " + " AND ".join(and_clauses)
    
    if or_clauses:
        where_clause += " OR " + " OR ".join(or_clauses)
    
    sql_query = f"SELECT * FROM {table_name} WHERE {where_clause};"
    return sql_query

# Example dictionary
dic_main_CLOUSE = {
    'AND': [{'2': [{'Subject': 'CampoInteiroB'},
                   {'Object': None},
                   {'Preposision': 'TTabelaRegistos'},
                   {'NUM': {'BETWEEN': ['30 and 40']}},
                   {'Relations': {'CampoInteiroB': '30 and 40'}}]}],
    'MAIN': [{'1': [{'Subject': 'CampoInteiroA'},
                    {'Object': None},
                    {'Preposision': 'TTabelaRegistos'},
                    {'NUM': {'BETWEEN': ['10 and 20']}},
                    {'Relations': {'CampoInteiroA': '10 and 20'}}]}],
    'OR': [{'3': [{'Subject': 'CampoInteiroC'},
                  {'Object': None},
                  {'Preposision': 'TTabelaRegistos'},
                  {'NUM': {'BETWEEN': ['50 and 60']}},
                  {'Relations': {'CampoInteiroC': '50 and 60'}}]}]
}

# Building the SQL query
sql_query = build_sql_query(dic_main_CLOUSE)

print(sql_query)
