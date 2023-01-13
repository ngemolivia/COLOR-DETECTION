import argparse

#Creating argument parser to take image path from command line
parser= argparse.ArgumentParser(description='taking image path from command line')
parser.add_argument('-i', '--image', required=True, help="Path of image to be tested")
args = vars(parser.parse_args())
img_path = args['image']
 
import cv2
#Reading the image with opencv
img = cv2.imread(img_path)

#giving names to each column in the csv file
index=["color","color_name","hex","R","G","B"]

#Reading csv file with pandas
import pandas as pd
csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        distance = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(distance<=minimum):
            minimum = distance
            colorname = csv.loc[i,"color_name"]
    return colorname


#declaring global variables (to be used later)
clicked = False
r = g = b = xpos = ypos = 0


#function to get x,y coordinates of mouse when double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        
#creating a window in which the input image will display.
cv2.namedWindow('image')#image here is the name of the winow

# seting a callback function which will be called when a mouse event happens.
cv2.setMouseCallback('image',draw_function)


while(1):

    cv2.imshow("image",img)#displaying image in the window created
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (760,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(4) & 0xFF ==27:
        break 
cv2.destroyWindow("image")
