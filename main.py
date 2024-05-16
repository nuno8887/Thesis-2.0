import spacy
from spacy.tokens import Doc

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

def create_doc_with_custom_pos(text, custom_pos_tags):
    """
    Create a spaCy Doc with custom POS tags for specific tokens and parse dependencies.
    
    :param text: The input text.
    :param custom_pos_tags: A dictionary where keys are token texts and values are the new POS tags.
    :return: A spaCy Doc object with custom POS tags.
    """
    # Tokenize the text to get words and spaces
    tokens = nlp(text)
    words = [token.text for token in tokens]
    spaces = [token.whitespace_ for token in tokens]

    # Create a new Doc object
    doc = Doc(nlp.vocab, words=words, spaces=spaces)

    # Assign custom POS tags
    for token in doc:
        if token.text in custom_pos_tags:
            token.tag_ = custom_pos_tags[token.text]
            #detailed_tag, universal_tag = custom_pos_tags[token.text]
            #token.tag_ = detailed_tag
            #token.pos_ = universal_tag
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
    "AAU": "VB"  # Detailed POS tag for 'AAU'
    #"AAU": ("VB", "VERB")  # Tuple of (detailed POS tag, universal POS tag)
}

# Create a new Doc with custom POS tags and parse the dependencies
new_doc = create_doc_with_custom_pos(text, custom_pos_tags)

# Print the tokens with their POS tags and dependencies
for token in new_doc:
    print(f"{token.text}: {token.tag_}, {token.pos_}, {token.dep_}, {token.head.text}")

# Verify the modifications
for token in new_doc:
    if token.text in custom_pos_tags:
        print(f"Modified POS tag for '{token.text}': {token.tag_}, UD POS tag: {token.pos_}")
