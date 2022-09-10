from flask import Flask, render_template, redirect, url_for, request

import re
import urllib

import subprocess
import os

import pygame as py
import librosa
import librosa.display
import matplotlib.pyplot as plt 
import numpy as np
import time
import ctypes

# getting audio link/download audio
def input(name):
    query = urllib.parse.urlencode({"search_query": name})
    searchUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query)
    searchResults = re.findall(r"watch\?v=(\S{11})", searchUrl.read().decode())
    return ("https://www.youtube.com/watch?v=" + "{}".format(searchResults[0]))

# CHANGES webm to wav
def formatAudio(videoUrl):
    command1 = ["youtube-dl", "-f", "bestaudio", "--extract-audio", 
                "--audio-format", "mp3", videoUrl, "-o", "./audio/firstOutput.mp3"]
    subprocess.run(command1, stdout=subprocess.PIPE, text=True)

    command2 = ["ffmpeg", "-i", "./audio/firstOutput.mp3", "-y", "./audio/outputAudio.wav"]
    subprocess.run(command2, stdout=subprocess.PIPE, text=True)

def get_decibel(target_time, freq):
    return s_h[int(freq * frequencies_to_index)][int(target_time * time_to_index)]
#audio visualizer
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_width = screensize[0]
screen_height = screensize[1]

py.init()
py.display.set_caption("Audio Visualizer")
window = py.display.set_mode(screensize)
clock = py.time.Clock()
running = True

def draw(first, middle, last, freq_index, num_bars, multiplier):
    bars_multiplier = 3

    bars_width_value = 12 * bars_multiplier
    bar_spacing = 8 * bars_multiplier

    total_space = bars_width_value + bar_spacing

    visual_length = (num_bars * bar_spacing) + (num_bars * bars_width_value)
    visual_y_pos = screen_height * 0.6
    visual_x_start = (screen_width - visual_length)/2
    
    color = [255,255,255]
    x_pos = visual_x_start + (freq_index * total_space)
    y_pos = visual_y_pos

    #first
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos-20 , y_pos, 
                        bars_width_value/bars_multiplier, (first-80) * multiplier), 0, 2)
    #middle bar
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos, y_pos, 
                        bars_width_value/bars_multiplier, (middle-80) * multiplier), 0, 2)
    #last
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos+20, y_pos, 
                        bars_width_value/bars_multiplier, (last-80) * multiplier), 0, 2)

def interface():
    global running 
    global hud
    for event in [e for e in py.event.get() if e.type == py.KEYDOWN]:
        # exit programm
        if event.key == py.K_ESCAPE:
            running = False

def reset():
    if os.path.exists("./audio/firstOutput.mp3"):
        os.remove("./audio/firstOutput.mp3")
            
def app():
    global s_h, time_to_index, frequencies_to_index
    #set value to 0 to keep some and 1 before changing songs
    value = 0
    if(value == 1):
        reset()
        name = "Infection - Don't Say A Word"
        videoUrl = input(name)
        formatAudio(videoUrl)

    #librosa setup
    filename = './audio/outputAudio.wav'
    y, sr = librosa.load(filename, sr = 44100)

    fft = librosa.stft(y, n_fft = 2048)
    fft_h, fft_p = librosa.decompose.hpss(fft, margin = 60.0)
    s_h = librosa.amplitude_to_db(fft_h, ref = np.max)

    frequencies = librosa.core.fft_frequencies(sr = sr, n_fft = 2048)
    time = librosa.core.frames_to_time(np.arange(s_h.shape[1]), sr = sr, n_fft = 2048)
    time_to_index = len(time)/time[len(time) - 1]
    frequencies_to_index = len(frequencies)/frequencies[len(frequencies)-1]

    #number of bars
    spectrum = np.arange(500, 1445, 45)

    py.mixer.music.load(filename)
    py.mixer.music.play(0)

    while running:
        interface() 
        window.fill(py.Color(0,0,0))        
        for Hz in spectrum:
            first = np.abs(int(get_decibel(py.mixer.music.get_pos()/1000.0, Hz-10)))
            middle = np.abs(int(get_decibel(py.mixer.music.get_pos()/1000.0, Hz)))
            last = np.abs(int(get_decibel(py.mixer.music.get_pos()/1000.0, Hz+10)))
            index = int(np.where(spectrum == Hz)[0])
            #index = spectrum.index(Hz)
            draw(first, middle, last, index, len(spectrum), multiplier = 3.5)
        
        py.display.update()
app()
py.quit()