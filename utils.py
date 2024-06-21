import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize

# gets eye from the image (one eye given)
def get_eyes(path):
    image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))   
    eyes = sorted(eyes,key=lambda x: x[0])
    if len(eyes) == 2:
        # if two eyes are in the image like sample_1 , it will take a rectangular strip having two eyes
        whole_eyes = [min(eyes[0][0],eyes[1][0]),eyes[1][0]+eyes[1][2],eyes[0][1],eyes[1][1]+eyes[1][3]]
    else:
        # else if one eye is in the image like sample_2 , it will take the eye only
        for x,y,w,h in eyes:
            whole_eyes = [x,x+w,y,y+h]
    image = image[whole_eyes[2]:whole_eyes[3], whole_eyes[0]:whole_eyes[1]]
    return image

# circular kernel 
def make_circular_kernel(shape,radius):
    if radius >= max(shape[0],shape[1]):
        return
    if shape[0] != shape[1]:
        return 
    ckernel = np.zeros(shape,dtype=np.uint8)
    center = (shape[0]//2,shape[1]//2)
    for i in range(center[0]-radius,center[0]+radius+1):
        for j in range(center[1]-radius,center[1]+radius+1):
            if (center[0] - i)**2 + (center[1] - j)**2 <= radius**2:
                ckernel[i][j] = 1
    return ckernel

# for pupil detection given one eye image
def get_center(eyes,lowcanny=450, highcanny=500,dp=1,iterations=1,verbose=False):
    kernel = make_circular_kernel((13,13),6)
   
    edges = cv2.Canny(eyes,lowcanny,highcanny)

    if verbose:
        print("Canny edges")
        plt.imshow(edges,cmap='gray')
        plt.axis('off')
        plt.show()
    
    edges = cv2.dilate(edges,kernel,iterations=iterations) 

    if verbose:
        print("Dilated edges")
        plt.imshow(edges,cmap='gray')
        plt.axis('off')
        plt.show()

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp, 60,param1=200,param2=12,minRadius=4)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        min_arr = []
        for x,y,_ in circles:
        # make filter and use to check if the surrounding is black 
            window = eyes[y-10:y+10,x-10:x+10]
            min_arr.append(np.mean(window))

    # get the pupil with the darkest surrounding
    pupil = circles[np.argmin(min_arr)]
    if verbose:
        cv2.drawMarker(eyes,(pupil[0],pupil[1]),color=(100,255,100),markerType=cv2.MARKER_TILTED_CROSS,thickness=2)
        plt.imshow(eyes,cmap='gray')
        plt.axis('off')
        plt.show()
    return pupil[0] , pupil[1]


def getEylidContour(path, verbose):
    extracted_eyes = get_eyes(path)
    cx,cy = get_center(extracted_eyes)
    edges = cv2.Canny(extracted_eyes,450,600)
    max_y = edges.shape[0]
    kernel = make_circular_kernel((3,3),1)
    edges = cv2.dilate(edges,kernel,iterations=1) 
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # get the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(extracted_eyes)
    cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), -1)
    skeleton = skeletonize(mask)
    skeleton=skeleton.astype(np.uint8)
    contours, _ = cv2.findContours(skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(extracted_eyes)
    cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), -1)
    # if verbose:
    #     plt.imshow(mask,cmap='gray')
    #     plt.plot(cx,cy,'ro')
    #     plt.axis('off')
    #     plt.show()
    # apply cubic spline on the largest contour 
    x = largest_contour[:,0,0]
    y = largest_contour[:,0,1]
    points = np.array([x,y]).T
    # modify the y to be max_y - y
    points[:,1] = max_y - points[:,1]
    if verbose:
        plt.scatter(cx,max_y-cy,color='red')
        plt.plot(points[:,0],points[:,1],color='green')
        # show the image from 0 to max_y
        plt.ylim(0,max_y)
        plt.xlim(0,points[:,0].max())
        plt.show()
    return points