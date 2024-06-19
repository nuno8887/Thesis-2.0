import main
import pprint

def process_clauses(dic_main, dic_if):
    def extract_values(clause_section):
        subjects_objects_list = []
        for condition_group in clause_section:
            for key, conditions in condition_group.items():
                subject = None
                obj = None
                for condition in conditions:
                    for cond_key, cond_value in condition.items():
                        if cond_key == 'Subject':
                            subject = cond_value
                        elif cond_key == 'Object':
                            obj = cond_value
                if subject is not None:
                    subjects_objects_list.append(subject)
                if obj is not None:
                    subjects_objects_list.append(obj)
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

    # Create the final dictionary with MAIN[Preposition] as key
    result_dict = {}
    if dic_main.get('MAIN'):
        for condition_group in dic_main['MAIN']:
            for key, conditions in condition_group.items():
                for condition in conditions:
                    if 'Preposision' in condition:
                        preposition = condition['Preposision']
                        if preposition:
                            result_dict[preposition] = dic_main_list

    return dic_main_list, dic_if_list, result_dict

# Main script to process the phrase and build the SQL query
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
dic_main_list, dic_if_list, result_dict = process_clauses(dic_main_CLOUSE, dic_if_CLOUSE)
print()
print("dic_main_list:")
pprint.pprint(dic_main_list)
print()
print("dic_if_list:")
pprint.pprint(dic_if_list)
print()
print("Result Dictionary:")
pprint.pprint(result_dict)
