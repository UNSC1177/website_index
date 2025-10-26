from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired
import mysql.connector
import bcrypt
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Formularze
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PersonForm(FlaskForm):
    imie = StringField('Imię', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    adres = TextAreaField('Adres')
    telefon = StringField('Telefon')
    pokrewienstwo = StringField('Pokrewieństwo')
    data_urodzenia = DateField('Data urodzenia', format='%Y-%m-%d')
    opis = TextAreaField('Opis')
    submit = SubmitField('Zapisz')

# Połączenie z bazą
def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

# Logowanie
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (form.username.data,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Niepoprawne dane logowania', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM osoby")
    osoby = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', osoby=osoby)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = PersonForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO osoby (imie, nazwisko, adres, telefon, pokrewienstwo, data_urodzenia, opis)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            form.imie.data,
            form.nazwisko.data,
            form.adres.data,
            form.telefon.data,
            form.pokrewienstwo.data,
            form.data_urodzenia.data,
            form.opis.data
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_person.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM osoby WHERE id=%s", (id,))
    person = cursor.fetchone()
    if not person:
        return redirect(url_for('dashboard'))
    form = PersonForm(data=person)
    if form.validate_on_submit():
        cursor.execute("""
            UPDATE osoby
            SET imie=%s, nazwisko=%s, adres=%s, telefon=%s, pokrewienstwo=%s, data_urodzenia=%s, opis=%s
            WHERE id=%s
        """, (
            form.imie.data,
            form.nazwisko.data,
            form.adres.data,
            form.telefon.data,
            form.pokrewienstwo.data,
            form.data_urodzenia.data,
            form.opis.data,
            id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    cursor.close()
    conn.close()
    return render_template('edit_person.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
