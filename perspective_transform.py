import numpy as np
import cv2
def order_points(pts):
	
	rect = np.zeros((4, 2), dtype = "float32")
  #compute the top-left and bottom-right values
  s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
  #compute top-right and bottom-left values
  diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

  return rect
  
def four_point_transform(image, pts):

  rect = order_points(pts)
  
	(tl, tr, br, bl) = rect
  
  #to compute the width of the image
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	
  #to compute the height of the image
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	
  #destination points for the new transformed image
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

  return warped
  
import numpy as np
import argparse
import cv2

image = cv2.imread("path to the image")
pts = np.array(eval("provide the coordinates in the form of string"), dtype = "float32") #[(240,70),(110,370),(290,500),(460,180)]
warped = four_point_transform(image, pts)

cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
