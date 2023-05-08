#Author: Kevin Yang
#Since: Sept 2022
#Tetris Game

#--------------------------------------
#initiation
import pygame
import sys
pygame.init()
import random
import time

#--------------------------------------
#screen setting
screen = pygame.display.set_mode((1000,800),0)

#--------------------------------------
# get screen width and height
screenWidth = screen.get_width()
screenHeight = screen.get_height()
screenCenterX = screenWidth/2
screenCenterY = screenHeight/2
screenCenter = (screenCenterX, screenCenterY)

#------------------------------------------------
#predefined colors
WHITE = (255,255,255) 
BLACK = (0,0,0) 
RED = (255,0,0) 
GREEN = (0,255,0) 	
BLUE = (0,0,255)
PURPLE = (128,0,128)
PINK = (255,192,203)
YELLOW = (255,255,0)
LIGHTSKYBLUE = (135,206,250)
AQUA = (0,255,255)
LIME = (0,255,0)
GRAY = (128,128,128)
DARKGRAY = (51,51,51)
ORANGE = (255,165,0)

#-------------------------------------------
#Fps setting
clock = pygame.time.Clock()
FPS = 120
#background
background = DARKGRAY
#------------------------------------------
#program name
pygame.display.set_caption("Tetris Game")

#-------------------------------------------
#predefined fonts
#comicsansms
comic32 = pygame.font.SysFont("comicsansms", 32)
comic72 = pygame.font.SysFont("comicsansms", 72)
comic32Bold = pygame.font.SysFont("comicsansms", 32,bold=True)
comic72Bold = pygame.font.SysFont("comicsansms", 72,bold=True)
comic32Italic = pygame.font.SysFont("comicsansms", 32,italic=True)
comic72Italic = pygame.font.SysFont("comicsansms", 72,italic=True)
comic20BI = pygame.font.SysFont("comicsansms", 20,bold=True,italic=True)
comic25BI = pygame.font.SysFont("comicsansms", 25,bold=True,italic=True)
comic30BI = pygame.font.SysFont("comicsansms", 30,bold=True,italic=True)
comic32BI = pygame.font.SysFont("comicsansms", 32,bold=True,italic=True)
comic35BI = pygame.font.SysFont("comicsansms", 35,bold=True,italic=True)
comic45BI = pygame.font.SysFont("comicsansms", 45,bold=True,italic=True)
comic72BI = pygame.font.SysFont("comicsansms", 72,bold=True,italic=True)


#inkfree
ink25 = pygame.font.SysFont("inkfree", 25)
ink32 = pygame.font.SysFont("inkfree", 32)
ink72 = pygame.font.SysFont("inkfree", 72)
ink32Bold = pygame.font.SysFont("inkfree", 32,bold=True)
ink72Bold = pygame.font.SysFont("inkfree", 72,bold=True)
ink32Italic = pygame.font.SysFont("inkfree", 32,italic=True)
ink72Italic = pygame.font.SysFont("inkfree", 72,italic=True)
ink8BI = pygame.font.SysFont("inkfree", 8,bold=True,italic=True)
ink12BI = pygame.font.SysFont("inkfree", 12,bold=True,italic=True)
ink16BI = pygame.font.SysFont("inkfree", 16,bold=True,italic=True)
ink20BI = pygame.font.SysFont("inkfree", 20,bold=True,italic=True)
ink25BI = pygame.font.SysFont("inkfree", 25,bold=True,italic=True)
ink32BI = pygame.font.SysFont("inkfree", 32,bold=True,italic=True)
ink72BI = pygame.font.SysFont("inkfree", 72,bold=True,italic=True)
#-------------------------------------------------------
#subprograms
    #textbox
def textbox(strmsg, centerx, centery, color, texttype):
    sign = texttype.render(strmsg, True, color)
    signRect = sign.get_rect()
    signRect.center = (centerx, centery)
    screen.blit(sign, signRect)
#--------------------------------------------------
    #color randomizer
def colorRandom(color, initial, duration):
    if initial < duration:
        initial +=1
    elif initial == duration:
        initial = 0
        colorR = random.randint(0,255)
        colorG = random.randint(0,255)
        colorB = random.randint(0,255)
        color = (colorR, colorG, colorB)
    return (color, initial)
#------------------------------------------------------------
def mapListDraw (mapGridList,mapingStartX, mapingStartY,blocksize):
    for row in mapGridList:
        for col in row:
            mapRect = pygame.Rect(mapingStartX, mapingStartY, blocksize,blocksize)
            pygame.draw.rect (screen, col, mapRect,0)
            mapingStartX += blocksize
        mapingStartY -= blocksize
        mapingStartX = (screenWidth - 10*blocksize)/2
