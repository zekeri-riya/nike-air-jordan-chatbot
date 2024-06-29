import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
from PIL import Image
import io
import base64
from gtts import gTTS
import pygame

# Load environment variables from .env file
load_dotenv()

pygame.mixer.init()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to get product information from the catalog
def get_product_info(catalog_url):
    response = requests.get(catalog_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch product catalog")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for product in soup.find_all('div', class_='product-card'):
        name = product.find('div', class_='product-card__title').text.strip()
        description = product.find('div', class_='product-card__subtitle').text.strip()
        price = product.find('div', class_='product-price').text.strip()
        image_tag = product.find('img', class_='product-card__img')
        image_url = image_tag['src'] if image_tag else None
        
        products.append({
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url
        })
    return products

# Function to encode the image
def encode_image(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to get product recommendations from GPT-4
def get_product_recommendations(products, user_query):
    product_descriptions = "\n".join([f"{p['name']}: {p['description']}. Price: {p['price']}" for p in products])

    prompt = f"""
    You are an expert product recommendation assistant for the Nike Air Jordan collection. 
    You have access to a catalog of products with details like name, description, price, and image URL. 
    Use this information to provide personalized recommendations to the user based on their query.

    User's query: {user_query}
    
    Product catalog:
    {product_descriptions}
    
    Based on the user's query, please provide 3 product recommendations from the Nike Air Jordan collection and explain why you recommended them.
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Function to understand image content using OpenAI vision capabilities
def analyze_image(image_url):
    encoded_image = encode_image(image_url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# Function to convert text to speech and play it using pygame
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    # Wait until the sound has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.music.stop()

# Main chatbot interface
def chatbot_interface():
    print("Welcome to Nike's Air Jordan Collection Chatbot!")
    speak_text("Welcome to Nike's Air Jordan Collection Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            speak_text("Goodbye!")
            print("Goodbye!")
            break
        products = get_product_info("https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok1")
        response = get_product_recommendations(products, user_input)
        print("NikeBot:", response)
        speak_text(response)

if __name__ == "__main__":
    chatbot_interface()
