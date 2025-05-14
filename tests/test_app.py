from http import HTTPStatus

from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    cliente = TestClient(app)

    response = cliente.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_home_deve_retornar_html_ola_mundo():
    cliente = TestClient(app)

    html = '''
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
    '''

    response = cliente.get('/home')

    assert response.status_code == HTTPStatus.OK
    assert response.text == html