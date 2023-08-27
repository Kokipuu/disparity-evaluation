import cv2
import numpy as np
from shapely.geometry import Point
import shapely
from shapely.geometry import Polygon
import random
import matplotlib
import math


# Parameters
# ImgSize: (W, H) pixel size of the image
# radiusRange: (min radius, max radius) radius range of the circles
# color & color2: hex code for the colour of the circles, must start with # not 0x
# backgroundClr: hex code for the background colour of the image, must start with # not 0x
# extraCircles: number of extra circles to be drawn in the image on top of default
# outfilePath: the path which the ong image would be stored
# cm_to_pixel: for scaling, default is 100 px/cm
# version: Default is 1, which allows overlapping, version 2 doesn't allow overlapping
# draw.drawCirlce((2970, 4200), (5, 10), "#ffffff", "#000000", "test_v3.png", cm_to_pixel=100, extraCircles=40000, version = 1, backgroundClr="#888888") //used to generate the images used for testing


def drawCirlce(imgSize:tuple, radiusRange:tuple, color1:str, color2:str, outputFilePath:str, backgroundClr:str = "#FFFFFF", cm_to_pixel:int = 100, extraCircles:int = 0, version:int = 1):
    # Parameters
    backgroundClr = tuple([int(x*255) for x in matplotlib.colors.to_rgb(backgroundClr)])
    color1 = tuple([int(x*255) for x in matplotlib.colors.to_rgb(color1)])
    color2 = tuple([int(x*255) for x in matplotlib.colors.to_rgb(color2)])

    min_r_pix = int(radiusRange[0] * cm_to_pix)
    max_r_pix = int(radiusRange[1] * cm_to_pix)
    r_range = (min_r_pix, max_r_pix)

    if version == 1:
       circleList = generateCircleCords(imgSize, r_range, extraCircles, cm_to_pixel) 
    elif version == 2:
        circleList = generateRandomCircleCords(imgSize, r_range, extraCircles, cm_to_pixel)
    
    color1Count = 0
    color2Count = 0

    # drawing image and cirlce 
    img = np.zeros((imgSize[1], imgSize[0], 3), np.uint8)
    img[:, :] = backgroundClr
    rand = 0
    for i in range(0, len(circleList)):
        if color1Count < int(len(circleList)/2) and color2Count < int(len(circleList)/2):
            #rand = random.randrange(2)
            if rand % 2 == 0:
                circleColor = color1
            else:
                circleColor = color2
            rand += 1
        elif color1Count >= int(len(circleList)/2):
            circleColor = color2
        else:
            circleColor = color1
        cv2.circle(img, (circleList[i][0], circleList[i][1]), circleList[i][2], circleColor, -1)
    cv2.imwrite(outputFilePath, img)
    nWhitePixels = np.sum(img==backgroundClr)
    print(nWhitePixels/(3*imgSize[0]*imgSize[1]))

def generateRandomCircleCords(imgSize:tuple, radiusRange:tuple, totalCircles:int, cm_to_pixel:int):
    TRYS = 1000
    circles = []
    nCircles = 0
    maxR = radiusRange[1]
    buffer = cm_to_pixel

    while nCircles < totalCircles:
        circleAdded = False
        for i in range(0, TRYS):
            found = True
            x = random.randrange(0, imgSize[0])
            y = random.randrange(0, imgSize[1])   
            r = random.randrange(radiusRange[0], maxR)    
            newCircle = Point(x, y).buffer(r)
            for circle in circles:
                if shapely.intersects(Point(circle[0], circle[1]).buffer(circle[2]+buffer), newCircle):
                    found = False
                    break
            if found:
                circles.append((x, y, r))
                nCircles += 1
                circleAdded = True
                break
        if not circleAdded:
            maxR =- 1
            buffer = 0
        if maxR <= radiusRange[0]:
            print(str(nCircles) + " circles were drawn")
            break

    circles.sort(key = lambda x: x[2], reverse=True)
    return circles

def generateCircleCords(imgSize:tuple, radiusRange:tuple, extraCircles:int, cm_to_pixel:int):
    circles = []
    # length of square such that the the furtherest distance between diagonal squares are less than 3cm 
    squareLength = int(math.sqrt((1/8)*(4*radiusRange[0]*radiusRange[0]+12*cm_to_pixel*radiusRange[0]+9*cm_to_pixel*cm_to_pixel)))
    nSquare = int(imgSize[0]/squareLength)

    nExtraCircles = 0
    currY = 0

    # Generating circles in each square grid such that there are no empty spaces greater than 3x3 cm2
    while currY < imgSize[1]:
        for i in range(0, nSquare + 1):
            x = random.randrange(i*squareLength, (i+1)*squareLength)
            y = random.randrange(currY, currY + squareLength)
            r = random.randrange(radiusRange[0], radiusRange[1])
            circles.append((x, y, r))
        currY += squareLength
    
    # Generating rest of the Circles if number of Circles required are greater
    while nExtraCircles < extraCircles:
        x = random.randrange(0, imgSize[0])
        y = random.randrange(0, imgSize[1])
        r = random.randrange(radiusRange[0], radiusRange[1])
        circles.append((x, y, r))
        nExtraCircles += 1
    circles.sort(key = lambda x: x[2], reverse=True)
    return circles


if __name__ == "__main__":
    SEED = 10
    #size_of_paper = (21, 29)   # for A4 (actual A4 size 21.0 x 29.7 cm) 
    size_of_paper = (29, 42)   # for A3 (actual A3 size 29.7 x 42.0 cm)
    rad_range = (0.15, 0.5)    # cm
    circles_per_10x10cm = 500
    color1 = "#888888"
    color2 = "#888888"
    # bgcolor = "#888888"
    bgcolor = "#000000"
    version = 1
    outfilePath = "pattern02/floorpattern-gray-black1.png"
    cm_to_pix = 100            # 1cm = X pixels

    np.random.seed(SEED)
    paper_area = size_of_paper[0] * size_of_paper[1]
    extraCircles = int(circles_per_10x10cm * paper_area / 100)
    img_size = (size_of_paper[0] * cm_to_pix, size_of_paper[1] * cm_to_pix)

    drawCirlce(img_size, rad_range, color1, color2, outfilePath, bgcolor, cm_to_pix, extraCircles, version)