#--------------------------------------------------------------
def mapListCreate (mapStartX, mapEndX,mapStartY, blocksize,mapGridRow,mapGridList):
    mapGridRow = []
    for H in range (mapStartY, 0, -blocksize):
        for W in range (mapStartX, mapEndX, blocksize):
            color = screen.get_at((W,H))
            mapGridRow.append(color)
        mapGridList.append(mapGridRow)
        mapGridRow = []
    return mapGridList
def mapListCancel (mapStartX, mapEndX,mapStartY, blocksize,mapGridCancelR,mapGridCancelList,background):
    mapGridCancelR = []
    for H in range (mapStartY, 0, -blocksize):
        for W in range (mapStartX, mapEndX, blocksize):
            color = screen.get_at((W,H))
            if color != background:
                mapGridCancelR.append("Y")
            if color == background:
                mapGridCancelR.append("N")
        mapGridCancelList.append(mapGridCancelR)
        mapGridCancelR = []
    return mapGridCancelList
#------------------------------------------------------------
def surrondingRect (blockRotationList,blocksize,blockX,blockY):
    width = 0
    height = 0
    widthR = 0
    for row in blockRotationList:
        for col in row:
            widthR += blocksize
        height+= blocksize
        if width < widthR:
            width = widthR
        widthR = 0
    borderRect = pygame.Rect(blockX, blockY, width, height)
    return borderRect
#----------------------------------------------------
def hitDetectBorder (borderRect, leftBorderRect, rightBorderRect, blockX,blocksize):
    if pygame.Rect.colliderect(borderRect,leftBorderRect):
        blockX = leftBorderRect.x + blocksize
    elif pygame.Rect.colliderect(borderRect,rightBorderRect):
        blockX = rightBorderRect.x - borderRect.width
    return blockX
#--------------------------------------------------------
def hitDetectBottom(borderRect,blockY,blockHitBelow):
    if blockY + borderRect.height >= screenHeight:
        blockY = screenHeight - borderRect.height
        blockHitBelow = True
    return (blockY, blockHitBelow)
        
#---------------------------------------------
def getCenterList (blockRotationList,color,blockX,blockY,blocksize):
    blockXC = blockX
    blockYC = blockY
    blockRect = pygame.Rect(blockX,blockY,blocksize,blocksize)
    centerList = []
    for row in blockRotationList:
        for col in row:
            if col == "Y":
                pieceRect = pygame.Rect(blockXC,blockYC,blocksize,blocksize)
                rectCenter = pieceRect.center
                centerList.append(rectCenter)
                blockXC += blocksize
            if col == "N":
                blockXC += blocksize
        blockYC += blocksize
        blockXC = blockX
    return centerList
def checkCollide (mapGridList, blockRotationList,color,blockX,blockY,blocksize,background):
    centerList = getCenterList(blockRotationList,color,blockX,blockY,blocksize)
    for i in centerList:
        
        color = screen.get_at(i)
        if color != background:
            return False
    return True
#--------------------------------------------
def chooseBlockNColor (colorList,listAll):
    blockType = int(random.randint(0,len(listAll) -1))
    colorIndex = int(random.randint(0,len(colorList) -1))
    blockList = listAll[blockType]
    blockLock = True
    color = colorList[colorIndex]
    return (blockList,color,blockLock)
#--------------------------------------------------
def drawBlock (blockList,color,blockX,blockY,blocksize,pieces):
    blockXC = blockX
    blockYC = blockY
    blockRect = pygame.Rect(blockX,blockY,blocksize,blocksize)
    for row in blockList:
        for col in row:
            if col == "Y":
                pieceRect = pygame.Rect(blockXC,blockYC,blocksize,blocksize)
                pieces.append(pieceRect)
                blockXC += blocksize
            if col == "N":
                blockXC += blocksize
        blockYC += blocksize
        blockXC = blockX
    for i in pieces:
        pygame.draw.rect(screen, color, i,0)
#---------------------------------------------------
def droppingSpeed (duration, blockY, speed,time,blocksize):
    if time < duration:
        time+=speed
    elif time >= duration:
        blockY +=blocksize
        time = 0
    return (time,blockY)
