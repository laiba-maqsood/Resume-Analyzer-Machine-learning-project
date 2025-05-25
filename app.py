
from flask import Flask, render_template, request, session
from utils.skill_extractor import extract_skills
from utils.contact_extractor import extract_contact_info
from utils.spell_checker import check_spelling
import fitz  
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import re
from difflib import get_close_matches

# Import your resource fetching function
from get_resources import search_courses

app = Flask(__name__)

app.secret_key = 'super_secret_key_123' 
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load job-role-to-skills mapping
job_data = pd.read_csv('job_skills.csv')
resume_data = pd.read_csv('resume_scores.csv')

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def match_skills(extracted_skills, required_skills, similarity_threshold=0.7):
    # Normalize both lists to lowercase
    extracted_normalized = [skill.lower().strip() for skill in extracted_skills]
    required_normalized = [skill.lower().strip() for skill in required_skills]

    found = []
    missing = []

    for req_skill in required_normalized:
        # Step 1: Exact match
        if req_skill in extracted_normalized:
            found.append(req_skill)
            continue

        # Step 2: Substring match
        if any(req_skill in skill for skill in extracted_normalized):
            found.append(req_skill)
            continue

        # Step 3: Fuzzy match
        match = get_close_matches(req_skill, extracted_normalized, n=1, cutoff=similarity_threshold)
        if match:
            found.append(req_skill)
        else:
            missing.append(req_skill)

    return found, missing
import joblib

# Load trained model and metrics
model = joblib.load('model2/resume_model.pkl')
metrics = joblib.load('model2/metrics.pkl')
train_mse = metrics['train_mse']
test_mse = metrics['test_mse']
train_r2 = metrics['train_r2']
test_r2 = metrics['test_r2']


def clean_resume_text(text):
    # Remove non-alphanumeric, URLs, and excessive whitespace
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\W+', ' ', text)
    return text.strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    jobs = job_data['job roles'].tolist()

    if request.method == 'POST':
        session['processing'] = True
        job_role = request.form['job']
        file = request.files['resume']

        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            lower_resume_text = resume_text.lower()
            contact_info = extract_contact_info(lower_resume_text)

            # Use custom spaCy NER model to extract all skills
            all_extracted_skills = extract_skills(resume_text)

            # Get required skills for the selected job role
            required_skills = job_data[job_data['job roles'] == job_role]['required skills'].values[0]
            required_skills = [skill.strip().lower() for skill in required_skills.split(',')]

            # Match resume skills against job-specific required skills
            found, missing = match_skills(all_extracted_skills, required_skills)
            matched_skills_count = len(found)
            total_required_skills = len(required_skills)
            match_percentage = (matched_skills_count / total_required_skills) * 100 if total_required_skills > 0 else 0

            # Count total words in resume
            cleaned_text = clean_resume_text(lower_resume_text)
            total_words = len(cleaned_text.split())
            known_terms = set(skill.lower() for skill in all_extracted_skills + required_skills)

            spelling_errors = check_spelling(resume_text)

            # Use model to predict score
            predicted_score = model.predict([[match_percentage, total_words]])[0]

            #Automatically fetch learning resources for missing skills
            learning_resources = {}
            for skill in missing:
                learning_resources[skill] = search_courses(skill)

            result = {
                'job': job_role,
                'found_skills': found,
                'missing_skills': missing,
                'all_extracted_skills': all_extracted_skills,
                'matched_skills': found,
                'contact_info': contact_info,
                'predicted_score': round(predicted_score, 2),
                'match_percentage': round(match_percentage, 2),
                'total_words': total_words,
                'train_mse': train_mse,
                'test_mse': test_mse,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'spelling_errors': spelling_errors,
                'learning_resources': learning_resources,  # Added here
            }
            session['processing'] = False

    return render_template('index.html', jobs=jobs, result=result)

if __name__ == '__main__':
    if not os.path.exists('lt_cache'):
        os.makedirs('lt_cache')
    app.run(debug=True)
