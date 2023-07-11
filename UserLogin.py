import certifi
import pymongo
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# MongoDB Atlas connection details
connection_string = 'mongodb+srv://tester:giatri@clustertest.kmzw0bd.mongodb.net/?retryWrites=true&w=majority'

# Create the MongoDB client
client = pymongo.MongoClient(connection_string, ssl=True, tlsCAFile=certifi.where())

# Select the database and collection
db = client['ratingsandreviews']
collection = db['registrants']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the form data from the request
        username = request.form.get("uname")
        password = request.form.get("psw")

        # Query the database for the registrant
        registrant = collection.find_one({"uname": username, "password": password})

        if registrant:
            # Authentication successful, redirect to product insights page
            return redirect(url_for("product_insights"))
        else:
            # Authentication failed, redirect to error page
            return redirect(url_for("error"))

    # Render the login form for GET requests
    return render_template("login.html")

@app.route("/productinsights")
def product_insights():
    # Render the product insights page
    return render_template("productinsights.html")

@app.route("/error")
def error():
    # Render the error page
    return render_template("error.html")

if __name__ == "__main__":
    app.run()