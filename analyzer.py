'''
import json
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/analyzer', method=['POST'])
def analyzer():
    try:
        name = json.loads(request.data)
        return name
    except ValueError:
        return json.dumps({'status': 1, 'info': 'request failed.'})
'''

import pafy
import re, requests, urllib

name = "beauz memories"
query = urllib.parse.urlencode({"search_query": name})
searchUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query)
searchResults = re.findall(r"watch\?v=(\S{11})", searchUrl.read().decode())
videoUrl = "https://www.youtube.com/watch?v=" + "{}".format(searchResults[0])

video = pafy.new(videoUrl)

audioLink = video.getbestaudio()