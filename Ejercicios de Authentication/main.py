from flask import Flask, Response, request, jsonify
from db import DB_manager
from jwt_manager import JWT_Manager

app = Flask("user-service")
db_manager = DB_manager()
jwt_manager = JWT_Manager("280596", "HS256")

@app.route("/liveness")
def liveness():
    return "<p> Hello, world! </p>"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        result = db_manager.insert_user(data.get('username'), data.get('password'))
        user_id = result[0]

        token = jwt_manager.encode({'id':user_id})
        
        return jsonify(token=token)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        result = db_manager.get_user(data.get('username'), data.get('password'))

        if (result == None):
            return Response(status=403)
        else:
            user_id = result[0]
            token = jwt_manager.encode({'id':user_id})

            return jsonify(token=token)
        
@app.route('/me')
def me():
    try:
        token = request.headers.get('Authorization')
        if(token is not None):
            test = token.replace("Bearer ", "")
            print(test)
            decoded = jwt_manager.decode(test)
            user_id = decoded['id']

            user = db_manager.get_user_by_id(user_id)

            return jsonify(id=user[0], username=user[1])
        else:
            return Response(status=403)
        
    except Exception as e:
        print(e)
        return Response(status=500)

app.run(host="localhost", port=5000, debug=True)

