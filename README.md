# Resume-Analyzer-Machine-learning-project
This is a powerful, intelligent **Resume Analyzer web app** built with **Flask**, **Machine Learning**, and **Natural Language Processing (NLP)** that helps users:

✅ Analyze their resume  
✅ Extract technical skills  
✅ Match skills to job roles  
✅ Identify missing skills  
✅ Get a resume score  
✅ Receive learning resources for improvement  
✅ Get spell-check feedback  
✅ See contact info from the resume  

---

##  Key Features

###  1. **Resume Upload & Parsing**
- Accepts PDF resume uploads
- Extracts raw text using `PyMuPDF (fitz)`

###  2. **Skill Extraction (Custom NLP Model)**
- A **custom-trained spaCy NER model** identifies all technical skills from resume text  
- Does **not rely on predefined skill lists**
- Handles multi-word skills (e.g., “power bi”, “data visualization”)
- Achieved Precision of 92% and Recall of 90%

###  3. **Job Role-Based Skill Matching**
- You select a **job role** from dropdown (e.g., Web Developer, Backend Engineer, etc.)
- It checks how many required skills (from `job_skills.csv`) match with your resume
- Displays:
  -  Found Skills
  -  Missing Skills

###  4. **Resume Score Prediction (ML Model)**
- A **linear regression model** is trained using `resume_scores.csv`
- Predicts score based on:
  - Skill match percentage
  - Resume word count

###  5. **Spelling Suggestions (NLP-enhanced)**
- Uses `pyspellchecker` and `spaCy` to check for common typos  
- **Ignores:**
  - Names (PERSON, ORG, PRODUCT)
  - Known tech skills
- Displays spelling corrections to improve resume quality

###  6. **Contact Info Extraction**
- Automatically extracts:
  -  Email(s)
  -  Phone number(s)
  -  LinkedIn / GitHub URLs

###  7. **Learning Resources API**
- For every missing skill, the app fetches:
  -  Top courses from Udemy and Coursera via their APIs
- Helps users learn what’s needed to qualify for the selected job

---

##  Technologies Used

| Area                  | Tools/Libraries                          |
|-----------------------|------------------------------------------|
| Backend               | Flask                                    |
| Resume Text Parsing   | PyMuPDF (`fitz`)                         |
| Skill Extraction      | spaCy (custom NER model)                 |
| ML Model              | Scikit-learn (LinearRegression)          |
| Spelling Check        | spaCy + pyspellchecker                   |
| Job Skills Mapping    | CSV from scraped data (Rozee.pk)         |
| Frontend              | HTML, CSS, JavaScript (typewriter, loader) |
| Learning Resources    | Udemy / Coursera (via APIs)  |
