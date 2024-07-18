from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin'
}


user_parser = reqparse.RequestParser()
user_parser.add_argument('first_name',
                           type=str,
                           required=True,
                           help="This field cannot be blank."
                           )
user_parser.add_argument('last_name',
                           type=str,
                           required=True,
                           help="This field cannot be blank."
                           )
user_parser.add_argument('cpf',
                           type=str,
                           required=True,
                           help="This field cannot be blank."
                           )
user_parser.add_argument('email',
                           type=str,
                           required=True,
                           help="This field cannot be blank."
                           )
user_parser.add_argument('birth_date',
                           type=str,
                           required=True,
                           help="This field cannot be blank."
                           )


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    birth_date = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        return {"massage": "user 1"}


class User(Resource):
    def post(self):
        data = user_parser.parse_args()
        UserModel(**data).save()

    def get(self, cpf):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
