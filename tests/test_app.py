from http import HTTPStatus

from fastapi_zero.schemas import UserPublic, UserSchema


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_home_deve_retornar_html_ola_mundo(client):
    html = """
    <html>
        <head>
            <title>Bem vindo ao meu Olá mundo!</title>
        </head>
        <body>
            <h1>Olá Mundo!!</h1>
            <p>
               Pra não sofrer com a maldição...
            </p>
        </body>
    </html>
    """

    response = client.get('/home')

    assert response.status_code == HTTPStatus.OK
    assert response.text == html


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(
    client,
    user: UserSchema,
):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema],
    }


def test_get_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_get_user_with_404(client, user):
    response = client.get('/users/11')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!!'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'email': 'bob@example.com',
            'username': 'bob',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'bob@example.com',
        'username': 'bob',
    }


def test_update_user_with_404(client, user):
    response = client.put(
        '/users/22',
        json={
            'email': 'bob@example.com',
            'username': 'bob',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!!'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully!!'}


def test_delete_user_with_404(client, user):
    response = client.delete('/users/33')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!!'}


def test_create_integrity_username_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists!!'}


def test_create_integrity_email_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists!!'}


def test_update_integrity_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'alice@exemplo.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists!!'}
