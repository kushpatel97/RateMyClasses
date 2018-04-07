from flask import Flask, render_template, redirect, request, flash, url_for, session, g
from flask_mysqldb import MySQL



app = Flask(__name__)



#MySQL config
app.secret_key = '123456789'
app.config['MYSQL_HOST'] = 'ratemyclass.cej3ioszzgpd.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'ratemyclass'
app.config['MYSQL_PASSWORD'] = 'ratemyclass'
app.config['MYSQL_DB'] = 'ratemyclass'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login

db = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])

        connection = db.connection
        cur = connection.cursor()

        result = cur.execute('SELECT * FROM Users WHERE Email=%s', [email])

        if result > 0:
            data = cur.fetchone()
            datapass = data['Password']

            if datapass == password:
                cur.close()
                return redirect(url_for('home'))
            else:
                error = 'Wrong Password!'
                return render_template('login.html',error=error)
        else:
            cur.close()
            error = 'No email found!'
            return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        major_name = str(request.form['major_name'])
        # con_password = str(request.form['con_password'])

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
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)