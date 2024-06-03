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

# Example usage
with open("data/rules.txt", "r") as f:
    text = f.read()

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
    for token in sentence:
        if token.dep_ in ("nsubj", "nsubjpass"):
            subject_parts = [child.text for child in token.lefts if child.dep_ == "compound"]
            subject_parts.append(token.text)
            subjects.append(" ".join(subject_parts))
    if subjects:
        return subjects[0]
    return None

def get_main_verb(sentence):
    for token in sentence:
        if token.dep_ == "ROOT":
            return token.text
    return None

def get_direct_objects(sentence):
    direct_objects = [token.text for token in sentence if token.dep_ == "dobj"]
    if direct_objects:
        return direct_objects[0]
    return None

def get_prepositional_objects(sentence):
    prepositional_objects = [token.text for token in sentence if token.dep_ == "pobj"]
    if prepositional_objects:
        return prepositional_objects[0]
    return None

def get_numbers(sentence):
    numbers = [token.text for token in sentence if token.like_num]
    if numbers:
        return numbers
    return None

def get_numbers_linked_to_subject_or_object(sentence):
    subject_numbers = []
    object_numbers = []
    for token in sentence:
        if token.like_num:
            head = token.head
            while head.dep_ not in ("ROOT", "nsubj", "dobj", "pobj", "nsubjpass"):
                head = head.head
            if head.dep_ in ("nsubj", "nsubjpass"):
                subject_numbers.append(token.text)
            elif head.dep_ in ("dobj", "pobj"):
                object_numbers.append(token.text)
    return subject_numbers, object_numbers

for sentence in new_doc.sents:
    subject = get_subject(sentence)
    verb = get_main_verb(sentence)
    direct_object = get_direct_objects(sentence)
    prepositional_object = get_prepositional_objects(sentence)
    subject_numbers, object_numbers = get_numbers_linked_to_subject_or_object(sentence)

    print()
    print("---------------------------------------------------------------")
    print(f"Sentence: {sentence}")
    print(f"Subject: {subject}")
    print(f"Verb: {verb}")
    print(f"Direct Object: {direct_object}")
    print(f"Prepositional Object: {prepositional_object}")
    print(f"Subject Numbers: {subject_numbers}")
    print(f"Object Numbers: {object_numbers}")
    print("---------------------------------------------------------------")

    for token in sentence:
        print(f"{token.text}: {token.tag_}, {token.pos_}, {token.dep_}, {token.head.text}")

    # Verify the modifications
    for token in new_doc:
        if token.text in custom_pos_tags:
            print(f"Modified POS tag for '{token.text}': {token.tag_}, UD POS tag: {token.pos_}")
