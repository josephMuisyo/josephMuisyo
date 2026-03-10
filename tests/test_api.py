import os
from pathlib import Path

os.environ['SECRET_KEY'] = 'this_is_a_test_secret_key_with_32_chars!'
os.environ['DATABASE_URL'] = f"sqlite:///{Path(__file__).parent / 'test.db'}"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_user(email: str, password: str, role: str):
    return client.post(
        '/auth/register',
        json={
            'email': email,
            'full_name': 'Test User',
            'password': password,
            'role': role,
        },
    )


def login(email: str, password: str) -> str:
    response = client.post('/auth/login', json={'email': email, 'password': password})
    return response.json()['access_token']


def test_secure_headers_present():
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.headers['x-frame-options'] == 'DENY'
    assert response.headers['x-content-type-options'] == 'nosniff'


def test_end_to_end_leasing_flow():
    owner = register_user('owner@example.com', 'strongPassword1!', 'owner')
    tenant = register_user('tenant@example.com', 'strongPassword1!', 'tenant')

    assert owner.status_code == 201
    assert tenant.status_code == 201

    owner_token = login('owner@example.com', 'strongPassword1!')
    tenant_token = login('tenant@example.com', 'strongPassword1!')

    parcel_resp = client.post(
        '/parcels',
        json={
            'title': 'Acre 9',
            'location': 'Kajiado',
            'area_hectares': 6.0,
            'monthly_price': 1200,
        },
        headers={'Authorization': f'Bearer {owner_token}'},
    )
    assert parcel_resp.status_code == 201
    parcel_id = parcel_resp.json()['id']

    lease_resp = client.post(
        '/leases',
        json={
            'parcel_id': parcel_id,
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
        },
        headers={'Authorization': f'Bearer {tenant_token}'},
    )
    assert lease_resp.status_code == 201

    lease_id = lease_resp.json()['id']
    approve_resp = client.patch(
        f'/leases/{lease_id}/status',
        json={'status': 'active'},
        headers={'Authorization': f'Bearer {owner_token}'},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()['status'] == 'active'
