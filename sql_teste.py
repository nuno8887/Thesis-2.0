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
        result = {}
        for condition_group in clause_section:
            for key, conditions in condition_group.items():
                preposition = None
                subject = None
                obj = None
                for condition in conditions:
                    for cond_key, cond_value in condition.items():
                        if cond_key == 'Preposision':
                            preposition = cond_value
                        elif cond_key == 'Subject':
                            subject = cond_value
                        elif cond_key == 'Object':
                            obj = cond_value
                if preposition:
                    if preposition not in result:
                        result[preposition] = []
                    if subject:
                        result[preposition].append(subject)
                    if obj:
                        result[preposition].append(obj)
        return result
    
    # Process MAIN, AND, OR sections for both dictionaries
    main_result = extract_values(dic_main.get('MAIN', []))
    and_result = extract_values(dic_main.get('AND', []))
    or_result = extract_values(dic_main.get('OR', []))

    if_result = extract_values(dic_if.get('MAIN', []))
    if_and_result = extract_values(dic_if.get('AND', []))
    if_or_result = extract_values(dic_if.get('OR', []))
    if_then_result = extract_values(dic_if.get('THEN', []))

    # Combine results
    combined_result = main_result

    for key, value in and_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    for key, value in or_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    for key, value in if_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    for key, value in if_and_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    for key, value in if_or_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    for key, value in if_then_result.items():
        if key in combined_result:
            combined_result[key].extend(value)
        else:
            combined_result[key] = value

    return combined_result

# Main script to process the phrase and build the SQL query
#Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA of TTabelaRegistos is bigger than 10.
phrase = "The CampoTextoA of TTabelaRegistos must not exceed 200 characters, Camp is equal to 2, Lamp is less than 4, User_GDAI is equal to 5."

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
processed_clauses = process_clauses(dic_main_CLOUSE, dic_if_CLOUSE)
print()
print("Processed Clauses:")
pprint.pprint(processed_clauses)
