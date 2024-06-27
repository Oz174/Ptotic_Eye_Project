from utils import *
def getbo2leela(imgPath,verbose=False):
    eyes=get_eyes(imgPath)
    if verbose:
        plt.imshow(eyes,cmap='gray')
        plt.show()
    kernel = np.ones((5,5),np.uint8)
    lowcanny=100
    highcanny=300
    iterations=1
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

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,1, 60,param1=200,param2=12,minRadius=30,maxRadius=70)
    print(circles)
    # choose circle with smallest radius
    chosenCircle= circles[0][0]
    # draw the outer circle
    img = eyes.copy()
    cv2.circle(img,(int(chosenCircle[0]),int(chosenCircle[1])),int(chosenCircle[2]),(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(int(chosenCircle[0]),int(chosenCircle[1])),2,(0,0,255),3)

    # show the image
    # plt.imshow(img,cmap='gray')
    return eyes,chosenCircle