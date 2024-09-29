import requests
import streamlit as st
from Login import login, decode_jwt
import jwt
import os
from dotenv import load_dotenv

ans = login(username="tanvi",password="genuser")
jwt_token = ans.get("jwt")

# Load environment variables
load_dotenv()

# API call to fetch the news data
news_api_url = os.getenv('NEWS_API_USER_URL')

# Fetch the news from the API
def fetch_news():
    response = requests.get(news_api_url, headers={"Authorization": f"Bearer {jwt_token}"})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch news data.")
        return {}

# Function to display the news in a more formatted way
def display_news(news_data):
    st.title("General User News Dashboard")

    # Check if the 'articles' key exists in the JSON response
    if 'articles' not in news_data:
        st.error("No articles found.")
        return

    articles = news_data['articles']

    for article in articles:
        # Display the title
        st.markdown(f"### {article['title']}")
        
        # Display the image if available
        if article.get("urlToImage"):
            st.image(article['urlToImage'], use_column_width=True)
        
        # Display the author and source if available
        author = article.get("author", "Anonymous")
        source = article['source'].get("name", "Source not known")
        st.markdown(f"**Author:** {author} | **Source:** {source}")
        
        # Display the description
        description = article.get("description", "No description available.")
        st.markdown(f"**Description:** {description}")
        
        # Display the link to the full article
        st.markdown(f"[Read more]({article['url']})")
        
        # Add a line separator between articles
        st.markdown("---")

# Main function to render the page
def main():
    # Fetch the news data
    news_data = fetch_news()

    # Display the formatted news articles
    if news_data:
        display_news(news_data)

if __name__ == "__main__":
    main()


