from google.cloud import vision
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Initialize the Google Cloud Vision client
client = vision.ImageAnnotatorClient()

def correct_text_ocr(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    corrected_text = []
    for text in texts:
        corrected_text.append(text.description.upper())
        
    return corrected_text

num = [1, 2]

for index, i in enumerate(num):
    image_path = "/Applications/XAMPP/xamppfiles/htdocs/OCR-Azure-sample/image/match_{}.jpg".format(i)
    corrected_text = correct_text_ocr(image_path)
    print(f"{index}: {corrected_text}\n")
