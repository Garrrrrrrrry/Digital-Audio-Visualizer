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
    output_mp3 = "../audio/firstOutput.mp3"
    command_mp3 = [
        "yt-dlp", videoUrl,
        "--format", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_mp3
    ]
    #command1 = ["youtube-dl", "-f", "bestaudio", "--extract-audio", 
    #            "--audio-format", "mp3", videoUrl, "-o", "../audio/firstOutput.mp3"]
    result = subprocess.run(command_mp3, stdout=subprocess.PIPE, text=True)
    print(result.stdout)
    
    output_wav = "../audio/outputAudio.wav"
    command_wav = [
        "ffmpeg", "-i", 
        "../audio/firstOutput.mp3", 
        "-y", output_wav
    ]
    result = subprocess.run(command_wav, stdout=subprocess.PIPE, text=True)
    print(result.stdout)

def get_decibel(s_h, target_time, freq, freq_to_index, time_to_index):
    return s_h[int(freq * freq_to_index)][int(target_time * time_to_index)]

def reset(song_name):
    while os.path.exists("../audio/firstOutput.mp3"):
        print("Removing File. Waiting...")
        os.remove("../audio/firstOutput.mp3")
        time.sleep(1)
    videoUrl = input(song_name)
    formatAudio(videoUrl)