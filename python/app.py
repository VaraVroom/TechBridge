import spacy
from spacy.matcher import Matcher
import PyPDF2
import os

# Load the Spacy English model
nlp = spacy.load('en_core_web_sm')
import csv 
from spacy.matcher import Matcher
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from ftfy import fix_text
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
stopw  = set(stopwords.words('english'))
from pyresparser import ResumeParser
import os
from docx import Document

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/jobs', methods=['POST'])
def recommend_jobs():

    file_path=r'utils/skills.csv'
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        skills = [row for row in csv_reader]
    skill_patterns = [[{'LOWER': skill}] for skill in skills[0]]
    matcher = Matcher(nlp.vocab)
    for pattern in skill_patterns:
        matcher.add('Skills', [pattern])
    # Load dataset:
    jd_df=pd.read_csv(r'utils/jd_structured_data.csv')

    # Load the extracted resume skills:
    file = request.files['resume']
    if not file:
         return jsonify({'error': 'No file provided'}), 400

    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    skills=[]
    skills.append(' '.join(word for word in skills_extractor(file_path,matcher)))
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
    tfidf = vectorizer.fit_transform(skills)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
    jd_test = (jd_df['Processed_JD'].values.astype('U'))
    distances, indices = getNearestN(jd_test,vectorizer,nbrs)
    test = list(jd_test)
    matches = []
    for i,j in enumerate(indices):
        dist=round(distances[i][0],2)
        temp = [dist]
        matches.append(temp)
    matches = pd.DataFrame(matches, columns=['Match confidence'])
    jd_df['match']=matches['Match confidence']
    recommendation= jd_df.head(5).sort_values('match')
    job_data = recommendation.to_dict(orient='records')
    return jsonify({'recommendations': job_data})

def getNearestN(query,vectorizer,nbrs):
  queryTFIDF_ = vectorizer.transform(query)
  distances, indices = nbrs.kneighbors(queryTFIDF_)
  return distances, indices

def extract_skills(text,matcher):
    doc = nlp(text)
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        skills.add(skill)
    return skills

def extract_text_from_pdf(file_path:str):
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def skills_extractor(file_path,matcher):
        # Extract text from PDF
        # path=r'notebook'
        # full_file_path = os.path.join(path, file_path)
        resume_text = extract_text_from_pdf(file_path)

        # Extract skills from resume text
        skills = list(extract_skills(resume_text,matcher))
        return skills

def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

@app.route('/courses', methods=['POST'])
def recommend_courses():
    print("***************************")
    data = request.get_json()
    keyword = data.get('keyword', '')
    data = pd.read_csv("utils/Online_Courses.csv")
    data['Level'].fillna('')
    data = data[['Title', 'URL', 'Category', 'Sub-Category', 'Course Type', 'Skills', 'Site', 'Duration', 'Instructors']]
    data.drop(data[data['Course Type'] == 'Project'].index,inplace=True)
    categories = ['Data Science', 'Business', 'Computer Science', 'Information Technology', 'Physical Science and Engineering']
    data = data[data['Category'].isin(categories)]
    data['tags'] = data['Title'] + ' ' + data['Category'] + ' ' + data['Skills']
    data['tags'] = data['tags'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['tags'])
    keyword_vector = tfidf.transform([keyword])
    
    similarity_scores = cosine_similarity(keyword_vector, tfidf_matrix)

    similar_indices = similarity_scores.argsort()[0][-5:][::-1]
    recommendations = data.iloc[similar_indices][['Title', 'URL', 'Duration', 'Site']]
    recommendations= recommendations.to_dict(orient='records')
    print("******************************")
    return jsonify({"recommendations":recommendations}) 


if __name__ == '__main__':
    app.run(debug=True)