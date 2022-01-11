
from ecran import Ecran
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import os


def get_screens_information():
    os.system('xrandr --verbose | grep " connected"> screens.txt')

    xrandr_screens = open('screens.txt', 'rt')
    screens_list = xrandr_screens.readlines()
    screens_list = [screen.replace('\n', '') for screen in screens_list]
    screens_list = [screen.replace('(normal left inverted right x axis y axis)', '') for screen in screens_list]
    screens_list = [screen.replace(' x ', 'x') for screen in screens_list]

    screens = []
    for screen_parameters in screens_list:
        try:
            sps = screen_parameters.split()
            print(sps)
            screen_orientation = sps[-2]
            size_in_mm = tuple([int(elem) for elem in sps[-1].replace('mm', '').split('x')])
            if screen_orientation in ['left', 'right']:
                size_in_mm = tuple(reversed(size_in_mm))

            screen_resolution_and_position = sps[-4]
            screen_resolution_description = screen_resolution_and_position.split('+')[0]
            screen_resolution = tuple([int(elem) for elem in screen_resolution_description.split('x')])

            screen_position = tuple([int(elem) for elem in screen_resolution_and_position.split('+')[1:]])

            screens.append(Ecran(screen_resolution, size_in_mm, screen_position))
        except:
            pass

    return screens


screens = get_screens_information()

max_right_pixel_position = max([ecran.get_right_pixel_position() for ecran in screens])
max_bottom_pixel_position = max([ecran.get_bottom_pixel_position() for ecran in screens])

# TODO find bigger screen as reference
screen_pixel_per_mm = screens[1].size_in_pixel[1] / screens[1].size_in_mm[1]

import sys

image_name = sys.argv[1]
img = Image.open(image_name)
resized_img = ImageOps.fit(img, (max_right_pixel_position, max_bottom_pixel_position))

numpydata = np.asarray(resized_img)[:, :, :3]


def get_correct_top_position(ecran, screen_pixel_per_mm, reference_position=None):
    return ecran.get_top_pixel_position()


def get_correct_bottom_position(ecran, screen_pixel_per_mm, reference_position=None):
    false_pixel_hauteur = int(round(ecran.size_in_mm[1] * screen_pixel_per_mm, 0))
    return ecran.get_top_pixel_position() + false_pixel_hauteur


def get_correct_left_position(ecran, screen_pixel_per_mm, reference_position=None):
    false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm, 0))
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) / 2
    return int(round(center - (false_pixel_largeur / 2), 0))


def get_correct_right_position(ecran, screen_pixel_per_mm, reference_position=None):
    false_pixel_largeur = int(round(ecran.size_in_mm[0] * screen_pixel_per_mm, 0))
    center = (ecran.get_left_pixel_position() + ecran.get_right_pixel_position()) / 2
    return int(round(center + (false_pixel_largeur / 2), 0))


wallpaper_correct = np.zeros((max_bottom_pixel_position, max_right_pixel_position, 3), dtype='uint8')

for screen in screens:
    left = numpydata[
           max(0, get_correct_top_position(screen, screen_pixel_per_mm)):
           get_correct_bottom_position(screen, screen_pixel_per_mm),
           max(0, get_correct_left_position(screen, screen_pixel_per_mm)):
           get_correct_right_position(screen, screen_pixel_per_mm)]
    corrected_img_left = np.asarray(Image.fromarray(left).resize(screen.size_in_pixel))
    wallpaper_correct[screen.get_top_pixel_position():screen.get_bottom_pixel_position(),
    screen.get_left_pixel_position():screen.get_right_pixel_position()] = corrected_img_left

plt.imshow(wallpaper_correct)

wallpaper_pic = Image.fromarray(wallpaper_correct)

import time

now = int(time.time())
wallpaper_pic.save(f"{now}.jpg")

os.system(f'gsettings set org.gnome.desktop.background picture-uri "$(pwd)/{now}.jpg"')
os.system(f'gsettings set org.gnome.desktop.background picture-options "spanned"')
