from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(os.environ.get('DB_HOST'), 27017, username=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'))
db = client[os.environ.get('DB_DB')]

@app.route('/')
def index():
    return "Index!"

@app.route('/user', methods=['GET'])
def read_data():
    try:
        # Get the collection from MongoDB
        collection = db['USERS']

        # Fetch all the documents from the collection
        documents = collection.find()

        # Convert the documents to a list of dictionaries
        data = []
        for document in documents:
            data.append({
                'uid': str(document['_id']),
                'name': document['name'],
                'age': document['age']
            })

        return jsonify(data)
    except Exception as error:
        return jsonify({'error_msg': str(error)})

@app.route('/user/new', methods=['POST'])
def create_new_user():
    try:
        # Get the collection from MongoDB
        collection = db['USERS']

        # Get the user data from the request
        user_data = request.get_json()

        # Extract the user details
        name = user_data.get('name')
        age = user_data.get('age')

        # Insert the user into the collection
        result = collection.insert_one({'name': name, 'age': age})

        # Get the ID of the newly created user
        user_id = str(result.inserted_id)

        return jsonify({'uid': user_id})
    except Exception as error:
        return jsonify({'error_msg': str(error)})

@app.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        # Get the collection from MongoDB
        collection = db['USERS']

        # Get the user data from the request
        user_data = request.get_json()

        # Extract the user details
        name = user_data.get('name')
        age = user_data.get('age')

        # Update the user in the collection
        result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': name, 'age': age}})

        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'})
    except Exception as error:
        return jsonify({'error_msg': str(error)})

@app.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Get the collection from MongoDB
        collection = db['USERS']

        # Find the document with the specified user ID
        document = collection.find_one({'_id': ObjectId(user_id)})

        if document:
            user = {
                'uid': str(document['_id']),
                'name': document['name'],
                'age': document['age']
            }
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found'})
    except Exception as error:
        return jsonify({'error_msg': str(error)})

@app.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Get the collection from MongoDB
        collection = db['USERS']

        # Delete the document with the specified user ID
        result = collection.delete_one({'_id': ObjectId(user_id)})

        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'})
    except Exception as error:
        return jsonify({'error_msg': str(error)})

if __name__ == '__main__':
    app.run()
