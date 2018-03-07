from flask import Flask, render_template, redirect, request, flash, url_for, session, g
from flask_mysqldb import MySQL
import json, requests



app = Flask(__name__)

#MySQL config
app.config['MYSQL_HOST'] = 'cs336-khp51-grader.creufxlr206t.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'cs336khp51grader'
app.config['MYSQL_PASSWORD'] = 'cs336khp51'
app.config['MYSQL_DB'] = 'ratemyclasses'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html',)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html',)

if __name__ == '__main__':
    app.run(debug=True)