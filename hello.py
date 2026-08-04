from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)

# 1. Rota raiz
@app.route('/')
def index():
    return '<h1>Hello World!</h1><h2>Disciplina PTBDSWS</h2>'

# 2. Rota dinâmica
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

# 3. Contexto da requisição
@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

# 4. Código de status diferente
@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    return 'Bad request', 400

# 5. Objeto de resposta (Cookie)
@app.route('/objetoresposta')
def objetoresposta():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('teste_cookie', '12345')
    return response

# 6. Redirecionamento
@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br')

# 7. Abortar (Erro 404)
@app.route('/abortar')
def abortar():
    abort(404)