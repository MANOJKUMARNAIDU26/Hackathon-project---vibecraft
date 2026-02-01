from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import re
from services.parser import extract_text
from services.predictor import JobPredictor

# Defensive imports for JobSpy
try:
    from jobspy import scrape_jobs
except ImportError:
    scrape_jobs = None

try:
    import pandas as pd
except ImportError:
    pd = None

app = FastAPI(title="Resume Intelligence API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from services.skill_extractor import extract_skills
from services.intelligence_engine import IntelligenceEngine

# Initialize Predictor and Intelligence Engine
predictor = JobPredictor()
intelligence = IntelligenceEngine()

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        resume_text = extract_text(file.file, file_ext)
        
        if not resume_text:
            return JSONResponse(
                status_code=422,
                content={"error": "Could not extract text from the provided file."}
            )

        # 1. Base Analysis
        results = predictor.predict(resume_text)
        ats_score = int(predictor.calculate_ats_score(resume_text))
        detected_skills = extract_skills(resume_text)
        
        # 2. Deep Intelligence Analysis
        deep_context = intelligence.analyze_context(resume_text)
        
        # Discover Top 3 Roles via Web
        discovered_roles = intelligence.discover_roles_via_web(detected_skills, resume_text)
        
        # Analyze Suitability for each discovered role
        role_matches = []
        for role in discovered_roles:
            suitability_data = intelligence.analyze_suitability(role, resume_text, predictor)
            role_matches.append({
                "role": role,
                "score": float(suitability_data["score"]),
                "description": suitability_data["reason"]
            })
        
        # Sort roles by score so the BEST match is always results[0]
        role_matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Generate the "Super Query" for ultra-personalized scraping (passing full results for confidence check)
        search_query = intelligence.generate_super_query(role_matches, detected_skills, resume_text)
        
        if not role_matches:
            return JSONResponse(
                status_code=500,
                content={"error": "No roles could be discovered for this profile."}
            )

        # 3. Scrape personalized suggestions based on Super Query
        job_suggestions = []
        if scrape_jobs is not None:
            try:
                # Use the top discovered role as the base for scraping if super_query isn't specific enough
                scrape_query = search_query if search_query != "Job Postings" else role_matches[0]["role"]
                
                jobs = scrape_jobs(
                    site_name=["indeed", "linkedin", "google"],
                    search_term=scrape_query,
                    location="remote",
                    results_wanted=5,
                    hours_old=72,
                    country_indeed='USA'
                )
                
                if jobs is not None and hasattr(jobs, 'empty') and not jobs.empty:
                    for _, row in jobs.iterrows():
                        job_suggestions.append({
                            "title": str(row.get('title', 'Job Opening')),
                            "company": str(row.get('company', 'Company')),
                            "url": str(row.get('job_url', '#')),
                            "platform": str(row.get('site', 'Job Board'))
                        })
            except Exception as e:
                print(f"Scraping logic execution error: {e}")

        # Fallback to search links based on Super Query
        if not job_suggestions:
            job_suggestions = [
                {"title": f"Search on LinkedIn", "company": f"Query: {search_query}", "url": f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}", "platform": "LinkedIn"},
                {"title": f"Search on Indeed", "company": f"Query: {search_query}", "url": f"https://www.indeed.com/jobs?q={search_query.replace(' ', '+')}", "platform": "Indeed"}
            ]

        # Generate Skill Roadmap for the Top Role
        skill_roadmap = intelligence.generate_skill_roadmap(role_matches[0]["role"], detected_skills)

        return {
            "role_matches": role_matches,
            "ats_score": ats_score,
            "detected_skills": detected_skills,
            "skill_roadmap": skill_roadmap,
            "deep_intelligence": {
                "projects": deep_context["projects"],
                "experience": deep_context["experience"],
                "super_query": search_query
            },
            "job_suggestions": job_suggestions,
            "extracted_text": resume_text
        }

    except Exception as e:
        import traceback
        print("Backend Error Traceback:")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal system error: {str(e)}"}
        )

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
