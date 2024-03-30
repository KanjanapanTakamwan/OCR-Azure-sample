from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "7b7d351c702e4332a6aac818d3222f54"
endpoint = "https://demo-orc-python.cognitiveservices.azure.com/"

credentials = CognitiveServicesCredentials(subscription_key)
client = ComputerVisionClient(endpoint, credentials)

def correct_text_ocr(image_path):
    with open(image_path, "rb") as image:
        result = client.recognize_printed_text_in_stream(image)
        data = []
        for region in result.regions:
            for line in region.lines:
                for word in line.words:
                    data.append(word.text)
    return data

num = [1, 2]

for index, i in enumerate(num):
    image_path = "/Applications/XAMPP/xamppfiles/htdocs/OCR-Azure-sample/image/match_{}.jpg".format(i)
    data = correct_text_ocr(image_path)
    print(f"{index+1}: {data}\n")
