import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

height = 10
width = 10
count = 0
interval = 4

folder_name = "color"
try: 
    os.mkdir(folder_name) 
except OSError as error: 
    print(error) 

def check_RGB_range(R,G,B):
    if R < 0: R = 0
    if G < 0: G = 0
    if B < 0: B = 0
    if R > 255: R = 255
    if G > 255: G = 255
    if B > 255: B = 255
    return R,G,B

def save_RGB_image(R,G,B,count):
    image = np.full((height ,width ,3),(R,G,B),dtype=np.uint8)
    image_name = str(count).zfill(3)+".png"	#補零補到三位數 對齊
    # print(image_name)    
    cv2.imwrite(folder_name + "/" + image_name, image)

def show_RGB_image(R,G,B,count):
    image = np.full((height ,width ,3),(R,G,B),dtype=np.uint8)
    image_name = str(count).zfill(3)+".png"
    if(count%10==0):
        plt.imshow(image)
        plt.title(image_name)
        plt.show(block=False)
        plt.axis('off')
        plt.pause(0.000001)
        plt.clf()
        
R,G,B=0,0,0

'''
    Color State:
    0 => black 0, 0, 0
    1 => white 255, 255, 255
    2 => red 255, 0, 0
    3 => yellow 255, 255, 0
    4 => green 0, 255, 0
    5 => cyan 0, 255, 255
    6 => blue 0, 0, 255
    7 => magenta 255, 0, 255
''' 
state = 0


while(1):
    save_RGB_image(R,G,B,count)
    show_RGB_image(R,G,B,count)
    print(R,G,B)
    count = count + 1

    if (state == 0):
        R = R + interval
        G = G + interval
        B = B + interval
    if (state == 1):
        R = R
        G = G - interval
        B = B - interval
    if (state == 2):
        R = R
        G = G + interval
        B = B
    if (state == 3):
        R = R - interval
        G = G
        B = B
    if (state == 4):
        R = R
        G = G
        B = B + interval
    if (state == 5):
        R = R
        G = G - interval
        B = B
    if (state == 6):
        R = R + interval
        G = G
        B = B
    if (state == 7):
        R = R - interval
        G = G
        B = B - interval
        
    R,G,B = check_RGB_range(R,G,B)

    if(R == 0 and G == 0 and B == 0): state = 0;  break;
    if(R == 255 and G == 255 and B == 255): state = 1
    if(R == 255 and G == 0 and B == 0): state = 2
    if(R == 255 and G == 255 and B == 0): state = 3
    if(R == 0 and G == 255 and B == 0): state = 4
    if(R == 0 and G == 255 and B == 255): state = 5
    if(R == 0 and G == 0 and B == 255): state = 6
    if(R == 255 and G == 0 and B == 255): state = 7
