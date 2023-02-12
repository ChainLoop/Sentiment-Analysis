import os
import requests
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"

MODEL_API = "https://huggingface.co/{}/model".format(MODEL)
MODEL_DIRECTORY = "./model"

if not os.path.exists(MODEL_DIRECTORY):
    os.makedirs(MODEL_DIRECTORY)

model_file = os.path.join(MODEL_DIRECTORY, MODEL.split("/")[-1]+".tar.gz")
if not os.path.exists(model_file):
    response = requests.get(MODEL_API)
    with open(model_file, "wb") as f:
        f.write(response.content)

sentiment_analysis = pipeline("sentiment-analysis", model=MODEL)

@app.route('/sentiment/sentence', methods=['POST'])
def sentiment_sentence():
    request_data = request.get_json()
    text = request_data.get('text')
    if not text:
        return jsonify({"error": "The 'text' field is required in the request"}), 400
    sentiment_score = sentiment_analysis(text)[0].get("label")
    sentiment_labels = {
        '1 star': 'negative',
        '2 stars': 'negative',
        '3 stars': 'neutral',
        '4 stars': 'positive',
        '5 stars': 'positive'
    }
    sentiment = sentiment_labels.get(sentiment_score)
    return jsonify({"sentiment": sentiment, "score": sentiment_score})

@app.route('/sentiment/document', methods=['POST'])
def sentiment_document():
    request_data = request.get_json()
    text = request_data.get('text')

    if not text:
        return jsonify({"error": "The 'text' field is required in the request"}), 400
    sentiments = sentiment_analysis(text)
    sentiment_labels = {
        '1 star': 'negative',
        '2 stars': 'negative',
        '3 stars': 'neutral',
        '4 stars': 'positive',
        '5 stars': 'positive'
    }
    sentiments = [{"label": sentiment_labels.get(res.get("label")), "score": res.get("label")} for res in sentiments]
    return jsonify({"sentiments": sentiments})


@app.route('/sentiment/custom', methods=['POST'])
def sentiment_custom():
    request_data = request.get_json()
    text = request_data.get('text')
    labels = request_data.get('labels')
    if not text:
        return jsonify({"error": "The 'text' field is required in the request"}), 400
    if not labels:
        return jsonify({"error": "The 'labels' field is required in the request"}), 400
    sentiment = sentiment_analysis(text,  labels=labels)[0].get("label")
    sentiment_value = sentiment_analysis(text,  labels=labels)[0].get("score")

    return jsonify({"sentiment": sentiment, "sentiment_value": sentiment_value})

if __name__ == '__main__':
    app.run(port=5000)