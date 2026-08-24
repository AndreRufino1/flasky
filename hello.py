from flask import Flask, render_template, request, session, redirect, url_for
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta_ifsp_dswa5'
moment = Moment(app)

class HomeForm(FlaskForm):
    nome = StringField('Informe o seu nome:', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de projetos', 'Gestão de projetos')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário ou e-mail', validators=[DataRequired()])
    senha = PasswordField('Informe a sua senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = HomeForm()

    # Se o usuário clicou em Submit
    if form.validate_on_submit():
        session['nome'] = form.nome.data
        session['sobrenome'] = form.sobrenome.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data

        # Captura o IP e o Host APENAS após o envio, para que antes fiquem como None
        session['ip_remoto'] = request.remote_addr
        session['host_app'] = request.host

        return redirect(url_for('index'))

    agora = datetime.now(timezone.utc)

    return render_template('index.html', form=form,
                           nome=session.get('nome'),
                           sobrenome=session.get('sobrenome'),
                           instituicao=session.get('instituicao'),
                           disciplina=session.get('disciplina'),
                           ip_remoto=session.get('ip_remoto'),
                           host_app=session.get('host_app'),
                           current_time=agora)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Agora ele salva o usuário que foi digitado na caixinha
        session['usuario_logado'] = form.usuario.data
        return redirect(url_for('login'))

    agora = datetime.now(timezone.utc)
    # Envia a informação do usuário logado para o HTML
    return render_template('login.html', form=form, usuario=session.get('usuario_logado'), current_time=agora)