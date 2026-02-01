import json
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from services.cleaner import clean_text
import os

def train_model():
    print("🚀 Starting model training pipeline...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'job_roles.json')
    model_dir = os.path.join(base_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    with open(data_path, 'r', encoding='utf-8') as f:
        job_roles = json.load(f)

    df = pd.DataFrame(job_roles)
    print("Columns found in JSON:", df.columns.tolist())

    # 🔥 Auto detect columns
    possible_title_cols = ['title', 'role', 'job_title', 'name']
    possible_desc_cols = ['description', 'skills', 'job_description', 'desc']

    title_col = next((c for c in possible_title_cols if c in df.columns), None)
    desc_col = next((c for c in possible_desc_cols if c in df.columns), None)

    if not title_col or not desc_col:
        print("❌ Could not detect title/description columns automatically.")
        return

    print(f"Using '{title_col}' as title and '{desc_col}' as description.")

    df['clean_text'] = df[desc_col].apply(clean_text)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['clean_text'])

    # Save artifacts
    with open(os.path.join(model_dir, 'tfidf.pkl'), 'wb') as f:
        pickle.dump(tfidf, f)

    with open(os.path.join(model_dir, 'job_vectors.pkl'), 'wb') as f:
        pickle.dump(tfidf_matrix, f)

    with open(os.path.join(model_dir, 'job_roles.pkl'), 'wb') as f:
        pickle.dump(df[title_col].tolist(), f)

    print("✅ Training complete!")
    print("Vocabulary size:", len(tfidf.vocabulary_))
    print("Matrix shape:", tfidf_matrix.shape)

if __name__ == "__main__":
    train_model()
