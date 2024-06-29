import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify if the API key is loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key is not set. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert product recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    print("Debug response get_product_recommendations:", response)  # Debug print to understand the response structure

    return response.choices[0].message.content

def analyze_image(encoded_image):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    print("Debug response analyze_image:", response)  # Debug print to understand the response structure

    return response.choices[0].message.content
