import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Pedro",
            "last_name": "Câmara",
            "cpf": "466.232.300-25",
            "email": "pedro.camara@gmail.com",
            "birth_date": "1997-09-29"
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Pedro",
            "last_name": "Câmara",
            "cpf": "466.232.300-27",
            "email": "pedro.camara@gmail.com",
            "birth_date": "1997-09-29"
        }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_users(self, client, valid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"successfully" in response.data

        response = client.post('/user', json=valid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data

    def test_get_user(self, client, valid_user):
        response = client.get('/user/%s', valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "Pedro"
        assert response.json[0]["last_name"] == "Câmara"
        assert response.json[0]["cpf"] == ""
        assert response.json[0]["email"] == "pedro.camara@gmail.com"
        assert response.json[0]["first_name"] == "Pedro"
