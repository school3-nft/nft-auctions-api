import asyncio
import pytest
from fastapi.testclient import TestClient

from app.main import app

pytest_plugins = ('pytest_asyncio',)

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_create_user():
    response = client.get('/create-user')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['account_address']) == 34
    assert response_data['account_address'][0] == 'r'
    assert response_data['account_balance'] == 1000.0
    assert len(response_data['seed']) == 31
    assert len(response_data['public_key']) == 66
    assert len(response_data['private_key']) == 66


@pytest.mark.asyncio
async def test_get_account_data():
    user_response = client.get('/create-user')
    assert user_response.status_code == 200
    user = user_response.json()
    user_seed = user['seed']
    user_sequence = user['sequence']

    response = client.get(f'/account-data/?seed={user_seed}&sequence={user_sequence}')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['account_address']) == 34
    assert response_data['account_address'][0] == 'r'
    assert response_data['account_balance'] == 1000.0
    assert len(response_data['seed']) == 31
    assert len(response_data['public_key']) == 66
    assert len(response_data['private_key']) == 66
