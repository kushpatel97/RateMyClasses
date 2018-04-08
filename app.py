from flask import Flask, render_template, redirect, request, flash, url_for, session, g
from flask_mysqldb import MySQL
from functools import wraps
import os



app = Flask(__name__)

#MySQL config
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'ratemyclass.cej3ioszzgpd.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'ratemyclass'
app.config['MYSQL_PASSWORD'] = 'ratemyclass'
app.config['MYSQL_DB'] = 'ratemyclass'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login

db = MySQL(app)



@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        username = str(request.form['username'])
        password = str(request.form['password'])

        connection = db.connection
        cur = connection.cursor()

        result = cur.execute('SELECT * FROM Users WHERE Username=%s', [username])

        if result > 0:
            data = cur.fetchone()
            datapass = data['Password']

            if datapass == password:
                cur.close()
                session['user'] = username
                return redirect(url_for('home'))
            else:
                error = 'Wrong Password! Try Again'
                flash(error, 'danger')
                return render_template('login.html',error=error)
        else:
            cur.close()
            error = 'No email found!'
            flash(error, 'danger')
            return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    majorlist = []
    connection = db.connection
    cur = connection.cursor()
    cur.execute('SELECT * FROM majors;')
    majorlist = cur.fetchall()
    db.connection.commit()
    cur.close()

    if request.method == 'POST':
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        major_name = str(request.form['major_name'])

        connection = db.connection
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM Users WHERE Username=%s",[username])


        if result > 0:
            flash('Username already exists', 'danger')
            return render_template('register.html')


        cur.execute('INSERT INTO ratemyclass.Users (Username, Email, Password, major_name) VALUES (%s, %s, %s, %s)',(username, email, password, major_name))

        db.connection.commit()

        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html', majorlist=majorlist)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You just logged out', 'success')
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if g.user:
        majorlist = []
        connection = db.connection
        cur = connection.cursor()
        cur.execute('SELECT * FROM majors;')
        majorlist = cur.fetchall()
        db.connection.commit()
        cur.close()

        test = g.user
        return render_template('home.html', majorlist=majorlist, test=test)
    else:
        flash('Use the front door!','danger')
        return redirect(url_for('login'))



# if __name__ == '__main__':
#     app.run(debug=True)