import streamlit as st
import os
from services.parser import extract_text
from services.predictor import JobPredictor

# Page config
st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

# Load CSS
def load_css():
    css_path = os.path.join("assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found.")

def main():
    load_css()
    
    # Hero Section
    st.markdown("""
        <div class="animate-fade-in">
            <h1 class="hero-title">AI Resume Analyzer</h1>
            <p class="hero-subtitle">Elevate your career with precision AI matching</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.header("Navigation")
        st.write("1. **Upload** your resume.")
        st.write("2. **AI Analysis** extracts skills.")
        st.write("3. **Job Match** finds your path.")
        st.info("Supported formats: PDF, DOCX, TXT")
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Upload Container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your resume here",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()

        with st.status("Analyzing Resume...", expanded=True) as status:
            st.write("Extracting data...")
            resume_text = extract_text(uploaded_file, file_ext)
            
            if resume_text:
                st.write("Running AI engine...")
                predictor = JobPredictor()
                results = predictor.predict(resume_text)
                status.update(label="Analysis Complete", state="complete", expanded=False)
            else:
                status.update(label="Error", state="error")
                st.error("Text extraction failed.")
                return

        if results:
            if results[0].get("role") == "Error":
                st.error(results[0].get("description"))
                return

            st.markdown('<h2 style="text-align:center; margin: 3rem 0; font-weight:600;">Strategic Job Matches</h2>', unsafe_allow_html=True)

            # Show Match Cards
            cols = st.columns(len(results))
            for i, res in enumerate(results):
                with cols[i]:
                    st.markdown(f"""
                        <div class="match-card animate-fade-in" style="animation-delay: {i*0.1}s">
                            <h3 style="font-weight:600; color:#495057;">{res['role']}</h3>
                            <div class="score-text">
                                {res['score']*100:.0f}%
                            </div>
                            <p style="color: var(--text-muted); font-size:0.9rem;">MATCH SCORE</p>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br><br>", unsafe_allow_html=True)
            
            with st.expander("Detailed Analysis"):
                st.dataframe(results, use_container_width=True)

            with st.expander("Extracted Blueprint"):
                st.text_area("Resume Text", resume_text, height=300)

if __name__ == "__main__":
    main()