#------------------------------------------------------
def scoreCalculation (rowCancel,score):
    basemark = 200
    if rowCancel ==1:
        score += basemark
    elif rowCancel == 2:
        score += 3*basemark
    elif rowCancel == 3:
        score += 5*basemark
    elif rowCancel == 4:
        score += 10*basemark
    return score
def bubbleSort (LeaderBoardTxt):
    scores = []
    readFile = open(LeaderBoardTxt,'r')
    for line in readFile:
        line = line.rstrip("\n")
        lineElement = line.split(",")
        if line != " ":
            scores.append(lineElement)
    readFile.close()

    length = len(scores)
    tempScore = []
    for i in range (length):
        for j in range (0,length -1):
            if int(scores[j][1]) < int(scores[j+1][1]):
                tempScore = scores [j]
                scores[j] = scores [j+1]
                scores[j+1] = tempScore
                
    writeFile=open(LeaderBoardTxt, 'w')
    length = len(scores)
    for i in range(length):
        line = scores [i][0] + "," + str(scores[i][1]) + "\n"
        writeFile.write(line)
    writeFile.close()
    

#===========================================================
#loop setting
main = True
intro = True
instructions = False
game = False
scoreboard = False
storescore = False
end = False
    #========
    #game loop
blockHitBelow = False
#=====================================================
#initial variables
    #intro
introSpacingX = screenWidth/4
introSpacingY = screenHeight/5
        #welcomesign
welcomeSignColor = RED
wsColorInitial = 0
wsColorDuration = 2*FPS   #second *FPS
        #instruction sign
insSpacingY = (screenHeight - 2*introSpacingY)/5
        #game   tetris size:10x20
blocksize = int(screenHeight/20)
leftBorderRect = pygame.Rect((screenWidth - 10*blocksize)/2 - blocksize, 0, blocksize, screenHeight)
rightBorderRect = pygame.Rect(screenWidth - (screenWidth - 10*blocksize)/2, 0 ,blocksize, screenHeight)
mapingStartX = int((screenWidth - 10*blocksize)/2)
mapingStartY = int(screenHeight - blocksize)
mapingEndX = int(screenWidth - mapingStartX)

defaultRotation = 4*300
rotation = defaultRotation

time = 0
duration = 3*FPS    #s * FPS
defaultSpeed = 5
speed = defaultSpeed
smultiply = 15

blockY = 0
blockLock = False
firstTimeLock = False
blockLockNext = False
blockX = screenCenterX - blocksize

mapStartX = int(mapingStartX + blocksize/2)
mapEndX = int(mapingEndX)
mapStartY = int(screenHeight - blocksize/2)
            #lists
pieces = []
mapGridRow = []
mapGridList = []
mapGridCancelR = []
mapGridCancelList = []
popIndexList = []
piecesNext = []

#game text display
score = 0
sideCenter = (mapingStartX-blocksize)/2
gameTextSpacing = 50
endColorInitial = 0
endSignColor = RED

#scoreboard
scoreboardSpacingX = screenWidth/4
scoreboardSpacingY = screenHeight/7
page = 0
#--------------------------------------------------
#initial block and color list
IListDefault = ["YYYY"]
IListRotateCW = [
    "Y",
    "Y",
    "Y",
    "Y"]
IListAll = [IListDefault,IListRotateCW,IListDefault,IListRotateCW]
        
leftLListDefault = [
    "YNN",
    "YYY"]
leftLListRotateCW = [
    "YY",
    "YN",
    "YN"]
leftLListRotateCW2 = [
    "YYY",
    "NNY"]
leftLListRotateCW3 = [
    "NY",
    "NY",
    "YY"]
leftLListAll = [leftLListDefault,leftLListRotateCW,leftLListRotateCW2,leftLListRotateCW3]
    
rightLList = [
    "NNY",
    "YYY"]
rightLListRotateCW = [
    "YN",
    "YN",
    "YY"]
rightLListRotateCW2 = [
    "YYY",
    "YNN"]
rightLListRotateCW3 = [
    "YY",
    "NY",
    "NY"]
rightLListAll = [rightLList, rightLListRotateCW, rightLListRotateCW2, rightLListRotateCW3]

square2x2List = [
    "YY",
    "YY"]
squareListAll = [square2x2List,square2x2List,square2x2List,square2x2List]

leftZList = [
    "YYN",
    "NYY"]
leftZListRotateCW = [
    "NY",
    "YY",
    "YN"]
leftZListAll = [leftZList,leftZListRotateCW,leftZList,leftZListRotateCW]

rightZList = [
    "NYY",
    "YYN"]
