import pandas as pd
import requests
import streamlit as st
from Login import login, decode_jwt
import jwt
import os
from dotenv import load_dotenv
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

# Admin login and get the JWT token
ans = login(username="shivani", password="admin")
jwt_token = ans.get("jwt")

# Load environment variables
load_dotenv()

# API call to fetch the news data
news_api_url = os.getenv('NEWS_API_ADMIN_URL')

# Fetch the news from the API
def fetch_news():
    response = requests.get(news_api_url, headers={"Authorization": f"Bearer {jwt_token}"})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch news data.")
        return {}

# Display News Articles
def display_news(news_data):
    st.title("Admin News Dashboard")

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

# Sentiment Analysis on Articles
def analyze_sentiment(articles):
    positive_count, negative_count, neutral_count = 0, 0, 0
    category_sentiments = {}

    for article in articles:
        text = article.get("description", "")
        category = article['source'].get("name", "Unknown Category")
        
        if text:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity

            if category not in category_sentiments:
                category_sentiments[category] = {'positive': 0, 'negative': 0, 'neutral': 0}

            if polarity > 0:
                positive_count += 1
                category_sentiments[category]['positive'] += 1
            elif polarity < 0:
                negative_count += 1
                category_sentiments[category]['negative'] += 1
            else:
                neutral_count += 1
                category_sentiments[category]['neutral'] += 1

    return positive_count, negative_count, neutral_count, category_sentiments

# Display Statistics and Graphs
def display_statistics(articles):
    st.title("News Sentiment Statistics")

    positive_count, negative_count, neutral_count, category_sentiments = analyze_sentiment(articles)

    # Pie Chart for Sentiment Distribution
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_count, negative_count, neutral_count]
    
    fig, ax = plt.subplots(figsize=(2, 2))  # Adjust size for clarity
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=50, colors=['green', 'red', 'gray'],
           textprops={'fontsize': 5})
    st.subheader("Sentiment Analysis")
    ax.axis('equal')
    st.pyplot(fig)

    # Bar Chart for News Channels
    st.subheader("Sentiment by News Channels")
    channel_data = []
    for channel, sentiment_data in category_sentiments.items():
        channel_data.append({
            'Channel': channel,
            'Positive': sentiment_data['positive'],
            'Negative': sentiment_data['negative'],
            'Neutral': sentiment_data['neutral']
        })

    if channel_data:
        fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size for better readability
        sns.set(style="whitegrid")
        category_df = pd.DataFrame(channel_data).melt('Channel')
        
        # Create the bar plot
        sns.barplot(data=category_df, x='Channel', y='value', hue='variable', ax=ax)
        
        # Rotate the x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
        
        ax.set_title("News Sentiment Distribution by Channel")
        ax.set_ylabel('Count')
        ax.set_xlabel('News Channels')
        st.pyplot(fig)

    # Display count statistics
    st.markdown(f"**Total Positive Articles:** {positive_count}")
    st.markdown(f"**Total Negative Articles:** {negative_count}")
    st.markdown(f"**Total Neutral Articles:** {neutral_count}")

# Main function to render the page
def main():
    st.sidebar.title("Admin Dashboard")
    page = st.sidebar.radio("Select a section", ("News Dashboard", "News Statistics"))

    news_data = fetch_news()

    if news_data:
        if page == "News Dashboard":
            display_news(news_data)
        elif page == "News Statistics":
            articles = news_data.get('articles', [])
            if articles:
                display_statistics(articles)
            else:
                st.warning("No articles available for sentiment analysis.")

if __name__ == "__main__":
    main()


#--------------------------------------------------------------------------------------------------------------

# import requests
# import streamlit as st
# from Login import login, decode_jwt
# import jwt
# import os
# from dotenv import load_dotenv
# from textblob import TextBlob  # For sentiment analysis
# import matplotlib.pyplot as plt

# # Admin login and get the JWT token
# ans = login(username="shivani", password="admin")
# jwt_token = ans.get("jwt")

# # Load environment variables from .env file
# load_dotenv()

# # API call to fetch the news data
# news_api_url = os.getenv('NEWS_API_ADMIN_URL')

# # Fetch the news from the API
# def fetch_news():
#     response = requests.get(news_api_url, headers={"Authorization": f"Bearer {jwt_token}"})
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("Failed to fetch news data.")
#         return {}

# # Function to display the news in a formatted way
# def display_news(news_data):
#     st.title("Admin News Dashboard")

#     # Check if the 'articles' key exists in the JSON response
#     if 'articles' not in news_data:
#         st.error("No articles found.")
#         return

