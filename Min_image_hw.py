#!/usr/bin/env python3
from PIL import Image
import os
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

path = os.path.dirname(__file__)+'/data/pizza_data/images'
# set an initial value which no image will meet
minw = 10000000
minh = 10000000
maxw = 0
maxh = 0
w_list = []
h_list = []


for image in tqdm(os.listdir(path)):
    # get the image height & width
    image_location = os.path.join(path, image)
    im = Image.open(image_location)
    data = im.size
    # if the width is lower than the last image, we have a new "winner"
    w = data[0]
    if w < minw:
        newminw = w, image_location
        minw = w
    # if the height is lower than the last image, we have a new "winner"
    h = data[1]
    if h < minh:
        newminh = h, image_location
        minh = h

    if w > maxw:
        newmaxw = w, image_location
        maxw = w
    # if the height is lower than the last image, we have a new "winner"

    if h > maxh:
        newmaxh = h, image_location
        maxh = h

    w_list.append(w)
    h_list.append(h)
# finally, print the values and corresponding files
print("minwidth", newminw)
print("minheight", newminh)
print("maxwidth", newmaxw)
print("maxheight", newmaxh)

fig2 = plt.figure()
plt.hist2d(np.array(w_list), np.array(h_list), bins=50)
plt.xlabel('Image Width')
plt.ylabel('Image Height')
cbar = plt.colorbar()
cbar.ax.set_ylabel('Counts')

plt.show()

with open(os.path.dirname(__file__)+'/data/pizza_data/imageLabels.txt') as f:
    labels = f.readlines()


with open(os.path.dirname(__file__)+'/data/pizza_data/categories.txt') as f:
    categories = [item.strip() for item in f.readlines()]

split_labels = [[int(label) for label in line.strip().split('  ')] for line in labels]
label_df = pd.DataFrame(split_labels, columns = categories)
print(label_df.sum())
label_df.sum().plot(kind = 'bar')
plt.tight_layout()
plt.show()


cat_dct = {v: k.strip() for v, k in enumerate(categories)}



pizza_labels = [tuple([cat_dct[key] for key,val in enumerate(entry) if val==1]) for entry in split_labels]


print(Counter(pizza_labels))