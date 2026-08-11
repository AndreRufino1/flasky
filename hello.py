from flask import Flask, render_template, request
from flask_moment import Moment
from datetime import datetime, timezone

app = Flask(__name__)
# Inicializa a extensão Moment
moment = Moment(app)

# 1. Rota Home (Aula 040)
@app.route('/')
def index():
    # Captura tempo exato
    agora = datetime.now(timezone.utc)
    # Envia a variável 'agora' para ser exibida no HTML
    return render_template('index.html', current_time=agora)

# 2. Rota de Identificação
@app.route('/identificacao')
def identificacao():
    return render_template('identificacao.html')

# 3. Rota do Contexto da Requisição
@app.route('/contextorequisicao')
def contexto():
    # Captura os dados do visitante
    user_agent = request.headers.get('User-Agent')
    ip_remoto = request.remote_addr
    host_app = request.host
    # Envia os 3 dados capturados para o HTML
    return render_template('contexto.html', user_agent=user_agent, ip_remoto=ip_remoto, host_app=host_app)