#     articles = news_data['articles']

#     for article in articles:
#         # Display the title
#         st.markdown(f"### {article['title']}")
        
#         # Display the image if available
#         if article.get("urlToImage"):
#             st.image(article['urlToImage'], use_column_width=True)
        
#         # Display the author and source if available
#         author = article.get("author", "Anonymous")
#         source = article['source'].get("name", "Source not known")
#         st.markdown(f"**Author:** {author} | **Source:** {source}")
        
#         # Display the description
#         description = article.get("description", "No description available.")
#         st.markdown(f"**Description:** {description}")
        
#         # Display the link to the full article
#         st.markdown(f"[Read more]({article['url']})")
        
#         # Add a line separator between articles
#         st.markdown("---")

# # Function to analyze sentiment of news articles
# def analyze_sentiment(articles):
#     positive_count = 0
#     negative_count = 0
#     neutral_count = 0
    
#     for article in articles:
#         text = article.get("description", "")
#         if text:
#             analysis = TextBlob(text)
#             if analysis.sentiment.polarity > 0:
#                 positive_count += 1
#             elif analysis.sentiment.polarity < 0:
#                 negative_count += 1
#             else:
#                 neutral_count += 1

#     return positive_count, negative_count, neutral_count

# # Function to display news sentiment statistics
# def display_statistics(articles):
#     st.title("News Sentiment Statistics")

#     # Analyze the sentiment of the news articles
#     positive_count, negative_count, neutral_count = analyze_sentiment(articles)
    
#     # Create a pie chart for sentiment distribution
#     labels = ['Positive', 'Negative', 'Neutral']
#     sizes = [positive_count, negative_count, neutral_count]
    
#     fig, ax = plt.subplots()
#     ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    
#     st.pyplot(fig)

#     # Display count statistics
#     st.markdown(f"**Positive Articles:** {positive_count}")
#     st.markdown(f"**Negative Articles:** {negative_count}")
#     st.markdown(f"**Neutral Articles:** {neutral_count}")

# # Main function to render the page
# def main():
#     # Sidebar for navigation between different sections
#     st.sidebar.title("Admin Dashboard")
#     page = st.sidebar.radio("Select a section", ("News Dashboard", "News Statistics"))

#     # Fetch the news data
#     news_data = fetch_news()

#     if news_data:
#         # Display content based on the selected section
#         if page == "News Dashboard":
#             display_news(news_data)
#         elif page == "News Statistics":
#             articles = news_data.get('articles', [])
#             if articles:
#                 display_statistics(articles)
#             else:
#                 st.warning("No articles available for sentiment analysis.")

# if __name__ == "__main__":
#     main()


#-------------------------------------------------------------------------------------------------------------

# import requests
# import streamlit as st
# from Login import login, decode_jwt
# import jwt
# import os
# from dotenv import load_dotenv

# ans = login(username="shivani",password="admin")
# jwt_token = ans.get("jwt")

# # Load environment variables from .env file
# load_dotenv()

# # API call to fetch the news data
# news_api_url = os.getenv('NEWS_API_ADMIN_URL')

# # Fetch the news from the API
# def fetch_news():
#     response = requests.get(news_api_url, headers={"Authorization": f"Bearer {jwt_token}"})
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("Failed to fetch news data.")
#         return {}

# # Function to display the news in a more formatted way
# def display_news(news_data):
#     st.title("Admin News Dashboard")

#     # Check if the 'articles' key exists in the JSON response
#     if 'articles' not in news_data:
#         st.error("No articles found.")
#         return

#     articles = news_data['articles']

#     for article in articles:
#         # Display the title
#         st.markdown(f"### {article['title']}")
        
#         # Display the image if available
#         if article.get("urlToImage"):
#             st.image(article['urlToImage'], use_column_width=True)
        
#         # Display the author and source if available
#         author = article.get("author", "Anonymous")
#         source = article['source'].get("name", "Source not known")
#         st.markdown(f"**Author:** {author} | **Source:** {source}")
        
#         # Display the description
#         description = article.get("description", "No description available.")
#         st.markdown(f"**Description:** {description}")
        
#         # Display the link to the full article
#         st.markdown(f"[Read more]({article['url']})")
        
#         # Add a line separator between articles
#         st.markdown("---")

# # Main function to render the page
# def main():
#     # Fetch the news data
#     news_data = fetch_news()

#     # Display the formatted news articles
#     if news_data:
#         display_news(news_data)    

# if __name__ == "__main__":
#     main()


