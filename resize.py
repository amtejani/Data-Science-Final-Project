from PIL import Image
import os

path = 'data/small/poster/'
height = 114

for f in os.listdir(path):
    with Image.open(path+f) as img:
        w,h = img.size
        if h < height:
            img = img.crop((0,(h-height)/2,92,(h+height)/2))
        else:
            img = img.crop((0,(h-height)/2,92,(h+height)/2))
        img.save(path+f)