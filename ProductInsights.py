import certifi
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from google.cloud import language_v1
import os

# Connect to MongoDB Atlas with SSL
client = MongoClient('mongodb+srv://tester:giatri@clustertest.kmzw0bd.mongodb.net/?retryWrites=true&w=majority',
                     ssl=True,
                     tlsCAFile=certifi.where())
db = client['ratingsandreviews']
collection = db['ratingsandreviews']

# Set the path to the service account key JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\Giatri Lalla\\Desktop\\Swayed\\api_key.json'

# Initialize Flask application
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        # Handle GET request
        return render_template('productinsights.html')

    elif request.method == 'POST':
        # Handle POST request
        # Get the search query from the request body
        search_query = request.json.get('searchQuery')

        # Search for reviews matching the query in the MongoDB collection
        query_filter = {"$or": [
            {"Star-rating": {"$regex": search_query, "$options": "i"}},
            {"Review Title": {"$regex": search_query, "$options": "i"}},
            {"Review Content": {"$regex": search_query, "$options": "i"}}
        ]}
        matched_reviews = collection.find(query_filter)

        # Return the matched reviews as JSON response
        reviews = []
        for review in matched_reviews:
            reviews.append({
                'Star-rating': review['Star-rating'],
                'Review Title': review['Review Title'],
                'Review Content': review['Review Content']
            })

        return jsonify({'results': reviews})

if __name__ == '__main__':
    # Run the Flask application on all addresses using port 8080
    app.run(host='0.0.0.0', port=8080)