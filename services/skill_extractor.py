import re

# Comprehensive list of industry skills
SKILL_DB = [
    # Programming Languages & DSA
    "Python", "JavaScript", "Java", "C++", "C#", "SQL", "Go", "Rust", "TypeScript", "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "Dart", "Objective-C", "COBOL", "Fortran", "C", "DSA", "Data Structures", "Algorithms",
    # Frontend
    "React", "React.js", "Angular", "Vue", "HTML", "CSS", "Sass", "Tailwind", "Bootstrap", "Next.js", "Vite", "Redux", "Svelte", "jQuery", "WebAssembly", "Electron", "Three.js",
    # Backend
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", "Laravel", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "MySQL", "Oracle", "Firebase", "Supabase", "GraphQL", "REST API", "Microservices", "Apollo", "Prisma",
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins", "Terraform", "CI/CD", "Git", "GitHub", "Linux", "Nginx", "Apache", "Prometheus", "Grafana", "Ansible", "Cloudflare",
    # Domains & Databases
    "Machine Learning", "Deep Learning", "DBMS", "Database Management", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-Learn", "Spacy", "NLP", "Computer Vision", "Tableau", "PowerBI", "Large Language Models", "LLM", "OpenAI", "LangChain", "Vector Databases", "Spark", "Hadoop", "KAFKA",
    # Mobile
    "React Native", "Flutter", "Android SDK", "iOS Development", "SwiftUI", "Jetpack Compose", "Xamarin", "Cordova",
    # Tools & Methodologies
    "Jira", "Agile", "Scrum", "Kanban", "Unit Testing", "TDD", "Postman", "Swagger", "Docker Compose", "Vagrant", "UML", "SDLC",
    # Soft Skills
    "Collaboration", "Leadership", "Public Speaking", "Problem Solving", "Communication", "Critical Thinking", "Adaptability", "Teamwork",
    # Specific Domain Skills
    "Cybersecurity", "Blockchain", "Solidity", "Smart Contracts", "IoT", "Embedded Systems", "AR/VR", "Unity", "Unreal Engine"
]

def extract_skills(text):
    """
    Extracts a list of detected skills from the given text.
    Uses a hybrid approach (Regex + Tokenization) for maximum accuracy.
    """
    if not text:
        return []

    detected_skills = []
    
    # 1. Pre-process text (normalize but keep symbols)
    # Replace common separators with spaces to help boundary detection
    # but keep characters like +, #, . that are part of skills
    # Normalize hyphens to spaces for hyphen-agnostic matching
    text_processed = re.sub(r'[,;/\\()|\[\]{}]', ' ', text)
    text_processed = text_processed.replace('-', ' ')
    lower_text = " " + text_processed.lower() + " "
    
    # 2. Tokenize text for simple lookups (handles single chars like C, R better)
    tokens = set(re.findall(r'[a-zA-Z0-9+#.]+', lower_text))
    
    for skill in SKILL_DB:
        skill_lower = skill.lower()
        # Handle spaces for skills like "Problem Solving" vs "Problem-solving"
        skill_search = skill_lower.replace('-', ' ')
        
        # Scenario A: Special chars (C++, Node.js) or Single chars (C, R)
        # Regex check for precise boundary detection
        safe_skill = re.escape(skill_search)
        pattern = rf'(?<=[^a-zA-Z0-9]){safe_skill}(?=[^a-zA-Z0-9])'
        
        if re.search(pattern, lower_text):
            detected_skills.append(skill)
            continue
            
        # Scenario B: Token fallback (if regex boundaries were too strict)
        if skill_search in tokens:
            detected_skills.append(skill)
            
    return sorted(list(set(detected_skills)))
