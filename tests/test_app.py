from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange

    response = client.get("/")  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Olá Mundo!"}  # Assert


def test_create_user():
    client = TestClient(app)  # Arrange
    response = client.post(  # UserSchema
        "/users/",
        json={
            "username": "testeusername",
            "password": "senhadificil",
            "email": "teste@teste.com",
        },
    )
    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        "username": "testeusername",
        "email": "teste@teste.com",
        "id": 1,
    }
