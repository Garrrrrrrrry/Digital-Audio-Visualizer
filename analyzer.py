from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/', method=['GET', 'POST'])
def main():
    if request.method == 'Post':
        name = request.form['param']

        result = name + "hiiiiii2"
        return render_template('response', result)
