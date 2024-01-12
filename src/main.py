import pygame as py
import librosa
import librosa.display
import numpy as np
import ctypes

from intializeWav import get_decibel, reset
from screen import window_init, draw

#main variables to control songs
song_name = "Benny Blanco - Eastside" #input song name
value = 1 #set value to 0 to keep song | 1 to change songs

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_width = screensize[0]
screen_height = screensize[1]

def interface():
    for event in [e for e in py.event.get() if e.type == py.KEYDOWN]:
        # exit program
        if event.key == py.K_ESCAPE:
            return False
    return True

def app():
    global s_h, time_to_index, frequencies_to_index
    global level_height, ratio
    ratio = 2.5
    level_height = screen_height - (screen_height * 0.9)

    window, running = window_init(screensize)
    
    name = song_name

    if(value == 1):
        reset(name)

    #librosa setup
    filename = "../audio/outputAudio.wav"
    (y, sr) = librosa.load(filename, sr = 44100)

    fft = librosa.stft(y, n_fft = 2048)
    s_h = librosa.amplitude_to_db(fft, ref = np.max)

    frequencies = librosa.core.fft_frequencies(sr = sr, n_fft = 2048)
    time = librosa.core.frames_to_time(np.arange(s_h.shape[1]), sr = sr, n_fft = 2048)
    time_to_index = len(time)/time[len(time) - 1]
    frequencies_to_index = len(frequencies)/frequencies[len(frequencies)-1]

    spectrum = np.arange(20, 2000, 20)

    py.mixer.music.load(filename)
    py.mixer.music.play(0)

    l1 = l2 = l3 = 50

    while running:
        running = interface() 
        window.fill(py.Color(0,0,0))        
        for Hz in spectrum:
            f = np.abs(int(get_decibel(s_h, py.mixer.music.get_pos()/1000.0, Hz-10, frequencies_to_index, time_to_index)))
            m = np.abs(int(get_decibel(s_h, py.mixer.music.get_pos()/1000.0, Hz, frequencies_to_index, time_to_index)))
            l = np.abs(int(get_decibel(s_h, py.mixer.music.get_pos()/1000.0, Hz+10, frequencies_to_index, time_to_index)))
            first = f * (ratio**(f/41))
            middle = m * (ratio**(m/40))
            last = l * (ratio**(l/41))
            if(first > level_height):
                first = level_height + 1
            if(middle > level_height):
                middle = level_height + 1
            if(last > level_height):
                last = level_height + 1
            if(first == l1):
                first = first + 1
            if(middle == l2):
                middle = middle + 1
            if(last == l3):
                last = last + 1
            l1 = first
            l2 = middle
            l3 = last
            index = int(np.where(spectrum == Hz)[0])
            draw(screen_height, screen_width, window, first, middle, last, index, len(spectrum), multiplier = 1)
        
        py.display.update()

app()
py.quit()