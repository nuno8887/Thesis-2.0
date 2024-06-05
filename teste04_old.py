import spacy
from spacy.tokens import Doc
import re


# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

def create_doc_with_custom_pos(text, custom_pos_tags):

    # Replace "more or equal than" with "no less than" (case-insensitive)
    #text = re.sub(r"more or equal than", "no less than", text, flags=re.IGNORECASE)
    # Tokenize the text to get words and spaces
    tokens = nlp(text)
    words = [token.text for token in tokens]
    spaces = [token.whitespace_ for token in tokens]

    # Create a new Doc object
    doc = Doc(nlp.vocab, words=words, spaces=spaces)

    # Assign custom POS tags
    for token in doc:
        if token.text in custom_pos_tags:
            detailed_tag, universal_tag, dependency = custom_pos_tags[token.text]
            token.tag_ = detailed_tag
            token.pos_ = universal_tag
            token.dep_ = dependency
            # Check if "is" is the head of a dependency and if so, change to AUX
            if token.text == "is" and any(child.dep_ != "ROOT" for child in token.children):
                token.pos_ = "AUX"
            

        

    # Re-parse the doc with the dependency parser
    for pipe in nlp.pipe_names:
        if pipe != "parser":
            nlp.get_pipe(pipe)(doc)

    nlp.get_pipe("parser")(doc)

    return doc

# Define the custom POS tags (using 'VB' tag for specific tokens)
custom_pos_tags = {
    "jogar": ("VB", "VERB","ROOT"),
    "AAS": ("VB", "VERB","ROOT"),
    "LOL": ("VB", "VERB","ROOT"), 
    "TCURSO": ("VB", "VERB","ROOT"),
}

# The group of 3 teams scored 10 and 12 points in 2 and 3 matches during more than 5 tournaments.
# The group has a size of more or equal than 200 words.
# The group as 5 tournaments.

# The CampoInteiroA of TTabelaRegistos must be a value between 10 and 20.
# The CampoInteiroA of TTabelaRegistos must be smaller or equal to 20.
# Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos.
# Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA is bigger than 10.
# Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA of TTabelaRegistos is bigger than 10.
#
#
text = "CampoInteiroA of TTabelaRegistos is bigger than 10"

# Create a new Doc with custom POS tags and parse the dependencies
new_doc = create_doc_with_custom_pos(text, custom_pos_tags)

def get_subject(sentence):
    subjects = []
    subject_details = {}
    for token in sentence:
        # Check for nsubj, nsubjpass, or if the token is a noun and the root
        if token.dep_ in ("nsubj", "nsubjpass") or (
            token.pos_ == "NOUN" and token.dep_ == "ROOT"
        ):
            subject_parts = [
                child.text for child in token.lefts if child.dep_ == "compound"
            ]
            subject_parts.append(token.text)
            subject_text = " ".join(subject_parts)
            subjects.append(subject_text)
            subject_details[subject_text] = {"token": token, "children": token.children}
    if subjects:
        return subjects[0], subject_details[subjects[0]]
    return None, None



def get_main_verb(sentence):
    root_token = None  # Store the root token
    for token in sentence:
        if token.dep_ == "ROOT":
            root_token = token  # Found the root, but might be AUX

    # Check if the root is an auxiliary verb
    if root_token and root_token.pos_ == "VERB" and root_token.tag_ != "VBZ":  
        return root_token.text

    # If the root was AUX, search for a different main verb
    for token in sentence:
        if token.pos_ == "VERB" and token.dep_ != "aux":
            return token.text

    return None

def get_direct_objects(sentence):
    direct_objects = [token.text for token in sentence if token.dep_ == "dobj"]
    return direct_objects


# for pobj--------------------------------------------------------------------------------------
def get_prepositional_objects_and_numbers(sentence):
    prepositional_objects = []
    pobj_numbers = {}
    child_numbers = {}
    
    for token in sentence:
        if token.dep_ == "pobj" and not token.like_num:
            prepositional_objects.append(token.text)
            if token.text not in pobj_numbers:
                pobj_numbers[token.text] = []
                child_numbers[token.text] = []
            
            # Collect numbers associated with this prepositional object
            for child in token.children:

                if child.dep_ == "nummod":
                    pobj_numbers[token.text].append(child.text)
                    # Collect children of the child, excluding numbers
                    children_texts = [c.text for c in child.children if not c.like_num]
                    if children_texts:
                        concatenated_text = " ".join(children_texts)
                        child_numbers[token.text].append(concatenated_text)
                    
                    # Print the children of the child
                    print(f"Children of {child.text}: {children_texts}")
                    
                    # Handle conjunctions directly related to the number
                    for conj in child.conjuncts:
                        if conj.dep_ == "conj" and conj.like_num:
                            pobj_numbers[token.text].append(conj.text)
                            # Exclude adding conjunction numbers to children
    
    return prepositional_objects, pobj_numbers, child_numbers

