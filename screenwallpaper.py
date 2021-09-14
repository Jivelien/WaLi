#!/usr/bin/env python3
from ecran import Ecran
import numpy as np
import matplotlib.pyplot as plt


def get_screens_information():
    import os
    os.system('xrandr --verbose | grep " connected"> screens.txt')
    
    xrandr_screens = open('screens.txt', 'rt')
    screens_list = xrandr_screens.readlines()
    screens_list = [screen.replace('\n','') for screen in screens_list]
    screens_list = [screen.replace('(normal left inverted right x axis y axis)','') for screen in screens_list]
    screens_list = [screen.replace(' x ','x') for screen in screens_list]
    
    screens = []
    
    for screen_parameters in screens_list:
        sps = screen_parameters.split()
    
        screen_orientation = sps[-2]
        size_in_mm = tuple([int(elem) for elem in sps[-1].replace('mm','').split('x')])
        if screen_orientation in ['left', 'right']:
            size_in_mm = tuple(reversed(size_in_mm))
            
        screen_resolution_and_position = sps[-4]
        screen_resolution_description = screen_resolution_and_position.split('+')[0]
        screen_resolution = tuple([int(elem) for elem in screen_resolution_description.split('x')])
        
        screen_position = tuple([int(elem) for elem in screen_resolution_and_position.split('+')[1:]])
        
        screens.append(Ecran(screen_resolution, size_in_mm, screen_position))
    
    return screens

    
#TODO : get xrandr output directly
# $ xrandr | grep " connected"
#   eDP-1 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 309mm x 173mm
#   DVI-I-4-4 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 0mm x 0mm
#   DVI-I-3-3 connected 1080x1920+0+0 left (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-2-2 connected primary 1920x1080+1080+259 (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-1-1 connected 1080x1920+3000+0 right (normal left inverted right x axis y axis) 527mm x 296mm

# ecran_gauche = Ecran((1080,1920), (296,527), (0,0))
# ecran_milieu = Ecran((1920,1080), (527,296), (1080,259))
# ecran_droite = Ecran((1080,1920), (296,527), (3000,0))
# ecran_bas    = Ecran((1920,1080), (309,173), (1080,1339))

# ecran_list = [ecran_gauche, ecran_milieu, ecran_droite, ecran_bas]

screens = get_screens_information()

max_right_pixel_position = max([ecran.get_right_pixel_position() for ecran in screens])
max_bottom_pixel_position = max([ecran.get_bottom_pixel_position() for ecran in screens])


# def add_screen(array, screen):
#     array[screen.get_top_pixel_position():screen.get_bottom_pixel_position(),
#          screen.get_left_pixel_position():screen.get_right_pixel_position()] = 1
#     return array

# for ecran in screens:
#     test = add_screen(test, ecran)

# plt.imshow(test)
# plt.show()

# def add_physical_screen(array, ecran, screen_pixel_per_mm, reference_position = None):
#     false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm,0))
#     false_pixel_hauteur = int(round(ecran.size_in_mm[1] * screen_pixel_per_mm ,0))
#     center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) /2
#     #print(f"center : {center}")
#     corrected_top = ecran.get_top_pixel_position() 
#     corrected_bottom = ecran.get_top_pixel_position() + false_pixel_hauteur
#     #print(f"hauteur : {corrected_top} - {corrected_bottom} ")
#     corrected_left = int(round(center - (false_pixel_largeur/2),0)) 
#     corrected_right = int(round(center + (false_pixel_largeur/2),0))
#     #print(f"largeur : {corrected_left} - {corrected_right}")
#     print(f"dim : {corrected_top} : {corrected_bottom}, {corrected_left} : {corrected_right}")
#     array[corrected_top : corrected_bottom, corrected_left : corrected_right ]  += 1
#     return array

#TODO find bigger screen as reference
screen_pixel_per_mm = screens[1].size_in_pixel[1] / screens[1].size_in_mm[1]

test = np.zeros((max_bottom_pixel_position, max_right_pixel_position), dtype='uint8')
# for ecran in screens:
#     test = add_physical_screen(test, ecran,screen_pixel_per_mm)

# plt.imshow(test)

from PIL import Image, ImageOps
  
