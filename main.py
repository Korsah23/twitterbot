#my imports 
import requests
from bs4 import BeautifulSoup
import openai

# Set up your OpenAI API key
openai.api_key = ''

# API endpoint and parameters
url = "https://newsapi.org/v2/top-headlines"
api_key = ""
parameters = {
    "apiKey": api_key,
    "country": "gb",  # Set country to "gb" for the United Kingdom
    "category": "sports",  # Set category to "sports" for sports-related news
    "q": "football"  # Set "q" parameter to "football" for football-related news
}

"""
function to make api request for the news
"""
def articleReceiver():
  try:
      response = requests.get(url, params=parameters)
      response.raise_for_status()  # Raise exception for any HTTP errors

      data = response.json()
      #print(data)
  
   # Process the response data
      articles = data["articles"]
  
      for article in articles:
          title = article["title"]
          source = article["source"]["name"]
          description = article["description"]
          link = article["url"]
          if description == None:
            description = contentScraper(link)

          #print(f"Title: {title}")
          #print(f"Source: {source}")
          #print(f"Link: {link}")
          #print(f"Description: {description}")
          #print("-" * 20)
          if description is not None:
            res= articleWriter(description)
            print(f"article:{res} source:{source}")
            break
  except requests.exceptions.RequestException as e:
      print(f"Error: {e}")



"""
function to scrape content off the page of the website 
"""
def contentScraper(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for any HTTP errors

    soup = BeautifulSoup(response.content, "html.parser")
    info = []

    # Find and process the article elements
    articles = soup.find_all(class_= "article-body")
    
    if articles is None:
      articles = soup.find_all(id="article-body")
    
   
    for article in articles:
        # Extract relevant information from the article
        contents = article.find_all("p")
        for content in contents:
          info.append(content.get_text())
       
    return " ".join(info)
    

  except requests.exceptions.RequestException as e:
      print(f"Error: {e}")
  

"""
  function that uses chatGPT api to write the news article
  
"""

def articleWriter(content):
  #print(content)
  prompt = f"Rewrite this content:{content}, give it nice title,write it as a  journalist posting on twitter making it interesting and attention grabbing using maximmum of 280 characters. avoid hashtags"

    # Generate the article
  response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=280,
        temperature=0.7,
    )

  article = response.choices[0].text.strip()
  #print(article)
  return article








  

print(articleReceiver())
