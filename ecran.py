# -*- coding: utf-8 -*-

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