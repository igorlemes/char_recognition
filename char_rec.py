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

def empty(a):
    pass

def std_deviation(contours):
    area = [cv.contourArea(cnt) for cnt in contours]
    mean = sum(area)/len(area)
    return mean, np.sqrt(sum([(i - mean)**2 for i in area])/len(area))

def get_contours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) >= 900:  
            cv.drawContours(imgContours, cnt, -1, (255,0,0), 3)
            perimeter = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*perimeter, True)
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(imgContours, (x-int(w*0.1),y-int(h*0.5)), (x+w+int(w*0.1), y+h+int(h*0.1)), (0, 0, 255), 3)

#paulo 245*2+1 e 45
# 4 4 2
# 7 5 3 #cross-elipse

#proibido 245*2+1 e 33
# 4 4 2
# 6 4 2 #cross-elipse
# 3 3 3 #rec-elipse


while True:
    cv.namedWindow("Trackbars")
    cv.resizeWindow("Trackbars", 1280, 480)
    cv.createTrackbar("Adaptive-1", "Trackbars", 245, 301, empty)
    cv.createTrackbar("Adaptive-2", "Trackbars", 25, 101, empty)

    adp_1 = cv.getTrackbarPos("Adaptive-1", "Trackbars")
    adp_2 = cv.getTrackbarPos("Adaptive-2", "Trackbars")
    # print(adp_1)

    cv.createTrackbar("Erosion", "Trackbars", 3, 10, empty)
    cv.createTrackbar("Dilation", "Trackbars", 3, 10, empty)
    cv.createTrackbar("kernel", "Trackbars", 3, 10, empty)

    ero = cv.getTrackbarPos("Erosion", "Trackbars")
    dila = cv.getTrackbarPos("Dilation", "Trackbars")
    ker = cv.getTrackbarPos("kernel", "Trackbars")
    

    # img = cv.imread("images/0004d959aab660c1ec6f4939f9c2be2e_30.png", cv.IMREAD_COLOR)
    img = cv.imread("images/ffed5601f04b75983070ea6c6dd30805_48.png", cv.IMREAD_COLOR)
    # img = cv.imread("images/Screenshot_20210525_004238.png", cv.IMREAD_COLOR)
    if img is None:
        print("Could not open the image")

    
    img = cv.resize(img,None,fx=3, fy=3, interpolation = cv.INTER_CUBIC)
    imgContours = img.copy()
    # img = contrast(img, 1.5, 10)
    img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    
    th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv.THRESH_BINARY_INV, adp_1*2+1, adp_2) 
    
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ker,ker))
    erosion = cv.erode(th3,kernel,iterations = ero)

    kernel = cv.getStructuringElement(cv.MORPH_RECT,(ker,ker))
    dilation = cv.dilate(erosion,kernel,iterations = dila)
    
  
    get_contours(erosion)
    
    cv.imshow("img", img)
    cv.imshow("imgContours", imgContours)
    cv.imshow("th3", th3)
    cv.imshow("dilation", dilation)
    cv.imshow("erosion", erosion)
    cv.waitKey(1)