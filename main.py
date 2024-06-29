from utils import get_product_info, get_product_recommendations, analyze_image, speak_text, upload_image, encode_image, recognize_speech

def chatbot_interface():
    print("Welcome to Nike's Air Jordan Collection Chatbot!")
    speak_text("Welcome to Nike's Air Jordan Collection Chatbot!")
    products = get_product_info("https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok1")
    
    while True:
        print("\nHow would you like to interact with the chatbot?")
        print("1. Text Query")
        print("2. Image and Text Query")
        print("3. Voice Query")
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
            user_input = recognize_speech()
            if user_input:
                response = get_product_recommendations(products, user_input)
            else:
                response = "Voice input not recognized."
        
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print("NikeBot:", response)
        speak_text(response)

if __name__ == "__main__":
    chatbot_interface()
