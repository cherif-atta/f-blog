




from flask import g, session
import pytest
from flaskr.db import get_db


def test_register_user_successfully(app, client):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'username':'a', 'password':'a'}
    )
    assert response.headers["Location"] == "/auth/login"
    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM user WHERE username =?',
            ('test',)
        ).fetchone() is not None
    


@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('test', 'test', b'User test is already registered'),
    ('', '', b'username required'),
    ('abb', '', b'password required'),
))
def test_validation_data_when_registering_user(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username':username, 'password':password}
    )
    assert message in response.data


def test_login_success_whith_valid_credentials(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('catta', 'test', b'Unknown user catta'),
    ('test', 'Tu!lk7?', b'incorrect password'),
))
def test_login_whith_invalid_credentials(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
