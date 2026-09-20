import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma chave secreta bem segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# Modelos do Banco de Dados
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'<User {self.username}>'

# Formulário
class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Função de envio de e-mail via SendGrid
def enviar_email_cadastro(nome_novo_usuario):
    email_remetente = 'a.papaleo@aluno.ifsp.edu.br'

    emails_destino = ['flaskaulasweb@zohomail.com', 'a.papaleo@aluno.ifsp.edu.br']

    conteudo_html = f"""
    <p><strong>Prontuário:</strong> PT3026159</p>
    <p><strong>Nome do aluno:</strong> André Rufino Papaleo</p>
    <p><strong>Novo usuário cadastrado:</strong> {nome_novo_usuario}</p>
    """

    mensagem = Mail(
        from_email=email_remetente,
        to_emails=emails_destino,
        subject='Novo Usuário Cadastrado no Flask',
        html_content=conteudo_html
    )

    try:
        # Chave protegida por variável de ambiente para o GitHub não bloquear
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(mensagem)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            enviar_email_cadastro(form.name.data)
            flash('Novo usuário cadastrado com sucesso e e-mail enviado!')
        else:
            flash('Nome de usuário já cadastrado!')
        return redirect(url_for('index'))

    # Consulta os usuários e funções cadastrados para exibir nas tabelas
    users = User.query.all()
    roles = Role.query.all()

    return render_template('index.html', form=form, name=None, users=users, roles=roles)

if __name__ == '__main__':
    app.run(debug=True)