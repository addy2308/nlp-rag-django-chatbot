from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# --- Load faq.json from quest_ans_app/data ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of views.py
faq_path = os.path.join(BASE_DIR, "data", "faq.json")

print(f"Loading FAQ from: {faq_path}")  # Debugging

with open(faq_path, "r") as f:
    data: list = json.load(f)

df = pd.DataFrame(data)

# Text preprocessing
def preprocess_text(text: str) -> str:
    sentences = sent_tokenize(text)
    tokens = [word_tokenize(sentence) for sentence in sentences]
    all_tokens = [t for sentence in tokens for t in sentence if t.isalnum()]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower(), pos='v') for token in all_tokens]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [t for t in lemmatized_tokens if t not in stop_words]
    return ' '.join(filtered_tokens)

# Preprocess dataset questions
df['processed_question'] = df['question'].apply(preprocess_text)

vectorizer: TfidfVectorizer = TfidfVectorizer()
faq_questions_vector: pd.DataFrame = vectorizer.fit_transform(df['processed_question'])

def get_answer(user_question: str):
    user_question_processed: str = preprocess_text(user_question)
    user_question_vector: pd.DataFrame = vectorizer.transform([user_question_processed])   
    similarities = cosine_similarity(user_question_vector, faq_questions_vector)
    idx: int = similarities.argmax()
    return df.iloc[idx]['answer']

# Django view
def ask_question(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        question = request.POST.get('question')
        print(f"User asked: {question}")

        try:
            answer = get_answer(question)
            return JsonResponse({"answer": answer})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET request -> just render template
    return render(request, 'query/ask_question.html')
