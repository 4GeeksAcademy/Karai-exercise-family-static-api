"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():

    members = jackson_family.get_all_members()
    response_members = []

    for member in members:
        member_dict = {
            'first_name': member.get('first_name'),
            'last_name': member.get('last_name'),
            'age': member.get('age'),
            'lucky_numbers': member.get('lucky_numbers')
        }
        response_members.append(member_dict)

    return jsonify(response_members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    member = jackson_family.get_member(id)

    if member is None:
        return jsonify({'message': f'No member with id: {id}'}), 404

    member_response = {
        'first_name': member.get('first_name'),
        'id': member.get('id'),
        'age': member.get('age'),
        'lucky_numbers': member.get('lucky_numbers')
    }

    return jsonify(member_response), 200

@app.route('/member', methods=['POST'])
def add_mebmber():

    data = request.json
    first_name = data.get('first_name')
    age = data.get('age')
    lucky_numbers = data.get('lucky_numbers', [])
    id = data.get('id')

    if not first_name or not age or not lucky_numbers:
        return jsonify({'message': 'Bad request. Missing required data.'}), 400

    member = {
        'first_name': first_name,
        'age': age,
        'lucky_numbers': lucky_numbers,
        'id': id
    }
   
    added_member = jackson_family.add_member(member)

    return jsonify(added_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    deleted_response = jackson_family.delete_member(id)

    # if not deleted_response:
    #     return jsonify({'message': f'No member with id: {id}'}), 404

    return jsonify({'done': deleted_response}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
