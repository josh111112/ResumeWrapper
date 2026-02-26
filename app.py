import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Generator", page_icon="📄", layout="wide")

st.title("📄 Smart Resume Tailor")
st.markdown("Paste a Job Description, and I'll tailor your resume to match it using your profile and template.")

# Initialize session state
if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = None

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input("Google API Key", type="password", help="Get your API key from Google AI Studio")
    else:
        st.success("API Key loaded from environment", icon="✅")
    
    selected_model_name = None
    client = None

    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        try:
            client = genai.Client(api_key=api_key)
            models = [m.name for m in client.models.list()]
            preferred_models = ["models/gemini-3-pro-preview"]
            default_index = 0
            if models:
                for pm in preferred_models:
                    if pm in models:
                        default_index = models.index(pm)
                        break
                    elif any(pm in m for m in models):
                        default_index = next(i for i, m in enumerate(models) if pm in m)
                        break
            else:
                models = ["gemini-2.5-flash"]
                
            selected_model_name = st.selectbox("Select Model", models, index=default_index)
        except Exception as e:
            st.error(f"Configuration/Model Error: {e}")
    else:
        st.warning("Please enter your Google API Key to proceed.")

# Paths
DEFAULT_TEMPLATE_PATH = "resume_template.tex"
USER_PROFILE_PATH = "user_profile.md"

# Load Data
try:
    with open(DEFAULT_TEMPLATE_PATH, "r") as f:
        resume_template = f.read()
except FileNotFoundError:
    st.error(f"Template file not found: {DEFAULT_TEMPLATE_PATH}")
    resume_template = None

try:
    with open(USER_PROFILE_PATH, "r") as f:
        user_profile = f.read()
except FileNotFoundError:
    st.error(f"Profile file not found: {USER_PROFILE_PATH}")
    user_profile = None

# Main Input Area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    job_description = st.text_area("Paste Job Description Here", height=400, placeholder="Paste the full job description here...")

    prompt_template = """
    You are an expert resume writer and LaTeX coder.
    
    Here is the USER'S PROFILE (Skills, Experience, Projects):
    {user_profile}
    
    Here is the JOB DESCRIPTION they are applying for:
    {job_description}
    
    Here is the LaTeX TEMPLATE they use (Style Reference):
    {resume_template}
    
    ---
    YOUR TASK:
    Generate a NEW LaTeX resume code that:
    1. **Format**: STRICTLY follows the formatting and style of the provided LaTeX TEMPLATE. Adapt the skills section to accommodate two sub-categories if needed, matching the template's visual style.
    2. **Content Tailoring**: Use the content from the USER'S PROFILE but TAILORS it to the JOB DESCRIPTION.
       - **Skills Section (CRITICAL CATEGORIZATION)**:
         - **Category 1: Core Technologies**: Analyze the Job Description. You MUST include and prioritize skills from the user profile that explicitly match the core requirements (e.g., C#, .NET, SQL).
         - **Category 2: Additional Technologies**: You MUST retain other major programming languages, frameworks, and foundational computer science skills (e.g., Swift, Python, Neo4j, microcontrollers/hardware) even if not listed in the job description, to demonstrate engineering breadth.
         - **STRICT EXCLUSION**: You MUST ruthlessly DELETE irrelevant, legacy, or non-development tools.
       - **Projects/Experience**: Highlight relevant software engineering experience. Rephrase bullet points to match the language/keywords of the job description where truthful. Remove bullet points that focus entirely on the deleted, irrelevant IT/Admin skills.
    3. **Links**: CRITICAL: You MUST preserve all hyperlinks (e.g., `\\href{{...}}`) for projects, contact info, and portfolio from the original template/profile. Do not remove or break these links.
    4. **Output**: OUTPUT ONLY valid LaTeX code.
       - Start directly with `\\documentclass` or the first line of the template.
       - Do not include markdown code fences (like ```latex or ```) or conversational text.
    """

    with st.expander("View/Edit Prompt Logic"):
        st.info(" This is the instruction sent to the AI. You can see how the inputs are combined.")
        st.code(prompt_template, language="md")

def generate_resume(client, model_name, profile, job_desc, template):
    try:
        # Fill in the prompt
        final_prompt = prompt_template.format(
            user_profile=profile,
            job_description=job_desc,
            resume_template=template
        )
        
        with st.spinner("Analyzing Job Description & Generating Resume..."):
            response = client.models.generate_content(
                model=model_name,
                contents=final_prompt
            )
            clean_text = response.text.strip()
            # Cleanup markdown fences
            if "```" in clean_text:
                lines = clean_text.split('\n')
                # Remove first line if fence
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                # Remove last line if fence
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                clean_text = "\n".join(lines)
            
            st.session_state.generated_resume = clean_text
            
        st.success("Generation Complete!")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.button("Generate Tailored Resume", type="primary"):
    if not api_key or not client:
        st.error("Please configure the API Key first.")
    elif not resume_template:
        st.error("Resume template missing.")
    elif not user_profile:
        st.error("User profile missing.")
    elif not job_description:
        st.error("Please paste a job description.")
    else:
        generate_resume(client, selected_model_name, user_profile, job_description, resume_template)

# Output Area
with col2:
    st.subheader("Result")
    if st.session_state.generated_resume:
        st.code(st.session_state.generated_resume, language='latex')
        st.download_button("Download .tex File", st.session_state.generated_resume, file_name="tailored_resume.tex")
    else:
        st.info("Generated resume code will appear here.")
