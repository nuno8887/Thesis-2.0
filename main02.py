import spacy
from spacy.tokens import Doc
import re
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from spacy import displacy

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


doc = nlp("Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA of TTabelaRegistos is bigger than 10 or 12 and TTable is equal to 5.")
#for ent in doc.ents:
 #   print(ent.text, ent.label_) 

def split_sentence_spans(doc):
    if_start = 0
    clause_spans = []

    for token in doc:
        if token.ent_type_ == "IF_CLOUSE":
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i
        elif token.ent_type_ in ("AND_CLOUSE", "OR_CLOUSE"):
            # Adjust the end index to exclude the conjunction
            clause_spans.append(Span(doc, if_start, token.i)) 
            if_start = token.i  # Move past the conjunction

    if if_start != 0:
        clause_spans.append(Span(doc, if_start, len(doc)))

    return clause_spans


clause_spans = split_sentence_spans(doc)

print (clause_spans)
for span in clause_spans:
    print(span.text)  # Print the text of each span

    # Example of accessing word-level information:
    for token in span:
        print(f"  - {token.text}: {token.pos_}, {token.dep_}, {token.tag_}")