import pymongo
import certifi
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# MongoDB Atlas connection details
connection_string = 'mongodb+srv://tester:giatri@clustertest.kmzw0bd.mongodb.net/?retryWrites=true&w=majority'

# Create the MongoDB client
client = pymongo.MongoClient(connection_string, ssl=True, tlsCAFile=certifi.where())

# Select the database
db = client['ratingsandreviews']

# Create the 'registrants' collection
collection = db['registrants']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the form data from the request
        data = {
            "uname": request.form.get("uname"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "confirmPassword": request.form.get("confirmPassword")
        }

        # Store the form data in MongoDB
        result = collection.insert_one(data)

        if result.acknowledged:
            return redirect(url_for('success'))
        else:
            return jsonify({"message": "Registration failed"})
    else:
        return render_template("newuser.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run()