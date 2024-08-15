from flask import Blueprint, request, jsonify
from .database import create_user, create_log, authenticate_user
from .mlmodel import predict
routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/newuser', methods=['POST'])
def create_user_route():
    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('password')
    new_user_name = data.get('newUserName')
    new_password = data.get('newPassword')
    userid = create_user(userName, password, newUserName, newPassword)
    if userid:
        response = {'message': 'User created successfully'}
        create_log(userid, "POST", data, response)
        return jsonify(response), 201
    else:
        response = jsonify({'message': 'Invalid credentials'}), 401
        return response

@routes_blueprint.route('/predict_group_survival', methods=['GET'])
def predictsurvival():
    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('password')
    passengers = data.get('passengers')
    user_id = authenticate_user(user_name, password)
    if not user_id:
        response = jsonify({'message': 'Invalid credentials'}), 401
        return response
    response = predict(passengers)
    create_log(user_id, "GET", data, response)
    return jsonify(response), 201

@routes_blueprint.route('/predict_individual_survival', methods=['GET'])
def predictsurvival():
    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('password')
    passenger = data.get('passengers')
    user_id = authenticate_user(user_name, password)
    if not user_id:
        response = jsonify({'message': 'Invalid credentials'}), 401
        return response
    response = predict([passenger])
    create_log(user_id, "GET", data, response)
    return jsonify(response), 201

@routes_blueprint.route('/health')
def healthcheck():
    return {'status': 'OK'}, 200
