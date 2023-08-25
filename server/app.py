from flask import Flask, request, jsonify, render_template, redirect, url_for
import util
from util import classify_image
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steeldefect.db'  # Use a local SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Define a User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image= db.Column(db.String(256), nullable=False)
    result = db.Column(db.String(120),nullable=False)

with app.app_context():
    db.create_all()


SECRET_KEY = 'random_key'

# Function to generate a JWT token
def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@app.route("/home")
def home():
    return render_template("homepage.html")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/description")
def description():
    return render_template("description.html")


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


@app.route("/loginapi", methods=["POST"])
def loginapi():
    if request.method == "POST":
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            # Query the database to check if the user exists
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                token = generate_token(user)
                return jsonify({"token": token, "user": user.username}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Check if the email is already registered
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                return jsonify({"error": "Email already exists"}), 400

            # Create a new user and add them to the database
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            # Generate a token for the new user
            token = generate_token(new_user)

            return jsonify({"token": token, "user": new_user.username}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/saveimage",methods=["POST"])
def saveimage():
    if request.method == "POST":
        try:
            data = request.get_json()
            image = data.get("image")
            result = data.get("result")

            new_image = Gallery(image=image,result=result)
            db.session.add(new_image)
            db.session.commit()

            return  jsonify({"message":"image uploaded to gallery!"}), 201

        except Exception as e:
                return jsonify({"error": str(e)}), 500

@app.route("/gallery")
def gallery():
    # Query the Gallery table to retrieve images and results
    images = Gallery.query.all()
    
    # Create a list of dictionaries containing result and image strings
    image_data = [{"result": image.result, "image": image.image} for image in images]
    
    return jsonify(image_data)


@app.route("/history")
def history():
    return render_template("gallery.html")


if __name__ == "__main__":
    util.load_save_artifacts()
    app.run(port=5000)
