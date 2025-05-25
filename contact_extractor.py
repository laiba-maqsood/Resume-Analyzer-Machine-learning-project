import re

def extract_contact_info(resume_text):
    # Initialize a dictionary to hold the contact info
    contact_info = {
        'emails': [],
        'phones': [],
        'linkedin': [],
        'github': []
    }

    # Keep your existing email pattern (unchanged)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
    contact_info['emails'] = re.findall(email_pattern, resume_text)

    # Improved phone number pattern (handles spaces, dashes, dots, parentheses)
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    contact_info['phones'] = re.findall(phone_pattern, resume_text)

    # Improved LinkedIn pattern (catches both full URLs and shortened forms)
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|pub)/[a-zA-Z0-9-]+'
    contact_info['linkedin'] = re.findall(linkedin_pattern, resume_text)

    # Improved GitHub pattern (catches both full URLs and shortened forms)
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9-]+'
    contact_info['github'] = re.findall(github_pattern, resume_text)

    return contact_info
