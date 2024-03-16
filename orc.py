from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

subscription_key = "7b7d351c702e4332a6aac818d3222f54"
endpoint = "https://demo-orc-python.cognitiveservices.azure.com/"

credentials = CognitiveServicesCredentials(subscription_key)
client = ComputerVisionClient(endpoint, credentials)

def correct_text_ocr(image_path):
    image = open(image_path, "rb")
    result = client.recognize_printed_text_in_stream(image)

    for region in result.regions:
        for line in region.lines:
            for word in line.words:
                # Print each character of the word vertically
   
                print(word)
                # Print an empty line after each word
                print()

    image.close()

num = [1,2,3,4,5,6]

for index, i in enumerate(num):
    image_path = "/Applications/XAMPP/xamppfiles/htdocs/OCR-Azure-sample/image/match_{}.jpg".format(i)
    corrected_text = correct_text_ocr(image_path)
    print(f"{index+1}: {corrected_text}\n")
