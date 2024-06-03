import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def get_prepositional_objects_and_numbers(sentence):
    prepositional_objects = []
    pobj_numbers = {}
    child_numbers = {}
    
    for token in sentence:
        if token.dep_ == "pobj" and not token.like_num:
            prepositional_objects.append(token.text)
            if token.text not in pobj_numbers:
                pobj_numbers[token.text] = []
                child_numbers[token.text] = {}
            
            # Collect numbers associated with this prepositional object
            for child in token.children:
                if child.dep_ == "nummod":
                    pobj_numbers[token.text].append(child.text)
                    # Collect children of the child
                    child_numbers[token.text][child.text] = [c.text for c in child.children]
                    
                    # Print the children of the child
                    print(f"Children of {child.text}: {child_numbers[token.text][child.text]}")
                    
                    # Handle conjunctions directly related to the number
                    for conj in child.conjuncts:
                        if conj.dep_ == "conj" and conj.like_num:
                            pobj_numbers[token.text].append(conj.text)
                            child_numbers[token.text][child.text].append(conj.text)
                            
    return prepositional_objects, pobj_numbers, child_numbers

# Example phrases


# Process each phrase
for phrase in phrases:
    doc = nlp(phrase)
    prepositional_objects, pobj_numbers, child_numbers = get_prepositional_objects_and_numbers(doc)
    print(f"Prepositional objects: {prepositional_objects}")
    print(f"Numbers associated with prepositional objects: {pobj_numbers}")
    print(f"Children of numerical modifiers: {child_numbers}")
    print("-" * 50)
