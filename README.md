# 🤖 AI Resume Analyzer

An intelligent, state-of-the-art resume analysis tool that uses NLP and real-world job data to bridge the gap between your profile and your dream career.

<img width="1920" height="5485" alt="output" src="https://github.com/user-attachments/assets/4408ff91-f323-4e7d-8014-ad75d0861093" />



## 📁 Project Structure

```bash
resume_webapp/
├── data/                 # Job role training data and JSON configs
├── model/                # Pre-trained ML models for role prediction
├── services/             # Core logic (Parser, Intelligence Engine, Predictor)
├── static/               # Frontend assets (HTML, CSS, JS)
├── main.py               # FastAPI application entry point
├── requirements.txt      # Project dependencies
└── output.png            # Application preview
```

## 🌟 Key Features

- **📊 ATS Optimization Score**: Get an instant breakdown of how well your resume matches industry-standard Applicant Tracking Systems.
- **🔍 Deep Content Extraction**: Automatically identifies complex sections like Projects, Work Experience, and Technical Skills using heuristic parsing.
- **🌐 AI-Driven Role Discovery**: Uses web-based intelligence to suggest the top 3 career paths best suited for your unique skill set.
- **🎯 Precision Suitability Analysis**: High-precision scoring and personalized reasoning for why you are a match for specific roles.
- **🗺️ Professional Skill Roadmap**: Visualizes your progress and identifies "Missing Links" in your technical stack.
- **💼 Live Job Search**: Direct integration with job boards to find current openings based on your "Super Query."

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **NLP & ML**: Scikit-Learn, NLTK, PDFPlumber, Python-Docx
- **Search Intelligence**: DuckDuckGo Search API, JobSpy (Integration)
- **Frontend**: Vanilla HTML5, Modern CSS (Glassmorphism), JavaScript (Async/Await)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Active Internet Connection (for AI Role Discovery & Job Scraping)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd resume_webapp
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python main.py
    ```

4.  **Access the Dashboard**:
    Open `http://localhost:5000` in your web browser.

## 📖 How It Works

1.  **Upload**: Submit your resume in `.pdf`, `.docx`, or `.txt` format.
2.  **Parse**: The `IntelligenceEngine` handles deep structure analysis to extract context beyond just simple keywords.
3.  **Discovery**: The system queries the web to find trending roles that match your detected skills.
4.  **Predict**: A custom `JobPredictor` calculates suitability and ATS scores.
5.  **Roadmap**: The UI generates a visual roadmap of your skills vs. the requirements of your top-matched role.

---
*Built with ❤️ for the next generation of developers.*
