# python3 crop_v1.py -p /home/kinga/crop2/img_to_test -ih 339 -iw 512 -in 256

# -p    <- folder z obrazami (zamiast -p można wpisać '--path' )
# -ih   <- wysokość docelowa obrazu (zamiast -ih można wpisać '--stride_h' )
# -iw   <- szerokość docelowa obrazu (zamiast -iw można wpisać '--stride_w' )
# -in   <- krok podziału (zamiast -in można wpisać '--interval' )

# W przypadku podziału części obrazu, można go ograniczyć w liniach 59-62

# W przypadku podziału całego obrazu, należy skomentować linie 59-62
# oraz odkomentować linie 52-55

# !!! Folder z nowymi obrazami tworzy się automatycznie
# Zmiana nazwy folderu w linii 63

# Nowe nazwy plików to trzy ostatnie znaki starej nazwy + numer (zaczynając od 1)
# Zmiana nazwy w linii 83

import argparse
import cv2
from os import makedirs
from PIL import Image
import numpy as np
import os

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="Path to the image")
ap.add_argument("-ih", "--stride_h", type=int, required=True, help="Stride heigh")
ap.add_argument("-iw", "--stride_w", type=int, required=True, help="Stride width")
ap.add_argument("-in", "--interval", type=int, required=True, help="Size")
args = vars(ap.parse_args())

folder_path = args["path"]
images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def loadImage(fname):
    return np.asarray(Image.open(fname))

X = [ loadImage(fname) for fname in images]
X = np.array(X)

interval = args["interval"]
stride_h = args["stride_h"]
stride_w = args["stride_w"]

count = 0
stride_wa = str(stride_w)
stride_ha = str(stride_h)

## cały obraz

# size_h1 = 0
# size_h2 = X.shape[0]
# size_w1 = 0
# size_w2 = X.shape[1]

## ogranicz obraz do podziału

size_h1 = 1209
size_h2 = 2233
size_w1 = 0
size_w2 = 3583

folder_name = 'crop_img' + '_' + stride_wa + '_' + stride_ha
makedirs(folder_name, exist_ok=True)
directory = './' + folder_name + '/'
# directory = '/home/kinga/crop2/' + folder_name + '/'

for k in range (0, len(images), 1):
    for i in range(size_w1, size_w2, interval):
        for j in range(size_h1, size_h2, interval):
            img = X[k]
            cropped_img = img[j:j + stride_h, i:i + stride_w]
            width = cropped_img.shape[1]
            heigh = cropped_img.shape[0]
            if width < stride_w or heigh < stride_h:
                pass
            else:
                count += 1
                num = str(count)
                image = images[k]
                name = str(image[-8:-5])
                cv2.imwrite(directory  + name + '_' + num + '.jpg', cropped_img)
