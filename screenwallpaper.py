#!/usr/bin/env python3
from ecran import Ecran
import numpy as np
import matplotlib.pyplot as plt


#TODO : get xrandr output directly
# $ xrandr | grep " connected"
#   eDP-1 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 309mm x 173mm
#   DVI-I-4-4 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 0mm x 0mm
#   DVI-I-3-3 connected 1080x1920+0+0 left (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-2-2 connected primary 1920x1080+1080+259 (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-1-1 connected 1080x1920+3000+0 right (normal left inverted right x axis y axis) 527mm x 296mm

ecran_gauche = Ecran((1080,1920), (296,527), (0,0))
ecran_milieu = Ecran((1920,1080), (527,296), (1080,259))
ecran_droite = Ecran((1080,1920), (296,527), (3000,0))
ecran_bas    = Ecran((1920,1080), (309,173), (1080,1339))

ecran_list = [ecran_gauche, ecran_milieu, ecran_droite, ecran_bas]

max_right_pixel_position = max([ecran.get_right_pixel_position() for ecran in ecran_list])
max_bottom_pixel_position = max([ecran.get_bottom_pixel_position() for ecran in ecran_list])

test = np.zeros((max_bottom_pixel_position, max_right_pixel_position), dtype='uint8')
plt.imshow(test)

def add_screen(array, screen):
    array[screen.get_top_pixel_position():screen.get_bottom_pixel_position(),
         screen.get_left_pixel_position():screen.get_right_pixel_position()] = 1
    return array

for ecran in ecran_list:
    test = add_screen(test, ecran)

plt.imshow(test)

def add_physical_screen(array, ecran, screen_pixel_per_mm, reference_position = None):
    false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm,0))
    false_pixel_hauteur = int(round(ecran.size_in_mm[1] * screen_pixel_per_mm ,0))
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) /2
    #print(f"center : {center}")
    corrected_top = ecran.get_top_pixel_position() 
    corrected_bottom = ecran.get_top_pixel_position() + false_pixel_hauteur
    #print(f"hauteur : {corrected_top} - {corrected_bottom} ")
    corrected_left = int(round(center - (false_pixel_largeur/2),0)) 
    corrected_right = int(round(center + (false_pixel_largeur/2),0))
    #print(f"largeur : {corrected_left} - {corrected_right}")
    print(f"dim : {corrected_top} : {corrected_bottom}, {corrected_left} : {corrected_right}")
    array[corrected_top : corrected_bottom, corrected_left : corrected_right ]  += 1
    return array

screen_pixel_per_mm = ecran_droite.size_in_pixel[1] / ecran_droite.size_in_mm[1]

for ecran in ecran_list:
    test = add_physical_screen(test, ecran,screen_pixel_per_mm)

plt.imshow(test)

from PIL import Image, ImageOps
  
# load the image and convert into
# numpy array

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

screen_pixel_per_mm = ecran_droite.size_in_pixel[1] / ecran_droite.size_in_mm[1]

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