#--------------------------------------------------------------------------------------------------------

# for doj -----------------------------------------------------------------------------------------------

def get_direct_objects_and_numbers(sentence):
    prepositional_objects = []
    pobj_numbers = {}
    child_numbers = {}
    
    for token in sentence:
        if token.dep_ == "dobj" and not token.like_num:
            prepositional_objects.append(token.text)
            if token.text not in pobj_numbers:
                pobj_numbers[token.text] = []
                child_numbers[token.text] = []
            
            # Collect numbers associated with this prepositional object
            for child in token.children:

                if child.dep_ == "nummod":
                    pobj_numbers[token.text].append(child.text)
                    # Collect children of the child, excluding numbers
                    children_texts = [c.text for c in child.children if not c.like_num]
                    if children_texts:
                        concatenated_text = " ".join(children_texts)
                        child_numbers[token.text].append(concatenated_text)
                    
                    # Print the children of the child
                    print(f"Children of {child.text}: {children_texts}")
                    
                    # Handle conjunctions directly related to the number
                    for conj in child.conjuncts:
                        if conj.dep_ == "conj" and conj.like_num:
                            pobj_numbers[token.text].append(conj.text)
                            # Exclude adding conjunction numbers to children
    
    return prepositional_objects, pobj_numbers, child_numbers

#--------------------------------------------------------------------------------------------------------
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

def get_related_info_pobj(sentence):
    related_info = {}
    for token in sentence:
        if token.dep_ == "prep":
            # Start with the preposition
            prep_phrase = [token.text] 
            # Iterate backwards to capture the whole phrase
            current_token = token
            while current_token.i > 0:
                previous_token = sentence[current_token.i - 1]
                if previous_token.pos_ in ("ADJ", "ADV", "CCONJ"):
                    prep_phrase.insert(0, previous_token.text)
                    current_token = previous_token
                else:
                    break  # Stop when we reach a non-phrase word
            prep_phrase = " ".join(prep_phrase)

            objects = []
            for child in token.children:
                if child.dep_ == "pobj":
                    objects.append(child.text)

            if objects:
                related_info[prep_phrase] = objects

    return related_info



def get_related_info_dobj(sentence):
    related_info = {}
    for token in sentence:
        if token.dep_ == "dobj":
            if token.head.text not in related_info:
                related_info[token.head.text] = []
            related_info[token.head.text].append(token.text)
    return related_info


for sentence in new_doc.sents:
    subject, subject_details = get_subject(sentence)
    verb = get_main_verb(sentence)
    direct_objects, dobj_numbers, dobj_child_numbers = get_direct_objects_and_numbers(sentence)
    prepositional_objects, pobj_numbers, child_numbers = get_prepositional_objects_and_numbers(sentence)
    subject_numbers, dobj_numbers = get_numbers_linked_to_subject_or_object(sentence)
    
    related_info_pobj = get_related_info_pobj(sentence)
    related_info_dobj = get_related_info_dobj(sentence)

    print()
    print("---------------------------------------------------------------")
    print(f"Sentence: {sentence}")
    print(f"Subject: {subject}")
    print(f"Subject Numbers: {subject_numbers}")
    print()
    print(f"Verb: {verb}")
    print()
    print(f"Direct Objects: {direct_objects}")
    print(f"Direct Object Numbers: {dobj_numbers}")
    print(f"Direct Object Numerical Modifiers: {dobj_child_numbers}")
    print(f"Related Info for the Direct Object: {related_info_dobj}")
    print()
    print(f"Prepositional Objects: {prepositional_objects}")
    print(f"Prepositional Object Numbers: {pobj_numbers}")
    print(f"Preposisitional Numerical Modifiers: {child_numbers}")
    print(f"Related Info for the Prepositions: {related_info_pobj}")
    print("---------------------------------------------------------------")

    for token in sentence:
        print(f"{token.text}: {token.tag_}, {token.pos_}, {token.dep_}, {token.head.text}")

    # Verify the modifications
    for token in new_doc:
        if token.text in custom_pos_tags:
            print(f"Modified POS tag for '{token.text}': {token.tag_}, UD POS tag: {token.pos_}")