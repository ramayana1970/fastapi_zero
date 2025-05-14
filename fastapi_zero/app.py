from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/home', response_class=HTMLResponse)
def home():
    return '''
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