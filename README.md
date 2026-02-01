# Hackathon-project---vibecraft


AI Resume Analyzer & Job Matcher

A Streamlit web app that automates resume screening using NLP and a lightweight ML approach. The system converts resumes into TF-IDF vectors and compares them with job role skill profiles using cosine similarity to find the best job match with clear scores.


🚀 Features

Upload resume in PDF format

Automatic text extraction and cleaning

TF-IDF model trained on job role skill corpora

Cosine similarity–based job matching

Displays best match and similarity scores for all roles

Clean, modular, and reproducible architecture


🧠 How It Works

Resume PDF → text extraction

Text cleaning and preprocessing

TF-IDF vectorization (pre-trained on job roles)

Cosine similarity between resume and job vectors

Display best matched role with scores


🏗️ Project Structure
resume_webapp/
│
├── app.py
├── train_model.py
├── model/
│   ├── tfidf.pkl
│   └── job_vectors.pkl
├── data/
│   └── job_roles.json
├── services/
│   ├── parser.py
│   ├── cleaner.py
│   └── predictor.py
├── requirements.txt


🛠️ Tech Stack

Python

Streamlit

scikit-learn (TF-IDF, cosine similarity)

PyPDF2


⚙️ Setup Instructions
1️⃣ Clone the repository
git clone <your-repo-link>
cd resume_webapp

2️⃣ Install dependencies
python -m pip install -r requirements.txt

3️⃣ Train the model (one-time step)
python train_model.py

4️⃣ Run the app
python -m streamlit run app.py


📊 Output

Best matched job role

Similarity scores for all job roles

picture:  ![WhatsApp Image 2026-02-01 at 2 48 25 AM](https://github.com/user-attachments/assets/17ce691c-fa09-4d28-8dbc-f873dc88f059)



♻️ Reproducibility

Judges and users can reproduce the project by:

Installing requirements

Running train_model.py

Launching the Streamlit app


🎯 Use Cases

College placement cells

Resume shortlisting for recruiters

Students analyzing resume-job fit


📌 Note

This project uses an explainable ML approach (TF-IDF + cosine similarity) for fast, accurate, and reproducible resume filtering without heavy deep learning models.