rightZListRotateCW = [
    "YN",
    "YY",
    "NY"]
rightZListAll = [rightZList,rightZListRotateCW,rightZList,rightZListRotateCW]

TList = [
    "YYY",
    "NYN"]
TListRotateCW = [
    "NY",
    "YY",
    "NY"]
TListRotateCW2 = [
    "NYN",
    "YYY"]
TListRotateCW3 = [
    "YN",
    "YY",
    "YN"]
TListAll = [TList,TListRotateCW,TListRotateCW2,TListRotateCW3]

listAll = [IListAll,leftLListAll,rightLListAll,squareListAll,leftZListAll,rightZListAll,TListAll]

colorList = [RED,PURPLE,LIME,YELLOW,ORANGE,BLUE,AQUA]
#=====================================================

#============================================
#main loop
while main:
    #FPS
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False

#-------------------------------------------
    #intro
    while intro:
        #FPS
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    intro = False
                elif event.key == pygame.K_p:
                    intro = False
                    game = True
                elif event.key == pygame.K_h:
                    intro = False
                    instructions = True
                elif event.key == pygame.K_s:
                    intro = False
                    scoreboard = True
                    page = 0
        #background
        screen.fill(background)
        #welcomesign
        textbox("Welcome to the Terris Game", screenCenterX, introSpacingY, welcomeSignColor, comic45BI)
        #option play
        textbox("P. Play", screenCenterX, 4*introSpacingY, PURPLE, ink32BI)
        #option help
        textbox("H. Help", introSpacingX, 4*introSpacingY, GREEN, ink32BI)
        #option quit
        textbox("Q. Quit", 3*introSpacingX, 4*introSpacingY, YELLOW, ink32BI)
        #option scoreboard
        textbox("S. Scoreboard", screenCenterX, 3*introSpacingY, AQUA, comic35BI)
        #welcomesign color change
        (welcomeSignColor, wsColorInitial) = colorRandom (welcomeSignColor, wsColorInitial, wsColorDuration)
        #update screen
        pygame.display.flip()
#---------------------------------------------------------------
    #instructions
    while instructions:
        #FPS
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                instructions = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    instructions = False
                elif event.key == pygame.K_b:
                    instructions = False
                    intro = True
        #background
        screen.fill(background)
        #option quit
        textbox("Q. Quit", 3*introSpacingX, 4*introSpacingY, YELLOW, ink32BI)
        #option back
        textbox("B. Back", introSpacingX, 4*introSpacingY, BLUE, ink32BI)
        #instruction sign
        textbox("Instructions", screenCenterX, introSpacingY, RED, comic45BI)

        #rules
        textbox("A block will fall from the top of the screen", screenCenterX, introSpacingY + insSpacingY, GREEN, ink20BI)
        textbox("Use a/d to control left/right movement and <-/-> for rotation", screenCenterX, introSpacingY + 2*insSpacingY, GREEN, ink20BI)
        textbox("Fill row(s) with blocks to erase the blocks in the row(s) and get points", screenCenterX, introSpacingY + 3* insSpacingY, GREEN, ink20BI)
        textbox("The game ends if the block pile reached the top of the screen", screenCenterX, introSpacingY + 4*insSpacingY, GREEN, ink20BI)
        
        #update screen
        pygame.display.flip()
#----------------------------------------------------------
    while scoreboard:
        displayScore = []
        screen.fill(background)
        textbox("Username:",scoreboardSpacingX, scoreboardSpacingY, RED, ink32BI)
        textbox("Score:",scoreboardSpacingX*3, scoreboardSpacingY, RED, ink32BI)
        
        readFileS = open('LeaderBoard.txt','r')
        for line in readFileS:
            line = line.rstrip("\n")
            lineElement = line.split(",")
            if line != "":
                displayScore.append(lineElement)
        readFileS.close()
        for rank in range (page,page+5):
            (username,userscore) = displayScore[rank]
            textbox(username,scoreboardSpacingX, scoreboardSpacingY * (rank+2), RED, ink32BI)
            textbox(userscore,scoreboardSpacingX*3, scoreboardSpacingY * (rank+2), RED, ink32BI)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                scoreboard = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    scoreboard = False
                elif event.key == pygame.K_b:
                    scoreboard = False
                    intro = True
            
                
