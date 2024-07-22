from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel
import re


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


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):

    def validate_cpf(self, cpf):

        # has te correct mask?
        if not re.match(r'\d{3}\.\d{3}\.\d{3}.\d{2}', cpf):
            return False

        # grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # validate first digit after -
        sum_of_produtcs = sum(a*b for a, b in zip(numbers[0:9],
                                                  range(10, 1, -1)))
        expected_digit = (sum_of_produtcs * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # validate second digit after -
        sum_of_produtcs = sum(a*b for a, b in zip(numbers[0:10],
                                                  range(11, 1, -1)))
        expected_digit = (sum_of_produtcs * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"massage": "CPF is invalid!"}, 400

        try:
            response = UserModel(**data).save()
            return {"massage": "User %s successfully created!" % response.id}
        except NotUniqueError:
            return {"massage": "CPF already exists in database!"}, 400

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)

        if response:
            return jsonify(response)

        return {"massage": "User doest not exists in database!"}, 400
