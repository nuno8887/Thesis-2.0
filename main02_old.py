import spacy
from spacy.tokens import Doc

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

def create_doc_with_custom_pos(text, custom_pos_tags):
    # Tokenize the text to get words and spaces
    tokens = nlp(text)
    words = [token.text for token in tokens]
    spaces = [token.whitespace_ for token in tokens]

    # Create a new Doc object
    doc = Doc(nlp.vocab, words=words, spaces=spaces)

    # Assign custom POS tags
    for token in doc:
        if token.text in custom_pos_tags:
            detailed_tag, universal_tag = custom_pos_tags[token.text]
            token.tag_ = detailed_tag
            token.pos_ = universal_tag

    # Re-parse the doc with the dependency parser
    for pipe in nlp.pipe_names:
        if pipe != "parser":
            nlp.get_pipe(pipe)(doc)

    nlp.get_pipe("parser")(doc)

    return doc

# Example text
text = "The group of 3 teams scored 10 and 12 points in 2 and 3 matches during 5 tournaments."

# Define the custom POS tags (using 'VB' tag for specific tokens)
custom_pos_tags = {
    "jogar": ("VB", "VERB"),
    "AAS": ("VB", "VERB"),
    "LOL": ("VB", "VERB"), 
    "QQW": ("VB", "VERB"),
    "QQWA": ("VB", "VERB"),
    "EQQWA": ("VB", "VERB"),
    "EIA": ("VB", "VERB"),
}

# Create a new Doc with custom POS tags and parse the dependencies
new_doc = create_doc_with_custom_pos(text, custom_pos_tags)

def get_subject(sentence):
    subjects = []
    subject_details = {}
    for token in sentence:
        if token.dep_ in ("nsubj", "nsubjpass"):
            subject_parts = [child.text for child in token.lefts if child.dep_ == "compound"]
            subject_parts.append(token.text)
            subject_text = " ".join(subject_parts)
            subjects.append(subject_text)
            subject_details[subject_text] = {"token": token, "children": token.children}
    if subjects:
        return subjects[0], subject_details[subjects[0]]
    return None, None

def get_main_verb(sentence):
    for token in sentence:
        if token.dep_ == "ROOT":
            return token.text
    return None

def get_direct_objects(sentence):
    direct_objects = [token.text for token in sentence if token.dep_ == "dobj"]
    return direct_objects[0]

def get_prepositional_objects_and_numbers(sentence):
    prepositional_objects = []
    pobj_numbers = {}
    for token in sentence:
        if token.dep_ == "pobj" and not token.like_num:
            print(f"Found prepositional object: {token.text}")
            prepositional_objects.append(token.text)
            if token.text not in pobj_numbers:
                pobj_numbers[token.text] = []
            # Collect numbers associated with this prepositional object
            for child in token.children:
                print(f"Child of {token.text}: {child.text} ({child.dep_})")
                if child.dep_ == "nummod":
                    pobj_numbers[token.text].append(child.text)
                    print(f"  -> Added number: {child.text}")
                    # Handle conjunctions directly related to the number
                    for conj in child.conjuncts:
                        if conj.dep_ == "conj" and conj.like_num:
                            pobj_numbers[token.text].append(conj.text)
                            print(f"    -> Added conjunct number: {conj.text}")
                elif child.dep_ == "conj" and child.dep_ == "pobj":
                    for conj_child in child.children:
                        if conj_child.dep_ == "nummod":
                            pobj_numbers[token.text].append(conj_child.text)
                            print(f"  -> Added number: {conj_child.text}")
                            for conj in conj_child.conjuncts:
                                if conj.dep_ == "conj" and conj.like_num:
                                    pobj_numbers[token.text].append(conj.text)
                                    print(f"    -> Added conjunct number: {conj.text}")
    print(f"Final prepositional objects: {prepositional_objects}")
    print(f"Final prepositional object numbers: {pobj_numbers}")
    return prepositional_objects, pobj_numbers

def get_numbers_linked_to_subject_or_object(sentence):
    subject_numbers = []
    dobj_numbers = []
    for token in sentence:
        if token.like_num:
            head = token.head
            while head.dep_ not in ("ROOT", "nsubj", "dobj", "pobj", "nsubjpass"):
                head = head.head
            if head.dep_ in ("nsubj", "nsubjpass"):
                subject_numbers.append(token.text)
            elif head.dep_ == "dobj":
                dobj_numbers.append(token.text)
    return subject_numbers, dobj_numbers

def get_related_info(subject_token):
    related_info = []
    for child in subject_token.children:
        if child.dep_ == "prep":
            for pobj in child.children:
                if pobj.dep_ == "pobj":
                    related_info.append((child.text, pobj.text))
    return related_info

for sentence in new_doc.sents:
    subject, subject_details = get_subject(sentence)
    verb = get_main_verb(sentence)
    direct_objects = get_direct_objects(sentence)
    prepositional_objects, pobj_numbers = get_prepositional_objects_and_numbers(sentence)
    subject_numbers, dobj_numbers = get_numbers_linked_to_subject_or_object(sentence)
    
    related_info = get_related_info(subject_details["token"]) if subject_details else []

    print()
    print("---------------------------------------------------------------")
    print(f"Sentence: {sentence}")
    print(f"Subject: {subject}")
    print(f"Verb: {verb}")
    print(f"Direct Objects: {direct_objects}")
    print(f"Prepositional Objects: {prepositional_objects}")
    print(f"Subject Numbers: {subject_numbers}")
    print(f"Direct Object Numbers: {dobj_numbers}")
    print(f"Prepositional Object Numbers: {pobj_numbers}")
    print(f"Related Info: {related_info}")
    print("---------------------------------------------------------------")

   