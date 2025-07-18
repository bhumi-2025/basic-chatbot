import requests
import re
from datetime import datetime, timedelta
from config import NEWS_API_KEY

def extract_topic_and_count(prompt):
    # Default values
    count = 10
    topic = prompt

    # Extract number
    number_match = re.search(r'\b(\d{1,2})\b', prompt)
    if number_match:
        count = int(number_match.group(1))

    # Remove filler words
    filler_words = [
        r'give me', r'latest', r'top', r'news',
        r'development', r'about', r'related to',
        r'of', r'\d+'
    ]
    pattern = '|'.join(filler_words)
    cleaned_prompt = re.sub(pattern, '', prompt, flags=re.IGNORECASE)
    topic = cleaned_prompt.strip()

    if not topic:
        topic = "technology"

    return topic, min(count, 20)

def fetch_news(topic, count, api_key):
    # Search last 7 days for more results
    today = datetime.today()
    from_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"from={from_date}&"
        f"to={to_date}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"pageSize={count}&"
        f"apiKey={api_key}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    data = response.json()
    return data.get("articles", [])

def print_articles(articles):
    if not articles:
        print("\nNo articles found.")
        return

    print(f"\nFound {len(articles)} articles:\n")
    for idx, article in enumerate(articles, 1):
        print(f"{idx}. {article.get('title')}")
        print(f"   {article.get('url')}\n")

def main():
    print("Welcome to the News CLI!")
    while True:
        prompt = input("\nEnter your news query (or type 'exit'): ").strip()
        if prompt.lower() in ('exit', 'quit'):
            print("\nGoodbye!")
            break

        topic, count = extract_topic_and_count(prompt)
        print(f"\nSearching for {count} latest news articles about: '{topic}'\n")

        articles = fetch_news(topic, count, NEWS_API_KEY)
        print_articles(articles)

if __name__ == "__main__":
    main()
