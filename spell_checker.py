import spacy
from spellchecker import SpellChecker

# Load spaCy model once globally
nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

# Assume this is your list of known skills
with open('skills_list.txt', 'r') as file:
    known_skills = [line.strip().lower() for line in file if line.strip()]

def check_spelling(text):
    doc = nlp(text)

    # Extract named entities (like LinkedIn, Microsoft, etc.)
    excluded_entities = set()
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]:
            excluded_entities.update(ent.text.lower().split())

    # Combine excluded terms with your known skills
    exclusion_list = set(known_skills).union(excluded_entities)

    spelling_errors = []
    words = text.split()

    for word in words:
        clean_word = word.strip(",.():;").lower()
        if clean_word and clean_word not in exclusion_list and not spell.known([clean_word]):
            suggestion = spell.correction(clean_word)
            if suggestion != clean_word:
                spelling_errors.append({
                    "type": "Spelling",
                    "error": word,
                    "suggestion": suggestion
                })

    return spelling_errors
