import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import date
from ..app import app
from routers.users import router
from schemas.user_schema import UserAuth
from utils.auth import get_hashed_password

app.include_router(router)  # Asegúrate de incluir el router manualmente
client = TestClient(app)

@pytest.fixture
def user():
    return {
        "email": "test@gmail.com",
        "password": "testpassword",
        "first_name": "test",
        "last_name": "Test",
        "birth_date": date(2021, 1, 1).isoformat(),
        "role": "user"
    }

@pytest.fixture
def user_invalid():
    return {
        "email": "invalid-email",
        "password": "testpassword",
        "first_name": "test",
    }

@pytest.fixture
def hass_password():
    return get_hashed_password("testpassword")

@patch('routers.users.UserRepository')
@patch('routers.users.get_hashed_password')
def test_create_user_success(mock_get_hashed_password, mock_UserRepository, user, hass_password):
    mock_repository = MagicMock()

    mock_repository.user_exists.return_value = False
    mock_UserRepository.return_value = mock_repository

    # Simula el valor del hash de la contraseña
    hashed_password = hass_password
    mock_get_hashed_password.return_value = hashed_password  # Configura el mock para que retorne el hash

    # Ahora el valor de password es un string, no un MagicMock
    user['password'] = hashed_password

    user_auth = UserAuth(**user)  # Crea un objeto UserAuth con los datos de la prueba
    response = client.post(url="/signup", json=user)

    assert response.status_code == 201
    assert response.json() == {'message': 'User created'}

    mock_repository.user_exists.assert_called_once_with(user['email'])
    mock_repository.create_user.assert_called_once_with(user_auth)

@patch('routers.users.UserRepository')
def test_create_user_invalid_data(mock_UserRepository, user_invalid):
    mock_repository = MagicMock()

    mock_repository.user_exists.return_value = False

    mock_UserRepository.return_value = mock_repository

    response = client.post(url="/signup", json=user_invalid)

    assert response.status_code == 422  # Unprocessable Entity

    mock_repository.user_exists.assert_not_called()
    mock_repository.create_user.assert_not_called()



@patch('routers.users.UserRepository')
def test_create_user_already_exists(mock_UserRepository, user):
    mock_repository = MagicMock()

    mock_repository.user_exists.return_value = True

    mock_UserRepository.return_value = mock_repository

    response = client.post(url="/signup", json=user)

    assert response.status_code == 400

    mock_repository.user_exists.assert_called_once_with(user['email'])
    mock_repository.create_user.assert_not_called()
