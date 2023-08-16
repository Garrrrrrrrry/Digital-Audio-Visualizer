import pygame as py

def window_init(screensize):
    py.init()
    py.display.set_caption("Audio Visualizer")
    window = py.display.set_mode(screensize)
    return window, True

def draw(screen_height, screen_width, window, first, middle, last, freq_index, num_bars, multiplier):
    bars_multiplier = 0.5
    bars_width_value = 1
    bar_spacing = 5
    level_height = screen_height - (screen_height * 0.9)
    total_space = bars_width_value + bar_spacing

    visual_length = (num_bars * bar_spacing) + (num_bars * bars_width_value)
    visual_y_pos = (screen_height * 0.6)
    visual_x_start = (screen_width - visual_length)/2
    
    color = [255,255,255]
    x_pos = visual_x_start + (freq_index * total_space)
    y_pos = visual_y_pos

    #first
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos-3 , y_pos, 
                        bars_width_value/bars_multiplier, (first-level_height) * multiplier), 0, 2)
    #middle bar
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos, y_pos, 
                        bars_width_value/bars_multiplier, (middle-level_height) * multiplier), 0, 2)
    #last
    py.draw.rect(window, py.Color(*color), 
                py.Rect(x_pos+3, y_pos, 
                        bars_width_value/bars_multiplier, (last-level_height) * multiplier), 0, 2)