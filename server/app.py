from flask import Flask, request, jsonify, render_template

import util
from util import classify_image

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":
        try:
            image = request.files["image_data"]
            if image:
                img = image.read()
                result = classify_image(img)  # Call your utility function
                return jsonify({"result": result})
            else:
                return jsonify({"error": "No image uploaded."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "GET":
        return jsonify({"message": "This is a GET request to the /classify endpoint."})
    else:
        return jsonify({"error": "Invalid request method."}), 400


if __name__ == "__main__":
    util.load_save_artifacts()
    app.run(port=5000)