#---------------------------------------------------------
    #game
    while game:
        #FPS
        clock.tick(FPS)
        #fill background
        screen.fill(background)
        #draw borders/game area
        pygame.draw.rect(screen, PINK, leftBorderRect, 0)
        pygame.draw.rect(screen, PINK, rightBorderRect, 0)

        #when a block is being moved
        while blockHitBelow == False:
            #FPS
            clock.tick(FPS)
            #fill background
            screen.fill(background)
            #draw borders/game area
            pygame.draw.rect(screen, PINK, leftBorderRect, 0)
            pygame.draw.rect(screen, PINK, rightBorderRect, 0)
            
            #display score
            textbox("Score:", screenWidth-sideCenter, gameTextSpacing, PINK, ink32BI)
            textbox(str(score), screenWidth-sideCenter, 2*gameTextSpacing ,PINK,ink32BI)
            #display welcome
            textbox("Terris Time", sideCenter, gameTextSpacing, LIGHTSKYBLUE, ink32BI)
            
            #generate block and color            
            if blockLockNext == False:
                if firstTimeLock == False:
                    (blockList,color,blockLock) = chooseBlockNColor (colorList,listAll)
                (blockListNext,colorNext,blockLockNext) = chooseBlockNColor (colorList,listAll)
                
            blockRotationList = blockList[rotation%4]
            blockRotationListNext = blockListNext[defaultRotation%4]
            borderRect = surrondingRect(blockRotationList,blocksize,blockX,blockY)
            
            #check if hit left/right border
            blockX = hitDetectBorder(borderRect, leftBorderRect, rightBorderRect, blockX,blocksize)
            #check if hit bottom
            (blockY,blockHitBelow) = hitDetectBottom(borderRect,blockY,blockHitBelow)
            #draw existing blocks
            mapListDraw (mapGridList,mapingStartX, mapingStartY,blocksize)

            #user control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    main = False
                    blockHitBelow = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game = False
                        main = False
                        blockHitBelow = True
                    if event.key == pygame.K_a:
                        blockX -= blocksize
                        if leftBorderRect.x + blocksize > blockX:
                            blockX += blocksize
                        elif checkCollide (mapGridList, blockRotationList,color,blockX,blockY,blocksize,background) == False:
                            blockX += blocksize
                            
                    if event.key == pygame.K_d:
                        blockX += blocksize
                        if rightBorderRect.x - borderRect.width < blockX:
                            blockX -= blocksize
                        elif checkCollide (mapGridList, blockRotationList,color,blockX,blockY,blocksize,background) == False:
                            blockX -= blocksize
                                            
                    if event.key == pygame.K_LEFT:
                        rotation -=1
                        if checkCollide (mapGridList, blockRotationList,color,blockX,blockY,blocksize,background) == False:
                            rotation +=1
                    if event.key == pygame.K_RIGHT:
                        rotation +=1
                        if checkCollide (mapGridList, blockRotationList,color,blockX,blockY,blocksize,background) == False:
                            rotation -=1
                            
                    if event.key == pygame.K_s:
                        speed = smultiply*speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        speed = speed/smultiply
                        
            #calculate drop
            blockYNext = blockY + blocksize
            if blockYNext > screenHeight - borderRect.height:
                blockHitBelow = True
            elif checkCollide (mapGridList, blockRotationList,color,blockX,blockYNext,blocksize,background) == True:
                (time,blockY) = droppingSpeed(duration, blockY, speed ,time,blocksize)
            else:
                blockHitBelow = True
                
            #draw block
            drawBlock(blockRotationList,color,blockX,blockY,blocksize,pieces)
            pieces = []
            #draw next block
            drawBlock(blockRotationListNext,colorNext,mapingEndX+2*blocksize,screenHeight - 2*gameTextSpacing,blocksize,piecesNext)
            piecesNext = []
            #draw lines
            for i in range (0,screenHeight,int(blocksize)):
                pygame.draw.line(screen, WHITE, ((screenWidth-10*blocksize)/2, i), (screenWidth - (screenWidth-10*blocksize)/2 , i),1)
            for i in range (mapingStartX, mapingEndX , int(blocksize)):
                pygame.draw.line(screen,WHITE, (i, 0), (i, screenHeight),1)
            #update screen
            pygame.display.flip()

            
        #when a block hit the bottom/cant be moved:
        if blockHitBelow:
            rowCancel = 0
            #for redrawing blocks
            mapGridList = []
            mapGridRow = []
            mapGridList = mapListCreate (mapStartX, mapEndX,mapStartY, blocksize,mapGridRow,mapGridList)
            mapGridListChanged = mapGridList.copy()
            #for cancel detection
            mapGridCancelList = []
            mapGridCancelR = []
            mapGridCancelList = mapListCancel (mapStartX, mapEndX,mapStartY, blocksize,mapGridCancelR,mapGridCancelList,background)
                #if cancel occur
            for rowIndex in range(len(mapGridCancelList)):
                if mapGridCancelList[rowIndex] == ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"]:
                    popIndexList.append(rowIndex)
                    rowCancel += 1

            if popIndexList != []:
                for i in popIndexList:
                    mapGridCancelList.remove(["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"])
                    mapGridCancelList.append(["N","N","N","N","N","N","N","N","N","N"])
                    
                    tempMapColor = mapGridList[i]
                    mapGridListChanged.remove(tempMapColor)
                    mapGridListChanged.append([background,background,background,background,background,background,background,background,background,background])
                mapGridList = mapGridListChanged.copy()

            score = scoreCalculation (rowCancel,score)
            

            
            
            #writeFile = open('B.txt','w')
            #for line in mapGridCancelList:                 #later use maybe...
                #writeFile.write(str(line)+ "\n")
            #writeFile.close()

            #if hit top of the screen:
            screenTopList = mapGridCancelList[19]
            for col in screenTopList:
                if col == "Y":
                    game = False
                    end = True
            #variable resets for next block
            blockHitBelow = False
            rotation = defaultRotation
            blockY = 0
            blockLockNext = False
            blockX = screenCenterX - blocksize
            time = 0
            firstTimeLock = True
            popIndexList = []
            #make the previewed next
            blockList = blockListNext
            color = colorNext
            blockLock = blockLockNext
            speed += (score/20000)
        
    #game over
    while end:
        #FPS
        clock.tick(FPS)
        #background
        screen.fill(background)
        #display score
        textbox("Congratulation! Your score is:", screenCenterX, screenHeight/5, endSignColor, comic45BI)
        textbox(str(score), screenCenterX, 2*screenHeight/5, endSignColor, comic45BI)
        textbox("Would you like other people admire your amazing skill? Hit S",screenCenterX,3*screenHeight/5,RED,comic25BI)
        textbox("Q. Quit", 3*introSpacingX, 4*screenHeight/5, YELLOW, ink32BI)
        textbox("S. Store Score", 2*introSpacingX, 4*screenHeight/5, BLUE, ink32BI)
        textbox("M. Menu", introSpacingX, 4*screenHeight/5,GREEN,ink32BI)
        #welcomesign color change
        (endSignColor, endColorInitial) = colorRandom (endSignColor, endColorInitial, wsColorDuration)

        #user Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                end = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    end = False
                elif event.key == pygame.K_m:
                    intro = True
                    end = False
                    score = 0
                    blockHitBelow = False
                    rotation = defaultRotation
                    blockY = 0
                    blockLock = False
                    blockX = screenCenterX - blocksize
                    time = 0
                    pieces = []
                    mapGridRow = []
                    mapGridList = []
                    mapGridCancelR = []
                    mapGridCancelList = []
                    firstTimeLock = False
                    blockLockNext = False
                    speed = defaultSpeed
                    
                elif event.key == pygame.K_s:
                    storescore = True
                    end = False
        
        pygame.display.flip()
    while storescore:
        while True:
            screen.fill(background)
            textbox("Please Enter The Name You Want To Be Remembered As In The Initiation Window", screenCenterX, screenCenterY, RED, comic20BI)
            pygame.display.update
            scoreListAll = []

            username = input("Please Enter The Name Here")
            if username != "":
                break
        screen.fill(background)
        textbox("Thank You For Playing This Game You Will Be Returned To The Menu", screenCenterX, screenCenterY, RED, comic20BI)
        timer = 3*FPS
        pygame.display.update()
        while True:
            clock.tick(FPS)
            timer -=1
            if timer == 0:
                break
            
        #store information
        writeFileA = open('LeaderBoard.txt','a')
        writeFileA.write(str(username) + "," + str(score) + "\n")
        writeFileA.close()
        bubbleSort('LeaderBoard.txt')
                
        storescore = False
        intro = True
        
        score = 0
        blockHitBelow = False
        rotation = defaultRotation
        blockY = 0
        blockLock = False
        blockX = screenCenterX - blocksize
        time = 0
        pieces = []
        mapGridRow = []
        mapGridList = []
        mapGridCancelR = []
        mapGridCancelList = []
        firstTimeLock = False
        blockLockNext = False
        speed = defaultSpeed
            
    


            
#quit
pygame.quit()
sys.exit()
        

