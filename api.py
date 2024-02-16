from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import db
from secure_token import SecureToken as sc
from urllib.parse import unquote

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'KUYK4536sfgfg@#%$%^&yuytu'
jwt = JWTManager(app)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        credentials = request.args.get('credentials')
    elif request.method == 'POST':
        credentials = request.form.get('credentials')
        
    credentials = sc.tokendecrypt(credentials)
    credentials = credentials.split(':')
    username, password = credentials

    if db.checkauth(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(msg=access_token), 200
    else:
        return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/api/version', methods=['GET'])
def get_version():
    return jsonify(msg='0.0.1')

@app.route('/api/private_method/<string:param1>', methods=['GET'])
@jwt_required()
def echo(param1):

    return jsonify({'msg': {'param1': unquote(param1), 'identity': get_jwt_identity()}}), 200 


if __name__ == '__main__':
    app.run(debug=True)
