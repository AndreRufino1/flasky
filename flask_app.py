from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghp_OUMt6a2NBB3djgQUa5W3sKppZdKxxz0lTA6E'

# Inicializando o Flask-Moment
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    
    # Adicionando a variável current_time no render_template
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)