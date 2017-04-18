from flask import Flask, render_template, request, jsonify, escape, redirect, abort, url_for, make_response
from pony.orm import *
from datetime import datetime
from hashlib import sha512
from uuid import uuid4
from urllib.parse import quote

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('projects.html')


@app.route('/structure')
def structure():
    return render_template('structure.html')



if __name__ == '__main__':
    app.run()
