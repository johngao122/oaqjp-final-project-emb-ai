import requests
import json


def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    }
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=input_json)
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        emotion_predictions = response_json.get("emotionPredictions", [{}])[0].get(
            "emotion", {}
        )
        print(emotion_predictions)
        emotions = ["anger", "disgust", "fear", "joy", "sadness"]
        filtered_emotions = {
            emotion: emotion_predictions.get(emotion, 0) for emotion in emotions
        }
        print(filtered_emotions)
        dominant_emotion = max(filtered_emotions, key=filtered_emotions.get)
        print(dominant_emotion)
        filtered_emotions["dominant_emotion"] = dominant_emotion

        return filtered_emotions

    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
