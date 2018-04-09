from flask import Flask, render_template, redirect, request, flash, url_for, session, g, jsonify
from flask_mysqldb import MySQL
from functools import wraps
from util import *
import os, json



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

        if username.lower() == 'admin' and password.lower() == 'admin':
            return redirect(url_for('admin'))

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

@app.errorhandler(500)
def page_not_found(e):
    flash('Refresh Page and search for review!')
    return render_template("review.html")


@app.route('/createReview', methods=['GET', 'POST'])
def createReview():
    user = g.user
    connection = db.connection
    cur = connection.cursor()
    cur.execute('SELECT Class_name, Class_id, dept_id FROM ratemyclass.Classes;')
    classes = cur.fetchall()
    db.connection.commit()
    cur.close()
    if request.method == 'POST':
        user = str(request.form['user'])
        classN = str(request.form['Class'])
        semester = str(request.form['Semester'])
        year = str(request.form['Year'])
        diff = str(request.form['Difficulty'])
        knowled = str(request.form['Knowledge'])
        review = str(request.form['Review'])

        if user == 'None':
            flash('Please fill out the username field with your username')
            return render_template('review.html', classes=classes, user=user)

        cur = connection.cursor()
        result = cur.execute("SELECT * FROM Reviews WHERE Username = %s and Class_id = %s", [user,classN])

        if result > 0:
            flash('You already submitted a post with this username', 'danger')
            return render_template('review.html', classes=classes, user=user)

        cur.close()

        user = g.user
        print(classN, semester, year, diff, knowled, review)

        cur = connection.cursor()
        cur.execute('INSERT INTO Reviews (Class_id, Difficulty_rating, knowledge_gain_rating, review, Username, Review_year, Review_semester) VALUES (%s, %s, %s, %s, %s, %s, %s)', (classN, diff, knowled, review, user, year, semester))
        db.connection.commit()
        cur.close()
        flash('Submitted Review!','success')

        return redirect(url_for('home'))

    return render_template('review.html', classes=classes, user=user)

@app.route('/home', methods=['GET', 'POST'])
def home():

        dept_id = ''
        class_name = ''
        classlist = []
        cList = []
        avg=[]
        avg2=[]
        avg_diff = ''
        avg_kno = ''
        connection = db.connection
        cur = connection.cursor()
        cur.execute('SELECT * FROM Classes;')
        classlist = cur.fetchall()

        db.connection.commit()
        cur.close()
        # dicts = clean(deptlist)

        if request.method == 'POST':
            class_id = str(request.form['class_id'])


            cur = connection.cursor()
            cur.execute("SELECT * FROM Reviews WHERE class_id = %s",[class_id])
            cList = cur.fetchall()
            cur.execute("SELECT avg(Difficulty_rating), avg(knowledge_gain_rating) FROM Reviews where Class_id = %s", [class_id])
            avg = cur.fetchall()
            db.connection.commit()
            cur.close()
        # print(deptlist)
        # print(deptlist[0]['dept_id'])
            for i in avg:
                avg2.append(i)
            avg_diff = avg2[0]['avg(Difficulty_rating)']
            avg_kno = avg2[0]['avg(knowledge_gain_rating)']

        return render_template('home.html', classlist=classlist, cList = cList, avg_diff=avg_diff, avg_kno=avg_kno)
    # else:
    #     flash('Use the front door!','danger')
    #     return redirect(url_for('login'))




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    g.user = admin
    userlist = []
    selected = []
    connection = db.connection
    cur = connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Users.Username NOT IN(SELECT Username FROM Reviews);")
    userlist = cur.fetchall()
    # db.connection.commit()
    cur.close()

    if request.method == 'POST':
        selected = request.form.getlist('user_box')
        print(selected)
        connection = db.connection
        cur = connection.cursor()
        for user in selected:
                cur.execute("DELETE FROM Users WHERE Username = %s;",[user])
                db.connection.commit()
        cur.close()
        message = 'Users: {} deleted'.format(selected)
        flash(message,'success')
        return render_template('admin.html', userlist=userlist)

    return render_template('admin.html', userlist = userlist)


#
# if __name__ == '__main__':
#     app.run(debug=True)