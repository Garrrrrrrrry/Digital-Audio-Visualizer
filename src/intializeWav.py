import re
import urllib
import urllib.parse
import urllib.request
import subprocess
import os
import time

def input(name):
    query = urllib.parse.urlencode({"search_query": name})
    searchUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query)
    searchResults = re.findall(r"watch\?v=(\S{11})", searchUrl.read().decode())
    return ("https://www.youtube.com/watch?v=" + "{}".format(searchResults[0]))

def formatAudio(videoUrl):
    command1 = ["youtube-dl", "-f", "bestaudio", "--extract-audio", 
                "--audio-format", "mp3", videoUrl, "-o", "../audio/firstOutput.mp3"]
    subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    #command2 = ["ffmpeg", "-i", "../audio/firstOutput.mp3", "-y", "../audio/outputAudio.wav"]
    #subprocess.run(command2, stdout=subprocess.PIPE, text=True)

def get_decibel(s_h, target_time, freq, freq_to_index, time_to_index):
    return s_h[int(freq * freq_to_index)][int(target_time * time_to_index)]

def reset(song_name):
    while os.path.exists("../audio/firstOutput.mp3"):
        print("Removing File. Waiting...")
        os.remove("../audio/firstOutput.mp3")
        time.sleep(1)
    videoUrl = input(song_name)
    formatAudio(videoUrl)