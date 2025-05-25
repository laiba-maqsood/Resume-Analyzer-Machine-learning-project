import spacy
import re

# Load trained model
nlp = spacy.load("models/skill_ner")

# Common month names (short + long)
MONTHS = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec",
    "January", "Feburary", "August", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    "- January", "- Feburary", "- August", "- March", "- April", "- May", "- June", "- July", "- August", "- September", "- October", "- November", "- December"
}

def extract_skills(text):
    doc = nlp(text)
    skills = []

    for ent in doc.ents:
        if ent.label_ != "SKILL":
            continue

        skill = ent.text.strip()

        # Filter: URLs or domains
        if re.search(r'(https?://|www\.|\.com|linkedin\.com|github\.com|mailto:)', skill, re.IGNORECASE):
            continue

        # Filter: Month names
        if skill.lower() in MONTHS:
            continue

        # Filter: Only numbers or very short
        if skill.isdigit() or len(skill) <= 1:
            continue

        # Optional: Remove purely non-alphabetic
        if not re.search(r'[a-zA-Z]', skill):
            continue

        skills.append(skill)

    return list(set(skills))  # Remove duplicates
