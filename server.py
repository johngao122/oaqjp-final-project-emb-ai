"""
server.py

This module contains the Flask application for the Emotion Detection project.
It provides an endpoint to process user input text and returns detected emotions
along with the dominant emotion.

Author: [John Gao Jiahao]
Date: [21/11/2024]
"""

from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/emotionDetector", methods=["POST"])
def detect_emotion():
    """
    Endpoint to detect emotion from text.
    Accepts a POST request with a JSON object containing a 'text' field.
    Returns the emotions and dominant emotion in a formatted response.
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    text_to_analyze = data["text"]
    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return jsonify({"message": "Invalid text! Please try again!"}), 400

    emotions = ", ".join(
        [
            f"'{key}': {value}"
            for key, value in result.items()
            if key != "dominant_emotion"
        ]
    )
    dominant_emotion = result["dominant_emotion"]

    response_message = (
        f"For the given statement, the system response is {emotions}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return jsonify({"message": response_message})


if __name__ == "__main__":
    #Run the flask application
    app.run(host="localhost", port=5000, debug=True)
