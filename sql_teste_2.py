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
                for num_key, num_values in value.items():
                    if num_key == 'BETWEEN':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} BETWEEN {num_condition}")
                    elif num_key == 'LESS_THAN':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} < {num_condition}")
                    elif num_key == 'LESS_EQUAL':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} <= {num_condition}")
                    elif num_key == 'BIGGER_THAN':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} > {num_condition}")
                    elif num_key == 'BIGGER_EQUAL':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} >= {num_condition}")
                    elif num_key == 'EQUAL_TO':
                        num_condition = num_values[0]
                        clauses.append(f"{subject} = {num_condition}")
            elif key == 'Relations':
                # Do nothing with 'Relations'
                pass
    return table_name, " AND ".join(clauses)

def build_clauses(dic_section, logical_op="AND"):
    clauses = []
    table_name = ""
    for condition_group in dic_section:
        for key, value in condition_group.items():
            table_name, clause = process_conditions(value)
            clauses.append(clause)
    return table_name, f" {logical_op} ".join(clauses)

def build_sql_query(dic_main, dic_if):
    main_clauses = []
    and_clauses = []
    or_clauses = []
    then_clauses = []
    table_name = ""

    if 'MAIN' in dic_main and dic_main['MAIN']:
        table_name, main_clause = build_clauses(dic_main['MAIN'])
        main_clauses.append(f"({main_clause})")
    
    if 'AND' in dic_main and dic_main['AND']:
        _, and_clause = build_clauses(dic_main['AND'])
        and_clauses.append(f"({and_clause})")
    
    if 'OR' in dic_main and dic_main['OR']:
        _, or_clause = build_clauses(dic_main['OR'], logical_op="OR")
        or_clauses.append(f"({or_clause})")
    
    main_where_clause = " AND ".join(main_clauses)
    
    if and_clauses:
        main_where_clause += " AND " + " AND ".join(and_clauses)
    
    if or_clauses:
        if main_where_clause:
            main_where_clause = f"({main_where_clause}) OR " + " OR ".join(or_clauses)
        else:
            main_where_clause = " OR ".join(or_clauses)

    if_clauses = []
    if 'MAIN' in dic_if and dic_if['MAIN']:
        _, if_main_clause = build_clauses(dic_if['MAIN'])
        if_clauses.append(f"({if_main_clause})")
    
    if 'AND' in dic_if and dic_if['AND']:
        _, if_and_clause = build_clauses(dic_if['AND'])
        if_clauses.append(f"({if_and_clause})")
    
    if 'OR' in dic_if and dic_if['OR']:
        _, if_or_clause = build_clauses(dic_if['OR'], logical_op="OR")
        if_clauses.append(f"({if_or_clause})")
    
    if 'THEN' in dic_if and dic_if['THEN']:
        _, then_clause = build_clauses(dic_if['THEN'])
        if_clauses.append(f"({then_clause})")

    if_where_clause = " AND ".join(if_clauses)

    final_where_clause = f"({main_where_clause}) AND ({if_where_clause})"

    sql_query = f"SELECT * FROM {table_name} WHERE\n  {final_where_clause.replace(' AND ', '\n  AND ').replace(' OR ', '\n  OR ')};"
    return sql_query

# Example dictionaries
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
                  {'Relations': {'CampoInteiroC': '50 and 60'}}]},
           {'4': [{'Subject': 'CampoInteiroD'},
                  {'Object': None},
                  {'Preposision': 'TTabelaRegistos'},
                  {'NUM': {'BIGGER_THAN': ['70']}},
                  {'Relations': {'CampoInteiroD': '70 and 80'}}]}]
}

dic_if_CLOUSE = {
    'AND': [{'5': [{'Subject': 'CampoInteiroE'},
                   {'Object': None},
                   {'Preposision': 'TTabelaRegistos'},
                   {'NUM': {'LESS_EQUAL': ['100']}},
                   {'Relations': {'CampoInteiroE': '90 and 100'}}]}],
    'MAIN': [{'6': [{'Subject': 'CampoInteiroF'},
                    {'Object': None},
                    {'Preposision': 'TTabelaRegistos'},
                    {'NUM': {'EQUAL_TO': ['115']}},
                    {'Relations': {'CampoInteiroF': '110 and 120'}}]}],
    'OR': [{'7': [{'Subject': 'CampoInteiroG'},
                  {'Object': None},
                  {'Preposision': 'TTabelaRegistos'},
                  {'NUM': {'LESS_THAN': ['140']}},
                  {'Relations': {'CampoInteiroG': '130 and 140'}}]},
           {'8': [{'Subject': 'CampoInteiroH'},
                  {'Object': None},
                  {'Preposision': 'TTabelaRegistos'},
                  {'NUM': {'BIGGER_EQUAL': ['150']}},
                  {'Relations': {'CampoInteiroH': '150 and 160'}}]}],
    'THEN': [{'9': [{'Subject': 'CampoInteiroI'},
                    {'Object': None},
                    {'Preposision': 'TTabelaRegistos'},
                    {'NUM': {'BETWEEN': ['160 and 170']}},
                    {'Relations': {'CampoInteiroI': '160 and 170'}}]}]
}

# Building the SQL query
sql_query = build_sql_query(dic_main_CLOUSE, dic_if_CLOUSE)

print(sql_query)
