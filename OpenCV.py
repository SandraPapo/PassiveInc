import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.modules[__name__].__dict__.clear()
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui

import os
print os.getcwd()
script_dir = os.getcwd() #<-- absolute dir the script is in

imgbuttons = {
'actionBar':script_dir + '/pics/buttons/actionbar.png',
'fold': script_dir + '/pics/buttons/fold.png',
'check':script_dir + '/pics/buttons/check.png',
'max': script_dir + '/pics/buttons/max.png',
'bet':script_dir + '/pics/buttons/bet.png',
'call':script_dir + '/pics/buttons/call.png', 
'imBack':script_dir + '/pics/buttons/imBack.png', 
'cardsDealt':script_dir + '/pics/buttons/cardsDelt.png', 
'raiseTo': script_dir + '/pics/buttons/raiseTo.png'
}

#to make quicker we can reduce the quality of the image and/or
#all that matters is that the images are the same resolution
#sourceImg: path of the image being searched, templateImg: path of the template Image, threashold: 0->1, drawBox: put 1 if you want to draw a box
def findImg(sourceImg, templateImg, threshold, drawBox):
    img_rgb = sourceImg
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templateImg, 0)
    w, h = template.shape[::-1]
    match_result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    location_of_results = np.where( match_result >= threshold)
    #print(location_of_results)
    #print(len(location_of_results[0]))
    if drawBox == 1:
        img_rgb = sourceImg
        for pt in zip(*location_of_results[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.imwrite('result.png',img_rgb)
    return location_of_results

def screenCapture():
    img = ImageGrab.grab()
    img_np = np.array(img) #puts it in numpy format
    return img_np



def getImportantRanks(currentScreen):    
    imgRanks = {
    script_dir + '/pics/cards/ten.png':'ten',
    script_dir + '/pics/cards/jack.png':'jack',
    script_dir + '/pics/cards/queen.png':'queen',
    script_dir + '/pics/cards/king.png': 'king',
    script_dir + '/pics/cards/ace.png':'ace'
    }
    sensitivities = [0.95,0.95,0.95,0.95,0.95]
    i = 0
    ranks = []
    for key in imgRanks:
    	#print(key)
        locMatches = findImg(currentScreen, key, sensitivities[i], 0) #play with sensitivities
        numMatches = len(locMatches[0])
        if len(ranks) > 1 :
            return ranks
        elif numMatches == 1 :
            ranks.append(imgRanks[key])
        elif numMatches == 2 :
            ranks.append(imgRanks[key]) 
            ranks.append(imgRanks[key])
        i += 1
    return ranks

def getSuits(currentScreen):
    imgSuits = {
    script_dir + '/pics/cards/hearts.png': 'hearts',
    script_dir + '/pics/cards/diamonds.png': 'diamonds',
    script_dir + '/pics/cards/spades.png':'spades', 
    script_dir + '/pics/cards/clubs.png':'clubs'
    }
    sensitivities = [0.96,0.95,0.95,0.95]
    i = 0
    suits = []
    for key in imgSuits:
    	#print(key)
        locMatches = findImg(currentScreen, key, sensitivities[i], 0)
        numMatches = len(locMatches[0])
        if len(suits) > 1:
            return suits
        elif numMatches == 1 :
            suits.append(imgSuits[key])
        elif numMatches == 2 :
            suits.append(imgSuits[key])
            suits.append(imgSuits[key])
        i += 1
    return suits

def exists(image, currentScreen, sensitivity):
    locMatches = findImg(currentScreen, image, sensitivity, 0)
    numMatches = len(locMatches[0])
    if numMatches == 0:
        return 0
    else:
        return 1

def waitfor(image,sensitivity):
    while 1:
        currentScreen = screenCapture()
        locMatches = findImg(currentScreen, image, sensitivity, 0)
        numMatches = len(locMatches[0])
        if numMatches != 0:
            break


def getPlay(currentScreen): 
    currentScreen = screenCapture() 
    ranks = []
    ranks = getImportantRanks(currentScreen)
    print(ranks)
    #print(ranks)
    if len(ranks) < 2:
        return 'fold'
    if ranks[0] == ranks[1]:
        return 'allIn'
    if 'ace' in ranks and 'king' in ranks:
        return 'allIn'
    #get suits only if nessisary to save time
    suits = []
    suits = getSuits(currentScreen)
    #print(suits)
    print(suits)
    if 'ace' in ranks and 'queen' in ranks and suits[0] == suits[1]:
        return 'allIn'
    if 'ace' in ranks and 'jack' in ranks and suits[0] == suits[1]:
        return 'allIn'
    if 'king' in ranks and 'queen' in ranks and suits[0] == suits[1]:
        return 'allIn'
    return 'fold'

def clickOn(width, height):
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True
    pyautogui.moveTo(width, height, duration=0.5)
    pyautogui.click(width, height)


def fold():
    if exists(imgbuttons['fold'],currentScreen, 0.80):
        location = findImg(currentScreen,imgbuttons['fold'], 0.80, 0)
        width = int(location[0][0]*(1280.0/2560.0)) + 10#2560
        height = int(location[1][0]*(800.0/1600.0)) + 10#1600
        clickOn(height, width)
    elif exists(imgbuttons['check'],currentScreen, 0.80):
        location = findImg(currentScreen,imgbuttons['check'], 0.80, 0)
        width = int(location[0][0]*(1280.0/2560.0)) + 10#2560
        height = int(location[1][0]*(800.0/1600.0)) + 10#1600
        clickOn(height, width)

def allIn():
    if exists(imgbuttons['max'],currentScreen, 0.80):
        location = findImg(currentScreen,imgbuttons['max'], 0.80, 0)
        width = int(location[0][0]*(1280.0/2560.0)) + 10#2560
        height = int(location[1][0]*(800.0/1600.0)) + 10#1600
        clickOn(height, width)
        if exists(imgbuttons['raiseTo'],currentScreen, 0.75): 
            location2 = findImg(currentScreen,imgbuttons['raiseTo'], 0.75, 0)
            width2 = int(location2[0][0]*(1280.0/2560.0)) + 10#2560
            height2 = int(location2[1][0]*(800.0/1600.0)) + 10#1600
            clickOn(height2, width2)
    elif exists(imgbuttons['call'],currentScreen, 0.80):
        location = findImg(currentScreen,imgbuttons['call'], 0.80, 0)
        width = int(location[0][0]*(1280.0/2560.0)) + 10#2560
        height = int(location[1][0]*(800.0/1600.0)) + 10#1600
        clickOn(height, width)

'''
def filter(location_of_results):
	location_of_results[0][0]
	for i in xrange(0,len(locMatches[0])):
	    if abs(location_of_results[i][0] - location_of_results[i + 1][0])  15 and abs(location_of_results[0][i] - location_of_results[0][i + 1] > 15:
'''



#for i in range(0,1):
while 1:
    currentScreen = screenCapture()
    waitfor(imgbuttons['actionBar'], 0.70)
    play = getPlay(currentScreen)
    print(play)
    if play == 'fold':
         fold()
    elif play == 'allIn':
         allIn()
'''
print(getImportantRanks(currentScreen))
print(getSuits(currentScreen))
'''
'''
    if exists(imgbuttons['imBack'],currentScreen, 0.80):
		location = findImg(currentScreen,imgbuttons['imBack'], 0.80, 0)
		width = int(location[0][0]*(1280.0/2560.0)) + 10#2560
		height = int(location[1][0]*(800.0/1600.0)) + 10#160
		clickOn(height, width)
    	continue
'''
		#allin






'''
random shit
print(len(findImg(screenCapture(), template, 0.965, 1)))
findImg(screenCapture(), script_dir + '/cards/ten.png', 0.965, 1)
findImg(screenCapture(), script_dir + '/cards/jack.png', 0.8, 1)
imgSuits = {script_dir + '/cards/heart.png': 'hearts',script_dir + '/cards/diamonds.png': 'diamonds',script_dir + '/cards/spades.png':'spades',script_dir + '/cards/clubs.png':'clubs'}
'''


