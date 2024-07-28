from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
from google.generativeai import (
    GenerationConfig,
    GenerativeModel,
)
from google.generativeai.types import (
    HarmBlockThreshold,
    HarmCategory,
)
import streamlit as st


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_resource
def load_models():
    text_model_pro = GenerativeModel("gemini-pro")
    return text_model_pro

def get_gemini_pro_text_response(
    model: GenerativeModel,
    contents: str,
    generation_config: GenerationConfig,
    stream: bool = True,
):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    responses = model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=stream,
    )

    final_response = []
    for response in responses:
        try:
            final_response.append(response.text)
        except IndexError:
            final_response.append("")
            continue
    return " ".join(final_response)

st.markdown('<h1 style="text-align: center;">Vision to Action</h1>', unsafe_allow_html=True)
text_model_pro = load_models()


max_output_tokens = 4096    

idea = st.text_input(
    "Enter your project idea:  \n\n", key="idea"
)

pr_type = st.selectbox(
    "Project Type",
    ("Mobile Application", "Desktop Application", "Web Application", "Other", "None"),
    index=None,
    placeholder="Select your desired Project Type."
)
if(pr_type == "Other"):
    pr_type = st.text_input("\n")


front_end = st.multiselect("Select front-end technologies", ["React", "Angular", "Flutter", "Vue", "Other", "None"])
if(front_end == "Other"):
    front_end = st.text_input("\n")
back_end = st.multiselect("Select back-end technologies", ["Node.js", "Python (Django, Flask)", "Java", "Ruby on Rails", "Other", "None"])
if(back_end == "Other"):
    back_end = st.text_input("\n")
database = st.multiselect("Select database", ["MySQL", "PostgreSQL", "MongoDB", "Firebase", "Other", "None"])
if(database == "Other"):
    database = st.text_input("\n")
cloud_platform = st.selectbox(
    "Select cloud platform",
    ("AWS", "GCP", "Azure", "Other", "None"),
    index=None,
    placeholder=""
)
if(cloud_platform == "Other"):
    cloud_platform = st.text_input("\n")

additional_requirements = st.text_area("Additional requirements: \n\n")

prompt = f"""
Create a project outline for a {pr_type} application.

The application should:
* {idea}

Use the following technologies:
* Front-end: {front_end}
* Back-end: {back_end}
* Database: {database}
* Cloud Platform: {cloud_platform}

Additional requirements:
{additional_requirements}

Provide a detailed breakdown of the project, including:
* Core functionalities and Requirements
* Technical architecture
* Development roadmap
* Potential challenges and solutions
"""

config = {
    "temperature": 0.8,
    "max_output_tokens": max_output_tokens,
}

generate_t2t = st.button("Generate Project BluePrint", key="generate_t2t")
if generate_t2t and prompt:

    with st.spinner("Generating the BluePrint..."):
        first_tab1, first_tab2 = st.tabs(["BluePrint", "Peview"])
        with first_tab1:
            response = get_gemini_pro_text_response(
                text_model_pro,
                prompt,
                generation_config=config,
            )
            if response:
                st.write("Your BluePrint:")
                st.write(response)
            
        with first_tab2:
            st.write("Feature coming soon")