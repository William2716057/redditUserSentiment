import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

base_url = "https://www.reddit.com/"
user = input("Enter username: ")
comments_url = base_url + user + "/comments"

try:
    # Make HTTP request to fetch user comments
    response = requests.get(comments_url)
    response.raise_for_status()  # Raise exception for bad responses

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all comment elements
        comment_elements = soup.find_all('div', class_='Comment')

        if comment_elements:
            print(f"Comments by {user}:")
            
            total_polarity = 0.0
            comment_count = 0
            
            for comment in comment_elements:
                comment_text = comment.find('p', class_='Comment__body').text.strip()
                sentiment = TextBlob(comment_text).sentiment.polarity
                total_polarity += sentiment
                comment_count += 1
                
                print(f"Comment: {comment_text}")
                print(f"Sentiment Polarity: {sentiment:.2f}\n")
            
            if comment_count > 0:
                average_polarity = total_polarity / comment_count
                print(f"Average Sentiment Polarity for {user}: {average_polarity:.2f}")
            else:
                print(f"No comments found for user '{user}'.")
        else:
            print(f"No comments found for user '{user}'.")
    else:
        print(f"Failed to fetch comments for user '{user}'. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching comments for user '{user}': {str(e)}")