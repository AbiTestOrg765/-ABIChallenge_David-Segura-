from flask import Blueprint, request, jsonify
from .database import Database
from .mlmodel import TitanicModel
routes_blueprint = Blueprint('routes', __name__)

INVALID_CREDENTIALS_ERROR = {'message': 'Invalid credentials'}

@routes_blueprint.route('/newuser', methods=['POST'])
def create_user_route():
    """This endpoint is used to create new users for the api
    ----
    POST:
        description: creates a new user 
        responses:
            201:
            content:
                application/json:
                schema: {'status': 'OK'}
    """
    data = request.get_json()

    user_name = data.get('userName')
    password = data.get('password')
    new_user_name = data.get('newUserName')
    new_password = data.get('newPassword')

    database = Database()
    userid = database.create_user(user_name, password, new_user_name, new_password)
    if userid:
        response = {'message': 'User created successfully'}
        database.create_log(userid,'/newuser', "POST", data, response)
        return jsonify(response), 201
    else:
        response = jsonify(INVALID_CREDENTIALS_ERROR), 401
        return response

@routes_blueprint.route('/predict_group_survival', methods=['GET'])
def predictsurvival():
    """This endpoint is used to predict the survival of a group of passengers 
    ----
    GET:
        description: returns a group of survival predictions
        responses:
            201:
            content:
                application/json:
                schema: [{{'Passenger Name' : name, 'Survived' : True/False}}]
    """
    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('password')
    passengers = data.get('passengers')

    database = Database()
    user_id = database.authenticate_user(user_name, password)
    if not user_id:
        response = jsonify(INVALID_CREDENTIALS_ERROR), 401
        return response
    titanic_model = TitanicModel()
    response = titanic_model.predict(passengers)
    database.create_log(user_id,'/predict_group_survival', "GET", data, response)
    return jsonify(response), 201

@routes_blueprint.route('/predict_individual_survival', methods=['GET'])
def predictsurvival_individual():
    """This endpoint is used to predict one single passenger 
    ----
    GET:
        description: returns a prediction of survival
        responses:
            201:
            content:
                application/json:
                schema: [{{'Passenger Name' : name, 'Survived' : True/False}}]
    """
    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('password')
    passenger = data.get('passengers')
    
    database = Database()
    user_id = database.authenticate_user(user_name, password)
    if not user_id:
        response = jsonify(INVALID_CREDENTIALS_ERROR), 401
        return response
    titanic_model = TitanicModel()
    response = titanic_model.predict([passenger])
    
    database.create_log(user_id, '/predict_individual_survival', "GET", data, response)
    return jsonify(response), 201

@routes_blueprint.route('/health')
def healthcheck():
    """This route is used to check the stability of the flask application
    ----
    description: returns status: OK, 200 if api is up
    responses:
        200:
          content:
            application/json:
              schema: {'status': 'OK'}
    """
    return {'status': 'OK'}, 200
