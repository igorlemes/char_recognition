import cv2 as cv
import sys
import pytesseract
import numpy as np

def contrast(image, alpha, beta):
    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

    return new_image

img = cv.imread(sys.argv[1])
if img is None:
    print("Could not open the image")
height, width, c = img.shape
contrasted = contrast(img, 1.8, 10)
grey = cv.cvtColor(contrasted, cv.COLOR_BGR2GRAY)

char_boxes = pytesseract.image_to_boxes(grey, config="--psm 7", lang="por")

for box in char_boxes.splitlines():
    print(box)
    box = box.split()
    x, y, w, h = int(box[1]) , int(box[2]), int(box[3]), int(box[4])
    
    cv.rectangle(img, (x, height-y), (w, height-h), (0,0,255), 1)
    cv.putText(img, box[0], (x, height-y), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)

cv.imwrite(sys.argv[2], img)