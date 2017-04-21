from flask import Flask, render_template, request, jsonify, escape, redirect, abort, url_for, make_response
from pony.orm import *
from datetime import datetime
from hashlib import sha512
from uuid import uuid4
from urllib.parse import quote

app = Flask(__name__)
app.debug = True


def auth(login, password):
    return True


def hash(salt, password):
    return sha512((salt + password).encode('utf-8')).hexdigest()


def getSession():
    return 123#request.cookies.get('session_key')


@app.route('/')
def index():
    if getSession() is None:
        return redirect('/login', 301)
    return redirect('/projects', 301)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if getSession() is None:
            return render_template('login.html')
        return redirect('/projects', 301)
    userLogin = request.form['login']
    password = request.form['password']
    if auth(userLogin, password):
        # создание сессии
        return redirect('/projects', 301)
    return render_template('login.html', message="Неверное имя пользователя или пароль")


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        if getSession() is None:
            return redirect('login.html', 301)
        return render_template('projects.html')


@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        if getSession() is None:
            return redirect('login.html', 301)
        return render_template('tasks.html')


if __name__ == '__main__':
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()
