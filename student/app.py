from flask import Flask, jsonify,request
import uuid
import jwt
from auth_middleware import auth_middleware
from middleware import jwt_middleware


app = Flask(__name__)
jwt_middleware(app)
auth_middleware(app)


student_db = {
    "bebb863f6e854a94979986d11f812832":{
        "name": "chirali",
        "roll no.": 17,
        "class": "CE1",
        "subject":["science","computer"]
    },
    "98d5ddbc61734a52b2eb208046adde85":{
        "name": "charmi",
        "roll no.": 5,
        "class": "CE1",
        "subject":["computer","physics"]
    },
    "0c773d7c9a5342bcb4a7be36d9d69317":{
        "name": "krisha",
        "roll no.": 60,
        "class": "CE2",
        "subject":["python","java"]
    },
    "477e88cc2cbb43eeb33fbe54c492afc8":{
        "name": "vrunda",
        "roll no.": 39,
        "class": "CE3",
        "subject":["cloud computing",".Net"]
    },
    "d504628eddfe4041b9a9a0083b3ec796":{
        "name": "drashti",
        "roll no.": 70,
        "class": "CE3",
        "subject":["machine learning","computer network"]
    }
}

@app.route('/')
def home():
    return "hello students"

@app.route('/students')
def get_all_students_detail():
    return jsonify({"students detail": student_db})

@app.route('/student')
def get_student_detail():
    id = request.args.get('id')
    try:
        return student_db[id]
    except:
        return jsonify({"message":"student not found"})

@app.route('/add_student',methods=['post'])
def create_student_detail():
    body_data = request.get_json()
    if "name" not in body_data or "roll no." not in body_data:
        return jsonify({"message": "name and roll no must be included"})
    student_db[uuid.uuid4().hex] = (body_data)
    return jsonify({"message": "student has been created" })

@app.put('/update-student')
def update_student_detail():
    id = request.args.get('id')

    if id in student_db.keys():
        student_db[id] = request.get_json()
        return jsonify({"message": "item updated"},200)
    else: 
        return jsonify({"message": "Not found"},404)

@app.delete('/delete-student')
def delete_student_detail():
    id = request.args.get('id')
    if id in student_db.keys():
        del student_db[id]
        return jsonify({"message": "student deleted"})  
    return jsonify({"message": "student not found"},404)

app.config['SECRET_KEY']="bcfc6ceab8bc4491b6a73da7f3b47c00"

@app.route('/login', methods=['POST'])
def login():
    # Perform necessary authentication and validation checks
    username = 'chirali'
    password = 'chirali1234'

    # Check if the credentials are valid
    if check_credentials(username, password):
        # Generate the JWT bearer token
        token = generate_token(username)
        return jsonify({'token': token})

    # Return an error message if the credentials are invalid
    return jsonify({'message': 'Invalid username or password'}), 401

def check_credentials(username, password):
    # Implement your authentication logic here
    # This can involve checking against a database, external service, or other methods
    # Return True if the credentials are valid, otherwise return False
    if username == 'chirali' and password == 'chirali1234':
        return True
    return False

def generate_token(username,role):
    # Create the payload for the token
    payload = {'username': username, 'role': role}

    # Generate the JWT bearer token
    token = jwt.encode(payload, 'bcfc6ceab8bc4491b6a73da7f3b47c00', algorithm='HS256')

    # Return the token
    app.config['SECRET_KEY']
    return token

token = generate_token('chirali', 'admin')
print("admin token",token)

token1 = generate_token('krisha' , 'user')
print("user token",token1)

token2 = generate_token('charmi','mediator')
print("mediatior token",token2)

if __name__ == '__main__':
    app.run(debug=True)



app.run(port=1000)