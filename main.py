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
            #token.tag_ = custom_pos_tags[token.text]
            detailed_tag, universal_tag = custom_pos_tags[token.text]
            token.tag_ = detailed_tag
            token.pos_ = universal_tag

            #token.tag_ = custom_pos_tags[token.text]
            #token.pos_ = "VERB" if custom_pos_tags[token.text] == "VB" else token.pos_
    
    # Re-parse the doc with the dependency parser
    for pipe in nlp.pipe_names:
        if pipe != "parser":
            nlp.get_pipe(pipe)(doc)

    nlp.get_pipe("parser")(doc)

    return doc

# Example usage
with open("data/rules.txt", "r") as f:
    text = f.read()

# Define the custom POS tags (using 'VB' tag for 'AAU')
custom_pos_tags = {
    #"AAU": "VB", # Detailed POS tag for 'AAU'
    #"LOL": "VB" 
    "jogar": ("VB", "VERB"),
    "AAS": ("VB", "VERB"),  # Tuple of (detailed POS tag, universal POS tag)
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

    # Iterate over the tokens in the sentence
    for token in sentence:
        # Check if the token is the subject
        if token.dep_ in ("nsubj", "nsubjpass"):
            # Collect all tokens that are part of the compound subject
            subject_parts = [child.text for child in token.lefts if child.dep_ == "compound"]
            subject_parts.append(token.text)
            subjects.append(" ".join(subject_parts))
            
        #para selecionar multiplos subjects pode se criar a funcionalidade aqui

    if subjects:
        return subjects[0]
    
    return None

def get_main_verb(sentence):
    for token in sentence:
        # Check if the token is the main verb (ROOT)
        if token.dep_ == "ROOT":
            return token.text
    
    return None

def get_direct_objects(sentence):
    direct_objects = [token.text for token in sentence if token.dep_ == "dobj"]
    #return direct_objects[0]
    if direct_objects:
        return direct_objects[0]
    return None

def get_prepositional_objects(sentence):
    prepositional_objects = [token.text for token in sentence if token.dep_ == "pobj"]
    if prepositional_objects:
        return prepositional_objects[0]
    return None

for sentence in new_doc.sents:

    subject = get_subject(sentence)
    verb = get_main_verb(sentence)
    direct_object = get_direct_objects(sentence)
    prepositional_object = get_prepositional_objects(sentence)
    print()
    print("---------------------------------------------------------------")
    print(f"Sentence: {sentence}")
    print(f"Subject: {subject}")
    print(f"Verb: {verb}")
    print(f"direct_object: {direct_object}")
    print(f"prepositional_object: {prepositional_object}")
    print("---------------------------------------------------------------")

    for token in new_doc:
        print(f"{token.text}: {token.tag_}, {token.pos_}, {token.dep_}, {token.head.text}")

    # Verify the modifications
    for token in new_doc:
        if token.text in custom_pos_tags:
            print(f"Modified POS tag for '{token.text}': {token.tag_}, UD POS tag: {token.pos_}")
