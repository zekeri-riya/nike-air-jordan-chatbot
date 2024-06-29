import easygui
import base64

def upload_image():
    file_path = easygui.fileopenbox(title="Select an image file", filetypes=["*.jpg", "*.jpeg", "*.png"])
    return file_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string
