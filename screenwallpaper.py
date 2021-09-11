#!/usr/bin/env python3

class Ecran:
    def __init__(self, 
                 size_pixel : (int, int), 
                 size_mm : (int, int),
                 position_in_pixel : (int, int)):
        self.size_in_pixel = size_pixel # largeur , hauteur
        self.size_in_mm = size_mm  # largeur , hauteur
        self.position_in_pixel = position_in_pixel
        
    def get_left_pixel_position(self):
        return  self.position_in_pixel[0]
        
    def get_top_pixel_position(self):
        return self.position_in_pixel[1]
    
    def get_right_pixel_position(self):
        return self.position_in_pixel[0] + self.size_in_pixel[0]

    def get_bottom_pixel_position(self):
        return self.position_in_pixel[1] + self.size_in_pixel[1]


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

import numpy as np
import matplotlib.pyplot as plt

test = np.zeros((max_bottom_pixel_position, max_right_pixel_position))
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
    print(f"corrected largeur : {false_pixel_largeur}")
    false_pixel_hauteur = int(round(ecran.size_in_mm[1] * screen_pixel_per_mm ,0))
    print(f"corrected largeur : {false_pixel_hauteur}")
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) /2
    print(f"center : {center}")
    
    corrected_top = ecran.get_top_pixel_position() 
    corrected_bottom = ecran.get_top_pixel_position() + false_pixel_hauteur
    print(f"hauteur : {corrected_top} - {corrected_bottom} ")
    
    corrected_left = int(round(center - (false_pixel_largeur/2),0)) 
    corrected_right = int(round(center + (false_pixel_largeur/2),0))
    print(f"largeur : {corrected_left} - {corrected_right} ")
    
    array[corrected_top : corrected_bottom, corrected_left : corrected_right ]  += 1

    return array

screen_pixel_per_mm = ecran_droite.size_in_pixel[1] / ecran_droite.size_in_mm[1]

for ecran in ecran_list:
    test = add_physical_screen(test, ecran,screen_pixel_per_mm)
    
    
test = np.zeros((max_bottom_pixel_position, max_right_pixel_position))

_ = add_physical_screen(test, ecran_gauche,screen_pixel_per_mm)
_ = add_physical_screen(test, ecran_milieu,screen_pixel_per_mm)
_ = add_physical_screen(test, ecran_droite,screen_pixel_per_mm)
_ = add_physical_screen(test, ecran_bas,screen_pixel_per_mm)

plt.imshow(test)
    