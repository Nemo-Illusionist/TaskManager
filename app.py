from flask import Flask, render_template, request, redirect, jsonify

from Services.UserManager import Authorization

app = Flask(__name__)
app.debug = True


def auth(login, password):
    return True


def getSession():
    return 123  # request.cookies.get('session_key')


def render(rend):
    if getSession() is None:
        return redirect('/login', 301)
    return rend


@app.route('/')
def index():
    return render(redirect('/projects', 301))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render(render_template('registration.html'))


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
        return render(render_template('projects.html'))


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return render(render_template('tasks.html'))


if __name__ == '__main__':
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()
