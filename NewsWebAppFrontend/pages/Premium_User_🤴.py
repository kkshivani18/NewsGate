import requests 
import streamlit as st
from Login import login, decode_jwt
import jwt
import google.generativeai as genai
import re
import wikipediaapi
from dotenv import load_dotenv
import os
from transformers import pipeline

# Login and get the JWT token
ans = login(username="sai", password="premuser")
jwt_token = ans.get("jwt")

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
gemini_api_key = os.getenv('GEMINI_KEY')

# API call to fetch the news data
news_api_url = os.getenv('NEWS_API_PREM_URL')

# CSS to hide sidebar
hide_sidebar_style = """
    <style>
    .css-18e3th9 {display:none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Fetch the news from the API
def fetch_news():
    response = requests.get(news_api_url, headers={"Authorization": f"Bearer {jwt_token}"})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch news data.")
        return {}

# Function to display the news in a formatted way
def display_news(news_data):
    st.title("Premium User News Dashboard")

    if 'articles' not in news_data:
        st.error("No articles found.")
        return

    articles = news_data['articles']

    for article in articles:
        st.markdown(f"### {article['title']}")
        if article.get("urlToImage"):
            st.image(article['urlToImage'], use_column_width=True)
        author = article.get("author", "Anonymous")
        source = article['source'].get("name", "Source not known")
        st.markdown(f"**Author:** {author} | **Source:** {source}")
        description = article.get("description", "No description available.")
        st.markdown(f"**Description:** {description}")
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")

# Function to get politician data from Wikipedia
def get_politician_data(politician_name):
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
    page_py = wiki_wiki.page(politician_name)
    return page_py.text

# Function to clean the text data
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Configure Google API Key and model settings
genai.configure(api_key=gemini_api_key)
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Input prompt for constituency work
input_prompt_constituency = """
               You are an expert in analyzing political information.
               Find the search and look for the politicians initiatives.
               Generate categories for initiatives of politicians based on the provided text.
               Generate as a news report. Don't give any other information.
               """

# Input prompt for criminal records
input_prompt_criminal = """
               You are a grandmother and you are an expert in analyzing political information.
               You tell your grandchildren about the active political cases of the provided individual.
               Say it down as a news report.
               Just break down the categories, don't start with a story format, keep it formal.
               Don't give any public opinion, just the facts.
               """

# Generate responses using the AI model
def generate_gemini_response(input_prompt, politician_text, question_prompt):
    prompt = f"{input_prompt}\n\nPolitician Details:\n{politician_text}\n\nQuestion: {question_prompt}"
    response = model.generate_content(prompt)
    return response.text

# Function to display constituency work
def display_constituency_work():
    st.title("Politician Initiatives Records")
    
    politician_name = st.text_input("Enter Politician Name")
    
    question_prompt = f"Generate categories for the initiatives and schemes undertaken by {politician_name}."
    
    if st.button("Generate Response"):
        if politician_name:
            politician_data = get_politician_data(politician_name)
            if politician_data:
                response_text = generate_gemini_response(input_prompt_constituency, politician_data, question_prompt)
                st.subheader("Generated Response:")
                st.write(response_text)
            else:
                st.warning("No data available for this politician.")
        else:
            st.warning("Please enter a politician name.")

# Function to display criminal records
def display_criminal_records():
    st.title("Politician Criminal Records")

    politician_name = st.text_input("Enter Politician Name for Criminal Records")
    
    question_prompt = f"Generate different categories for the active cases of {politician_name} if there are any."
    
    if st.button("Generate Response"):
        if politician_name:
            politician_data = get_politician_data(politician_name)
            if politician_data:
                response_text = generate_gemini_response(input_prompt_criminal, politician_data, question_prompt)
                st.subheader("Generated Response:")
                st.write(response_text)
            else:
                st.warning("No data available for this politician.")
        else:
            st.warning("Please enter a politician name.")

# Main function to render the page
def main():
    # Sidebar for navigation between different sections
    st.sidebar.title("Premium User Menu")
    page = st.sidebar.radio("Select a section", ("News Dashboard", "Constituency Work", "Criminal Records"))

    if page == "News Dashboard":
        news_data = fetch_news()
        if news_data:
            display_news(news_data)
    elif page == "Constituency Work":
        display_constituency_work()
    elif page == "Criminal Records":
        display_criminal_records()

if __name__ == "__main__":
    main()
