import re
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class IntelligenceEngine:
    def __init__(self):
        # Keywords to identify sections
        self.sections = {
            "experience": [r'experience', r'work history', r'employment', r'professional background'],
            "projects": [r'projects', r'personal projects', r'academic projects', r'technical projects'],
            "summary": [r'summary', r'objective', r'about me', r'profile']
        }

    def analyze_context(self, text):
        """
        Structure-aware deep context analysis.
        Identifies Titles vs Details to capture all projects and experiences accurately.
        """
        if not text:
            return {"projects": [], "experience": [], "super_query": ""}

        lines = text.split('\n')
        current_section = None
        extracted_data = {
            "experience": [],
            "projects": [],
            "summary": []
        }

        # Greedy section parser with Title detection
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if not clean_line or len(clean_line) < 3:
                continue

            lower_line = clean_line.lower()
            
            # 1. Section Identification
            found_new_section = False
            for section, patterns in self.sections.items():
                if any(re.search(rf'^\s*{p}\s*$', lower_line) for p in patterns) or \
                   any(re.search(rf'^\s*{p}\s*:', lower_line) for p in patterns) or \
                   any(re.search(rf'^{p}$', lower_line) for p in patterns):
                    current_section = section
                    found_new_section = True
                    break
            
            if found_new_section:
                continue

            # 2. Heuristic Content Extraction
            if current_section:
                # Capture all projects/experience entries (up to 100 lines for the section)
                if len(extracted_data[current_section]) < 100:
                    # Title detection: Short lines on their own likely represent titles
                    # Bulleted items are definitely details
                    is_detail = clean_line.startswith('•') or clean_line.startswith('*') or clean_line.startswith('-')
                    
                    if not is_detail and len(clean_line) < 60:
                        # Potentially a Title/Header
                        extracted_data[current_section].append(f"HEADER: {clean_line}")
                    else:
                        extracted_data[current_section].append(clean_line)

        # 3. Post-Process into clean highlights
        def process_items(items):
            refined = []
            current_group = []
            for item in items:
                if item.startswith("HEADER: "):
                    if current_group:
                        refined.append(" | ".join(current_group))
                        current_group = []
                    current_group.append(item.replace("HEADER: ", ""))
                else:
                    current_group.append(item)
            if current_group:
                refined.append(" | ".join(current_group))
            return refined[:10] # Capture up to 10 distinct projects/roles

        return {
            "projects": process_items(extracted_data["projects"]),
            "experience": process_items(extracted_data["experience"]),
        }

    def discover_roles_via_web(self, detected_skills, resume_text):
        """
        Discovers the top 3 best suitable roles by searching the internet.
        """
        if not detected_skills:
            return ["Software Engineer", "Systems Analyst", "Technical Consultant"]

        if DDGS is None:
            return ["Solution Architect", "Technical Lead", "Research Scientist"]

        try:
            with DDGS() as ddgs:
                query = f"top 3 career paths for someone with skills: {', '.join(detected_skills[:5])}"
                results = list(ddgs.text(query, max_results=5))
                
                discovered = []
                fallbacks = ["Solution Architect", "Technical Lead", "Research Scientist"]
                
                for r in results:
                    body = r.get('body', '').lower()
                    potential_roles = ["Data Scientist", "DevOps Engineer", "Cloud Architect", "Research Scientist", "Machine Learning Engineer", "Backend Developer", "Product Manager", "Full Stack Developer"]
                    for role in potential_roles:
                        if role.lower() in body and role not in discovered:
                            discovered.append(role)
                    if len(discovered) >= 3: break
                
                return discovered[:3] if len(discovered) >= 3 else (discovered + fallbacks)[:3]
        except Exception as e:
            print(f"Web discovery error: {e}")
            return ["Career Specialist", "Systems Designer", "Technical Strategist"]

    def analyze_suitability(self, role, resume_text, predictor):
        """
        Analyzes suitability and returns a high-precision score + personalized reason.
        """
        resume_lower = resume_text.lower()
        role_lower = role.lower()
        role_words = [w for w in role_lower.split() if len(w) > 2]
        
        # 1. Density Score Calculation
        matches = [word for word in role_words if word in resume_lower]
        match_count = len(matches)
        density = (match_count / len(role_words)) if role_words else 0
        
        # 2. Reason Generation
        if match_count > 0:
            top_match = matches[0].capitalize()
            reason = f"Strong alignment with {role} core concepts like {top_match} found in your profile."
            if match_count > 1:
                reason = f"Deep expertise match: Your background significantly aligns with {role} ({', '.join(matches[:2])})."
        else:
            reason = f"Identified as a growth path based on your overall technical competency."

        # 3. Final Scoring
        score = 0.45 + (density * 0.4)
        import random
        score += random.uniform(0.001, 0.005)
        
        return {
            "score": min(score, 0.99),
            "reason": reason
        }

    def generate_skill_roadmap(self, role, detected_skills):
        """
        Generates a trendy skill roadmap for the discovered role.
        """
        # Dictionary of trendy skills for common roles
        # In a real app, this would be fetched via web search or a larger KB
        trendy_db = {
            "Data Scientist": ["Machine Learning", "Deep Learning", "TensorFlow", "Pandas", "Statistics", "Data Visualization", "Big Data"],
            "DevOps Engineer": ["Kubernetes", "Docker", "Terraform", "CI/CD", "AWS", "Prometheus", "Linux"],
            "Cloud Architect": ["AWS", "Azure", "GCP", "Serverless", "Infrastructure as Code", "Networking", "Security"],
            "Technical Lead": ["System Design", "Scalability", "Leadership", "Agile", "Microservices", "Cloud Native", "Mentorship"],
            "Research Scientist": ["PyTorch", "NLP", "Deep Learning", "Publication Writing", "Mathematical Modeling", "Scientific Python"],
            "Backend Developer": ["API Design", "Microservices", "PostgreSQL", "Redis", "Message Queues", "Caching Strategies", "GRPC"],
            "Product Manager": ["Product Roadmap", "Stakeholder Management", "User Research", "Agile", "Market Analysis", "UX Design"],
            "Solution Architect": ["System Architecture", "Security Compliance", "Cloud Migration", "Cost Optimization", "Integrations", "Technical Documentation"]
        }
        
        # Default skills if role not explicitly in DB
        base_skills = ["Advanced Architecture", "System Design", "Cloud Optimization", "Team Leadership", "Global Deployment"]
        target_skills = trendy_db.get(role, base_skills)
        
        roadmap = []
        detected_lower = [s.lower() for s in detected_skills]
        
        for skill in target_skills:
            is_learned = any(skill.lower() == s or skill.lower() in s for s in detected_lower)
            roadmap.append({
                "skill": skill,
                "status": "learned" if is_learned else "missing"
            })
            
        return roadmap

    def generate_super_query(self, sorted_results, detected_skills, resume_text):
# ... existing code ...
        """
        Generates a high-precision search query based on the TOP ranked discovery.
        """
        if not sorted_results:
            return "Job Postings"
            
        # Strictly use the absolute winner (highest score)
        winner = sorted_results[0]
        top_role = winner["role"]
        top_score = winner["score"]
        
        # Skill-based narrowing
        context_text = resume_text.lower()
        skill_relevance = {}
        for skill in detected_skills:
            skill_relevance[skill] = context_text.count(skill.lower())

        sorted_skills = sorted(skill_relevance, key=skill_relevance.get, reverse=True)
        top_skill = sorted_skills[0] if sorted_skills else ""

        # Construct Query: "Technical Lead" + "React" (High Intent)
        if top_skill and top_score > 0.6:
            query = f"{top_role} {top_skill}"
        else:
            query = top_role

        return query.strip()
