import spacy
from spacy.tokens import Doc, Span
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_lg")

ruler = nlp.add_pipe('entity_ruler', before='ner')

patterns = [
    {"label": "IF_CLOUSE", "pattern": [{"LEMMA": "if"}]},
    {"label": "THEN_CLOUSE", "pattern": [{"LEMMA": "then"}]},
    {"label": "AND_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True}, {"LOWER": "and"}, {"LIKE_NUM": True}]},
    {"label": "AND_CLOUSE", "pattern": [{"LOWER": "and"}]},
    {"label": "OR_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True}, {"LOWER": "or"}, {"LIKE_NUM": True}]},
    {"label": "OR_CLOUSE", "pattern": [{"LOWER": "or"}]},
]

ruler.add_patterns(patterns)

# Sample text
doc = nlp("TTabelaRegistos must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 if CampoInteiroA of TTabelaRegistos is bigger than 10 or 12 and TTable is equal to 5 then TTable is fine.")

# Function to split sentence spans based on conjunctions and clauses
def split_sentence_spans(doc):
    if_start = 0
    clause_spans = []
    current_clause = None

    for token in doc:
        if token.ent_type_ == "IF_CLOUSE":
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i
            current_clause = "IF"
        elif token.ent_type_ == "THEN_CLOUSE":
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i
            current_clause = "THEN"
        elif token.ent_type_ in ("AND_CLOUSE", "OR_CLOUSE"):
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i

    if if_start != 0:
        clause_spans.append(Span(doc, if_start, len(doc)))

    return [span for span in clause_spans if span.text.strip()]

# Split the document into spans
clause_spans = split_sentence_spans(doc)

def classify_spans(clause_spans):
    main_CLOUSE = {
        "MAIN": [],
        "AND_MAIN": [],
        "OR_MAIN": []
    }
    if_CLOUSE = {
        "IF_MAIN": [],
        "IF_AND_MAIN": [],
        "IF_OR_MAIN": [],
        "THEN": []
    }
    
    current_clause = "MAIN"
    
    for span in clause_spans:
        if any(token.ent_type_ == "IF_CLOUSE" for token in span):
            current_clause = "IF_MAIN"
            if_CLOUSE[current_clause].append(span[1:].text.strip())  # Skip the first token ("if")
        elif any(token.ent_type_ == "THEN_CLOUSE" for token in span):
            current_clause = "THEN"
            if_CLOUSE[current_clause].append(span[1:].text.strip())  # Skip the first token ("then")
        elif any(token.ent_type_ == "AND_CLOUSE" for token in span):
            if current_clause == "IF_MAIN":
                if_CLOUSE["IF_AND_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("and")
            else:
                main_CLOUSE["AND_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("and")
        elif any(token.ent_type_ == "OR_CLOUSE" for token in span):
            if current_clause == "IF_MAIN":
                if_CLOUSE["IF_OR_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("or")
            else:
                main_CLOUSE["OR_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("or")
        else:
            if current_clause == "IF_MAIN":
                if_CLOUSE[current_clause].append(span.text.strip())
            else:
                main_CLOUSE["MAIN"].append(span.text.strip())
    
    return main_CLOUSE, if_CLOUSE

main_CLOUSE, if_CLOUSE = classify_spans(clause_spans)

print("main_CLOUSE:", main_CLOUSE)
print("if_CLOUSE:", if_CLOUSE)

dic_main_CLOUSE = {
    "MAIN": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
    "AND": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
    "OR": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
}

dic_if_CLOUSE = {
    "MAIN": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
    "AND": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
    "OR": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
    "THEN": {
        "1": [
            {"Subject": None},
            {"Object": None},
            {"Preposision": None},
            {"NUM": None}
        ]
    },
}

print(dic_main_CLOUSE)
