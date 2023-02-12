import requests

url1 = "http://localhost:5000/sentiment/sentence"
url2 = "http://localhost:5000/sentiment/document"

data1 = {"text": "This is an example good  sentence. But we want more "}

data2 = {"text": "Another advantage of 3D printing prosthetic devices is faster development cycles, which can facilitate rapid design iteration to improve fit and comfort. In addition, the scalability of AM makes mass production more economically viable, reducing costs for healthcare providers and consumers."}

try:
    response1 = requests.post(url1, json=data1)
    response2 = requests.post(url2, json=data2)
except requests.exceptions.RequestException as e:
    print("An error occurred during the API call:", e)
else:
    print(response1.json())
    print(response2.json())
