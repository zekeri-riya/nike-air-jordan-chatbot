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
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

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

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert product recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    print("Debug response:", response)  # Debug print to understand the response structure

    return response.choices[0].message.content

# Function to understand image content using OpenAI vision capabilities
def analyze_image(encoded_image):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

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

# Function to upload an image file
def upload_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.destroy()  # Properly close the Tkinter window
    return file_path

# Enhanced chatbot interface
def chatbot_interface():
    print("Welcome to Nike's Air Jordan Collection Chatbot!")
    speak_text("Welcome to Nike's Air Jordan Collection Chatbot!")
    products = get_product_info("https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok1")
    
    while True:
        print("\nHow would you like to interact with the chatbot?")
        print("1. Text Query")
        print("2. Image and Text Query")
        print("3. Text and Voice Query")
        print("Type 'exit' or 'quit' to end the session.")
        
        choice = input("Your choice: ").strip().lower()
        
        if choice in ['exit', 'quit']:
            speak_text("Goodbye!")
            print("Goodbye!")
            break
        
        if choice == '1':
            user_input = input("Enter your text query: ").strip()
            response = get_product_recommendations(products, user_input)
        
        elif choice == '2':
            user_input = input("Enter your text query: ").strip()
            image_path = upload_image()
            if image_path:
                encoded_image = encode_image(image_path)
                image_analysis = analyze_image(encoded_image)
                print("Image Analysis:", image_analysis)
                response = get_product_recommendations(products, user_input)
            else:
                response = "No image uploaded."
        
        elif choice == '3':
            user_input = input("Enter your text query: ").strip()
            response = get_product_recommendations(products, user_input)
        
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print("NikeBot:", response)
        speak_text(response)

if __name__ == "__main__":
    chatbot_interface()
