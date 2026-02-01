import pickle
from sklearn.metrics.pairwise import cosine_similarity
from services.cleaner import clean_text
import json
import os
import numpy as np

class JobPredictor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tfidf_path = os.path.join(self.base_dir, 'model', 'tfidf.pkl')
        self.vectors_path = os.path.join(self.base_dir, 'model', 'job_vectors.pkl')
        self.data_path = os.path.join(self.base_dir, 'data', 'job_roles.json')
        self.tfidf = None
        self.job_vectors = None
        self.job_roles = None
        self._load_models()

    def _load_models(self):
        """Loads the trained models and data from disk."""
        try:
            with open(self.tfidf_path, 'rb') as f:
                self.tfidf = pickle.load(f)
            with open(self.vectors_path, 'rb') as f:
                self.job_vectors = pickle.load(f)
            with open(self.data_path, 'r') as f:
                self.job_roles = json.load(f)
            return True
        except FileNotFoundError:
            return False

    def calculate_ats_score(self, text):
        """
        Calculates a heuristic ATS score (0-100) based on content.
        """
        score = 0
        checks = {
            "contact": ["phone", "email", "address", "linkedin", "github"],
            "education": ["education", "degree", "university", "college", "school"],
            "experience": ["experience", "work", "history", "employment", "professional"],
            "skills": ["skills", "competencies", "tools", "technologies"],
            "projects": ["projects", "personal", "github", "portfolio"]
        }
        
        lower_text = text.lower()
        
        # 1. Section Presence (50 points)
        for section, keywords in checks.items():
            if any(k in lower_text for k in keywords):
                score += 10
                
        # 2. Length/Detail Check (20 points)
        word_count = len(text.split())
        if 200 < word_count < 1500:
            score += 20
        elif word_count > 100:
            score += 10
            
        # 3. Formatting/Consistency (30 points)
        # Check for common bullet point characters
        bullets = ['•', '·', '-', '*']
        if any(b in text for b in bullets):
            score += 15
        
        # Check for year patterns (indicates chronological experience)
        import re
        years = re.findall(r'\b(20\d{2}|19\d{2})\b', text)
        if len(years) >= 2:
            score += 15
            
        return min(score, 100)

    def predict(self, resume_text, top_k=3):
        """
        Predicts top_k job roles for the given resume text.
        Returns a list of dictionaries with result details.
        """
        # Ensure models are loaded
        if self.tfidf is None or self.job_vectors is None:
            success = self._load_models()
            if not success:
               return [{"role": "Error", "score": 0.0, "description": "Models not found. Please run train_model.py first."}]
        
        # 1. Clean Text
        clean_resume = clean_text(resume_text)
        
        if not clean_resume:
             return [{"role": "Error", "score": 0.0, "description": "Resume text could not be extracted or is empty."}]

        # 2. Vectorize
        resume_vector = self.tfidf.transform([clean_resume])
        
        # 3. Calculate Similarity
        similarities = cosine_similarity(resume_vector, self.job_vectors).flatten()
        
        # 4. Get Top K
        # Check if we have fewer roles than K
        k = min(top_k, len(self.job_roles))
        top_indices = similarities.argsort()[-k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "role": self.job_roles[idx]['role'],
                "score": float(similarities[idx]),
                "description": self.job_roles[idx]['description']
            })
            
        return results