#TODO : image name in args
img = Image.open('earth.jpg')
resized_img = ImageOps.fit(img, (max_right_pixel_position,max_bottom_pixel_position))

numpydata = np.asarray(resized_img)

#TODO shape depend of picture 

def get_correct_top_position(ecran, screen_pixel_per_mm, reference_position = None):
    return ecran.get_top_pixel_position()

def get_correct_bottom_position(ecran, screen_pixel_per_mm, reference_position = None):
    false_pixel_hauteur = int(round(ecran.size_in_mm[1] * screen_pixel_per_mm ,0))
    return ecran.get_top_pixel_position() + false_pixel_hauteur
    
def get_correct_left_position(ecran, screen_pixel_per_mm, reference_position = None):
    false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm,0))
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) /2
    return int(round(center - (false_pixel_largeur/2),0)) 

def get_correct_right_position(ecran, screen_pixel_per_mm, reference_position = None):
    false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm,0))
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) /2
    return int(round(center + (false_pixel_largeur/2),0))    

left = numpydata[
    get_correct_top_position(ecran_gauche, screen_pixel_per_mm) : 
    get_correct_bottom_position(ecran_gauche, screen_pixel_per_mm) , 
    get_correct_left_position(ecran_gauche, screen_pixel_per_mm)  : 
    get_correct_right_position(ecran_gauche, screen_pixel_per_mm) ]
middle = numpydata[
    get_correct_top_position(ecran_milieu, screen_pixel_per_mm) : 
    get_correct_bottom_position(ecran_milieu, screen_pixel_per_mm) , 
    get_correct_left_position(ecran_milieu, screen_pixel_per_mm)  : 
    get_correct_right_position(ecran_milieu, screen_pixel_per_mm) ]
right = numpydata[
    get_correct_top_position(ecran_droite, screen_pixel_per_mm) : 
    get_correct_bottom_position(ecran_droite, screen_pixel_per_mm) , 
    get_correct_left_position(ecran_droite, screen_pixel_per_mm)  : 
    get_correct_right_position(ecran_droite, screen_pixel_per_mm) ]
bottom = numpydata[
    get_correct_top_position(ecran_bas, screen_pixel_per_mm) : 
    get_correct_bottom_position(ecran_bas, screen_pixel_per_mm) , 
    get_correct_left_position(ecran_bas, screen_pixel_per_mm)  : 
    get_correct_right_position(ecran_bas, screen_pixel_per_mm) ]

corrected_img_left = np.asarray(Image.fromarray(left).resize(ecran_gauche.size_in_pixel))
corrected_img_middle = np.asarray(Image.fromarray(middle).resize(ecran_milieu.size_in_pixel))
corrected_img_right = np.asarray(Image.fromarray(right).resize(ecran_droite.size_in_pixel))
corrected_img_bottom = np.asarray(Image.fromarray(bottom).resize(ecran_bas.size_in_pixel))


wallpaper_correct = np.zeros((max_bottom_pixel_position, max_right_pixel_position, 3), dtype='uint8')

wallpaper_correct[ecran_gauche.get_top_pixel_position():ecran_gauche.get_bottom_pixel_position(),
                  ecran_gauche.get_left_pixel_position():ecran_gauche.get_right_pixel_position()] = corrected_img_left

wallpaper_correct[ecran_milieu.get_top_pixel_position():ecran_milieu.get_bottom_pixel_position(),
                  ecran_milieu.get_left_pixel_position():ecran_milieu.get_right_pixel_position()] = corrected_img_middle

wallpaper_correct[ecran_droite.get_top_pixel_position():ecran_droite.get_bottom_pixel_position(),
                  ecran_droite.get_left_pixel_position():ecran_droite.get_right_pixel_position()] = corrected_img_right

wallpaper_correct[ecran_bas.get_top_pixel_position():ecran_bas.get_bottom_pixel_position(),
                  ecran_bas.get_left_pixel_position():ecran_bas.get_right_pixel_position()] = corrected_img_bottom

plt.imshow(wallpaper_correct)

wallpaper_pic = Image.fromarray(wallpaper_correct)

import time
now = int(time.time())
wallpaper_pic.save(f"test_{now}.jpg")

