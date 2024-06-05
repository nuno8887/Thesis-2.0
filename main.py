import spacy
from spacy.tokens import Doc
import re
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span

nlp = spacy.load("en_core_web_lg")

ruler = nlp.add_pipe('entity_ruler', before= 'ner')

patterns = [

{"label": "IF_CLOUSE", "pattern": [{"LEMMA": "if"}]},

{"label": "THEN_CLOUSE", "pattern": [{"LEMMA": "then"}]},

{"label": "AND_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True},{"LOWER": "and"}, {"LIKE_NUM": True}]},
{"label": "AND_CLOUSE", "pattern": [{"LOWER": "and"}]},

{"label": "OR_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True},{"LOWER": "or"}, {"LIKE_NUM": True}]},
{"label": "OR_CLOUSE", "pattern": [{"LOWER": "or"}]},

]

#ruler = EntityRuler(nlp, overwrite_ents=True)  # Create EntityRuler
ruler.add_patterns(patterns)


doc = nlp("Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos and TTable equal to 5.")
#for ent in doc.ents:
 #   print(ent.text, ent.label_) 

def split_sentence(doc):
    if_start = 0  # Start at the beginning of the sentence
    clauses = []

    for token in doc:
        if token.ent_type_ == "IF_CLOUSE":
            clauses.append(doc[if_start: token.i].text)  # Extract the initial part before "if"
            if_start = token.i  # Now start tracking clauses within the "if" condition
        elif token.ent_type_ == "AND_CLOUSE":  
            clauses.append(doc[if_start: token.i].text) 
            if_start = token.i
        elif token.ent_type_ =="OR_CLOUSE":  
            clauses.append(doc[if_start: token.i].text) 
            if_start = token.i

    # Last clause handling (same as before)
    if if_start != 0:
        clauses.append(doc[if_start:].text)

    return clauses


main_CLOUSE1 = {
    "MAIN":[],
    "AND_MAIN":[],
    "OR_MAIN":[]
}
if_CLOUSE1 = {
    "IF_MAIN":[],
    "IF_AND_MAIN":[],
    "IF_OR_MAIN":[]
}


clause_strings = split_sentence(doc)
print(clause_strings)