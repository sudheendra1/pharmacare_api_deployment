from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import random

app = Flask(__name__)


CORS(app)

@app.route('/search', methods=['POST'])
def search():
    product_name = request.json.get('product_name')
    results = search_csv(product_name)
    return jsonify(results)

def search_csv(query):
    results = []
    with open('all_medicines.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if query.lower() in row['product_name'].lower():
                results.append(row)
    unique_results = remove_duplicates(results)
    return unique_results

    

def remove_duplicates(results):
    unique_results = []
    seen = set()  
    for row in results:
        if row['product_name'] not in seen:
            unique_results.append(row)
            seen.add(row['product_name'])  
    return unique_results

@app.route('/all_products', methods=['GET'])
def get_all_products():
    limit = request.args.get('limit', default=10, type=int)
    products = []
    with open('all_medicines.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
    
    random.shuffle(products)  
    return jsonify(products[:limit]) 



if __name__ == "__main__":
    app.run( host='0.0.0.0')
