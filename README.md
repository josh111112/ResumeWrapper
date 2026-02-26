# ResumeWrapper

A Streamlit application that tailors your resume based on a specific job description using Google Gemini.

## Features
- Paste the Job Description
- Automatically generates a tailored LaTeX Resume using your provided template and profile
- Smart categorization of skills to highlight relevant technologies while retaining your baseline engineering breadth

## Setup & Installation

1.  **Clone the repository**
2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Set up your environment variables**:
    ```bash
    cp .env.example .env
    ```
    *Open `.env` and add your Google Gemini API Key.*
4.  **Customize your profile and resume template**:
    ```bash
    cp user_profile_example.md user_profile.md
    cp resume_template_example.tex resume_template.tex
    ```
    *Edit `user_profile.md` to contain your skills and experience.*
    *Edit `resume_template.tex` to contain your LaTeX resume template format.*
5.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage
- Enter your Google Gemini API Key in the .env file.
- change the user_profile_example.md to match your profile.
- change resume_template_example.tex to match your template.
- change the filesnames from resume_template_example.tex to resume_template.tex and user_profile_example.md to user_profile.md
- Paste the job description.
- Click "Generate".