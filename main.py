import certifi
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os

# Connect to MongoDB Atlas with SSL
client = MongoClient(
    'mongodb+srv://tester:giatri@clustertest.kmzw0bd.mongodb.net/?retryWrites=true&w=majority',
    ssl=True,
    tlsCAFile=certifi.where()
)
db = client['ratingsandreviews']
collection = db['productinsights']

# Set the path to the service account key JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\Giatri Lalla\\Desktop\\Swayed\\api_key.json'

# Initialize Flask application
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results.html', methods=['GET'])
def results():
    # Get the search query from the URL parameters
    search_query = request.args.get('searchQuery')

    # Analyze each product insight
    results = []
    for doc in collection.find():
        # Get the fields from the document
        full_name = doc.get('FullName', '')
        description = doc.get('Description', '')
        brand = doc.get('Brand', '')
        manufacturer = doc.get('Manufacturer', '')
        dimension = doc.get('Dimension', '')
        weight = doc.get('Weight', '')
        star_rating = doc.get('Average Star Rating', 0.0)
        sentiment_score = doc.get('Average Sentiment Score', 0.0)
        product_link = doc.get('ProductLink', '')
        sentiment_description = doc.get('Sentiment Description', '')
        statement = doc.get('Statement', '')

        # Check if the search query is present in any of the fields
        if search_query.lower() in (description + brand + manufacturer + dimension).lower():
            # Add the fields to the results list
            results.append({
                'FullName': full_name,
                'Description': description,
                'Brand': brand,
                'Manufacturer': manufacturer,
                'Dimension': dimension,
                'Weight': weight,
                'Average Star Rating': star_rating,
                'Average Sentiment Score': sentiment_score,
                'Sentiment Description': sentiment_description,
                'Statement': statement,
                'ProductLink': product_link
            })

    return render_template('results.html', results=results)

if __name__ == '__main__':
    # Run the Flask application on all addresses using port 8080
    app.run(host='0.0.0.0', port=8080)