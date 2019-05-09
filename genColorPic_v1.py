import cv2  # Not actually necessary if you just want to create an image.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

height = 10
width = 10
count = 0
interval = 16

for R in range(0, 256 , interval):
    for G in range(0, 256 , interval):
        for B in range(0, 256 , interval):
            #image = np.zeros((height, width, 3), np.uint8)
            '''another way to fill image'''
            #image[:] = (255,0,0)
            
            image = np.full((height ,width ,3),(R,G,B),dtype=np.uint8)
            '''uint8 range is 0 to 255'''
            
            #print(image)
            #print(image.shape)
            image_name = str(count)+".png"
            print(image_name)
            
            if(count%100==0):
                plt.imshow(image)
                plt.title(image_name)
                plt.show(block=False)
                plt.axis('off')
                plt.pause(0.000001)
                plt.clf()
                

            cv2.imwrite(str(count)+'.png', image)
            count=count+1


