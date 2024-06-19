import main
import pprint

def process_conditions(conditions):
    clauses = []
    table_name = ""
    for condition in conditions:
        for key, value in condition.items():
            if key == 'Subject':
                subject = value
            elif key == 'Object':
                obj = value
                if obj in ["characters", "character", "chars", "char", "extent", "distance", "span", "duration", "measurement", "magnitude", "scope", "stretch", "interval", "breadth", "height", "depth", "propongation", "reach", "range"]:  # If Object is not None
                    subject = f"LEN({subject})"
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

    if if_clauses:
        if_where_clause = " AND ".join(if_clauses)
        final_where_clause = f"({main_where_clause}) AND ({if_where_clause})"
    else:
        final_where_clause = f"({main_where_clause})"

    sql_query = f"SELECT * FROM {table_name} WHERE\n  {final_where_clause.replace(' AND ', '\n  AND ').replace(' OR ', '\n  OR ')};"
    return sql_query

def process_clauses(dic_main, dic_if):
    def extract_values(clause_section):
        subjects_objects_list = []
        for condition_group in clause_section:
            for key, conditions in condition_group.items():
                for condition in conditions:
                    for cond_key, cond_value in condition.items():
                        if (cond_key == 'Subject' or cond_key == 'Object') and cond_value is not None:
                            subjects_objects_list.append(cond_value)
        return subjects_objects_list
    
    # Process MAIN, AND, OR sections for dic_main
    main_subjects_objects = extract_values(dic_main.get('MAIN', []))
    and_subjects_objects = extract_values(dic_main.get('AND', []))
    or_subjects_objects = extract_values(dic_main.get('OR', []))

    # Combine the lists
    dic_main_list = main_subjects_objects + and_subjects_objects + or_subjects_objects

    # Process MAIN, AND, OR sections for dic_if
    if_subjects_objects = extract_values(dic_if.get('MAIN', []))
    if_and_subjects_objects = extract_values(dic_if.get('AND', []))
    if_or_subjects_objects = extract_values(dic_if.get('OR', []))
    if_then_subjects_objects = extract_values(dic_if.get('THEN', []))

    # Combine the lists
    dic_if_list = if_subjects_objects + if_and_subjects_objects + if_or_subjects_objects + if_then_subjects_objects

    # Create the final dictionary with MAIN[Preposision] as key for dic_main
    result_dict_main = {}
    if dic_main.get('MAIN'):
        for condition_group in dic_main['MAIN']:
            for key, conditions in condition_group.items():
                for condition in conditions:
                    if 'Preposision' in condition:
                        preposition = condition['Preposision']
                        if preposition:
                            result_dict_main[preposition] = dic_main_list

    # Create the final dictionary with MAIN[Preposision] as key for dic_if, or add to dic_main_list if Preposision is None
    result_dict_if = {}
    if dic_if.get('MAIN'):
        for condition_group in dic_if['MAIN']:
            for key, conditions in condition_group.items():
                for condition in conditions:
                    if 'Preposision' in condition:
                        preposition = condition['Preposision']
                        if preposition:
                            result_dict_if[preposition] = dic_if_list
                        else:
                            dic_main_list.extend(dic_if_list)

    return dic_main_list, dic_if_list, result_dict_main, result_dict_if

# Main script to process the phrase and build the SQL query
#The CampoTextoA of TTabelaRegistos must not exceed 200 characters and Camp is equal to 2 and Lamp is less than 4 and User_GDAI is equal to 5 if CampoInteiroA of TTabelaRegistos is bigger than 10.
phrase = "The CampoTextoA of TTabelaRegistos must not exceed 200 characters and Camp is equal to 2 and Lamp is less than 4 and User_GDAI is equal to 5 if CampoTesteInteiroA is bigger than 10."

docs, dic_main_CLOUSE, dic_if_CLOUSE, text = main.main(phrase)

# Print the updated dictionaries
print(text)
print()
print("dic_main_CLOUSE")
pprint.pprint(dic_main_CLOUSE)
print()
print("dic_if_CLOUSE")
pprint.pprint(dic_if_CLOUSE)
print()
print(docs)

# Build and print the SQL query
sql_query = build_sql_query(dic_main_CLOUSE, dic_if_CLOUSE)
print()
print("Generated SQL Query:")
print(sql_query)

# Process clauses and print the result
dic_main_list, dic_if_list, result_dict_main, result_dict_if = process_clauses(dic_main_CLOUSE, dic_if_CLOUSE)
print()
print("dic_main_list:")
pprint.pprint(dic_main_list)
print()
print("dic_if_list:")
pprint.pprint(dic_if_list)
print()
print("Result Dictionary (Main):")
pprint.pprint(result_dict_main)
print()
print("Result Dictionary (If):")
pprint.pprint(result_dict_if)
