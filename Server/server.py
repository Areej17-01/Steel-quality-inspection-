from flask import Flask, request, jsonify
import cv2
import numpy as np
from Server import Util
from Util import classify_image

app = Flask(__name__)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        try:
            image = request.form['image']
            if image:
                result = classify_image(image)  # Call your utility function
                return jsonify(result)
            else:
                return jsonify({"error": "No image uploaded."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':

        return jsonify({"message": "This is a GET request to the /classify endpoint."})
    else:
        return jsonify({"error": "Invalid request method."}), 400

if __name__ == '__main__':
    Util.load_save_artifacts()
    app.run(host='0.0.0.0', port=5000)
