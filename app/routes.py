try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
except:
    print("Make sure to pip install Flask twilio")
from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

# Home page, renders the index.html template
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# Pig latin page, when we click translate, moves to text result page
@app.route('/text',methods=['GET','POST'])
def text():
    if request.method == 'POST':
        old_text = request.form['text']
        print(request.form['text2'])
        return render_template('textResults.html', old_text=old_text, new_text='new_text')
    return render_template('text.html', title='Home')