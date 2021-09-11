#!/usr/bin/env python3

class Ecran:
    def __init__(self, 
                 size_pixel : (int, int), 
                 size_mm : (int, int),
                 position_in_pixel : (int, int)):
        self.size_in_pixel = size_pixel
        self.size_in_mm = size_mm
        self.position_in_pixel = position_in_pixel
        
        
# $ xrandr | grep " connected"
#   eDP-1 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 309mm x 173mm
#   DVI-I-4-4 connected 1920x1080+1080+1339 (normal left inverted right x axis y axis) 0mm x 0mm
#   DVI-I-3-3 connected 1080x1920+0+0 left (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-2-2 connected primary 1920x1080+1080+259 (normal left inverted right x axis y axis) 527mm x 296mm
#   DVI-I-1-1 connected 1080x1920+3000+0 right (normal left inverted right x axis y axis) 527mm x 296mm

ecran_gauche = Ecran((1080,1920), (296,527), (0,0))
ecran_milieu = Ecran((1920,1080), (527,296), (1080,1339))
ecran_droite = Ecran((1080,1920), (296,527), (3000,0))
ecran_bas    = Ecran((1920,1080), (309,173), (1080,1339))

ecran_list = [ecran_gauche, ecran_milieu, ecran_droite, ecran_bas]