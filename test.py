from utils import *
import cv2


img = cv2.imread('will.jpeg')
str_img = mat_to_str(img)
print(str_img[0:10])
print(str_img.decode()[0:10])

img2 = str_to_mat(str(str_img))

cv2.imshow('output', img2)
cv2.waitKey(0)