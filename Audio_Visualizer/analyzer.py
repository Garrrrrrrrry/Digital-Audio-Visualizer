from flask import Flask, redirect, url_for, request
from flask import make_response

if request.method == 'Post':
    name = request.form['param']

    # include 3+ here:____________

    #result = ""
    # response = make_response('{"response": '+result'}')
    # return response
