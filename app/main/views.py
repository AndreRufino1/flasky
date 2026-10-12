from datetime import datetime
from flask import render_template, redirect, url_for, session, flash
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Role, Email
from ..email import enviar_email_cadastro

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            
            # Dispara o e-mail automático para o Zoho e para o seu e-mail institucional
            try:
                enviar_email_cadastro(user.username)
                flash('E-mail enviado com sucesso para o Zoho e e-mail institucional!')
            except Exception as e:
                print(f"Erro ao disparar e-mail: {e}")
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        return redirect(url_for('.index'))
        
    users = User.query.all()
    roles = Role.query.all()
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           users=users,
                           roles=roles,
                           current_time=datetime.utcnow())

@main.route('/emailsEnviados')
def emails_enviados():
    emails = []
    try:
        emails = Email.query.order_by(Email.timestamp.desc()).all()
    except Exception:
        pass
    return render_template('emails_enviados.html', emails=emails)