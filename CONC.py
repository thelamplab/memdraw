
#import packages
from psychopy import visual,event,core,gui
import pygame, time, sys, csv, math, random as r, matplotlib.pyplot as graph, numpy as np, os
from random import randint
from matplotlib.collections import LineCollection

import pygame, pygame.font, pygame.event,pygame.draw, string
from pygame.locals import *


Startup = gui.Dlg(title="EXPERIMENTER")
Startup.addField('Items:','default')
Startup.addField('Time:','default')
Startup.addField('RecogTime:','default')
Startup.addField('Version:',"2")
Startup.show()  # show dialog and wait for OK or Cancel
if Startup.OK:  # then the user pressed OK
    Starters = Startup.data
    input1, input2, input3, input4 = Starters
else:
    print('user cancelled')





Startup = gui.Dlg(title="Part 1")
Startup.addField('SONA ID:')
Startup.addField('Age:')
Startup.addField('Gender:','F')
Startup.show()  # show dialog and wait for OK or Cancel
if Startup.OK:  # then the user pressed OK
    Demographics = Startup.data
    subject, age, gender = Demographics
else:
    print('user cancelled')




#set number of each trial type, timing for fixation, size of image
if input1 == 'default':
    maxTrialTypes = 80
else:
    maxTrialTypes = int(input1)
if input2 == 'default':
    large = 10
else:
    large=int(input2)
if input3 == 'default':
    recalltime = 3
else:
    recalltime=int(input3)
dim = 300

version = "Version"+str(input4)+".csv"
V = "V"+str(input4)


#instructions
Conversion = "The experimenter will now switch the computer into tablet mode."
Instructions1 = "In this experiment, you will be asked to either draw or write out words that appear on the screen."
Instructions2 = "You will be presented with a set of prompts and words, one at a time. First, you will see a 'prompt' telling you which of the two tasks to do. This will be followed immediately by a word."
Draw = "If the prompt is 'draw' we ask that you use the stylus to draw a picture illustrating the word on the screen. If you finish your drawing early, continue adding detail until your time is up."
Write = "If the prompt is 'write' we ask that you use the stylus to clearly and carefully write out the word multiple times. In other words, just continue to rewrite the word until time runs out."
Roundup = "You will have 10 seconds to perform the task that the 'prompt' indicates. Following this, any marks you have created will be recorded by the computer and the next prompt will immediately appear on the screen."
Middle = "Please try to keep your drawings away from the very edges of the screen, as this may disrupt the functionality of the program."
Verification = "The experimenter will now verify that you understand the instructions."
Ready = "Ready?"




#load fonts, build screen, set various dimensions
pygame.font.init()
Details = pygame.font.SysFont("arial", 48)
Load = pygame.font.SysFont("arial",72)  # was 72
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill((255,255,255))
middlex = screen.get_width()/2
middley = screen.get_height()/2
centerx = (middlex)-(dim/2)
centery = (middley)-(dim/2)
small = 350
med = small * 3
maxTrials = maxTrialTypes*2
draw_on = False
last_pos = (0, 0)
black = (0,0,0)
white = (255,255,255)
pink = (255,51,153)
radius = 1


# function to connect dots while drawing
def roundline(srf, color2, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.display.update(pygame.draw.circle(srf, color2, (x, y), radius))
 
 
def switchscreen(contents, duration, font):
    screen.fill((255, 255, 255))
    pygame.display.flip()
    prompt = font.render(contents, 1, (0, 0, 0))
    screen.blit(prompt, (middlex - prompt.get_width() / 2, middley - prompt.get_height() / 2))
    pygame.display.flip()
    pygame.time.delay(duration)
    pygame.display.flip()



def Advance1():
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:                
                exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            return
	
def Advance2():
    Advance1()
    pygame.display.flip()
    

def AdvanceSpace():
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                exit()
            if e.key == pygame.K_SPACE:
                return


def Advance3():
    AdvanceSpace()
    pygame.display.flip()

def drawText(surface, text, color, rect, font, aa=False, bkg=None): # This function is used to create wrapped text
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        if y + fontHeight > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1     
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        text = text[i:]
    return text

def InstructionScreen(text):
    drawText(screen,text,black,(100,200,screen.get_width()-200,screen.get_height()-200),font=Details,aa=False,bkg=None)
    pygame.display.flip()
    Advance1()
    Advance2()
    screen.fill((255,255,255))
    pygame.display.flip()
    
def InstructionPic(instructimage, scale):
    picture = pygame.image.load(instructimage)
    picture = pygame.transform.scale(picture, scale)
    screen.blit(picture, (0,0))
    pygame.display.flip()
    pygame.time.delay(3000)
    screen.fill(white)
    pygame.display.flip()
    
def InstructionSpace(text):
    drawText(screen,text,black,(100,200,screen.get_width()-200,screen.get_height()-200),font=Details,aa=False,bkg=None)
    pygame.display.flip()
    AdvanceSpace()
    Advance3()
    screen.fill((255,255,255))
    pygame.display.flip()


#read in words and images
with open(version, 'rb') as WordList:
    read = csv.reader(WordList)
    
    data = []
    for row in read:
        data.append(row)



#build lists
itemnumber=[]
instruct=[]
word=[]
trialtype=[]

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


InstructionScreen(Conversion)
InstructionScreen(Instructions1)
InstructionScreen(Instructions2)
InstructionScreen(Draw)
InstructionScreen(Write)
InstructionScreen(Roundup)
#InstructionScreen(Middle)
InstructionScreen(Verification)
InstructionScreen(Ready)
pygame.time.delay(3000)


f = open ( "./"+str(subject)+" - DrawingData.csv", "a+")
f.write("Item Number, TrialType, Word, Xpos, Ypos, Time, Mouse\n")




#randomize
x = [1,2]*40
r.shuffle(x)
xx = [1,2]*40
r.shuffle(xx)
x.extend(xx)
x2 = [3]*160
x.extend(x2)


y = range(1,81)
r.shuffle(y)
yy= range(81,161)
r.shuffle(yy)
y.extend(yy)
y2 = range(161,321)
r.shuffle(y2)
y.extend(y2)
zipped = zip(x,y)








#each trial
for i,j in zipped[:maxTrials]:
    #print(zipped)
    #print(zipped[:maxTrials])
    # comment back in if using stylus
    draw_on = False
    #pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    itemnumber.append(j)
    trialnum = j
    randword = data[trialnum][0]
    if i == 1:
        cue="draw"
        instruct.append('draw')
        trialtype.append('draw')
        opacity=0
        color2=black
    elif i == 2:
        cue="write"
        instruct.append('write')
        trialtype.append('write')
        opacity=0
        color2=black

    
    switchscreen(cue,med,Load)
    switchscreen("+",small,Load)
    
    word.append(randword)
    switchscreen(randword,med,Load)
    print(cue, randword)
    

    screen.fill((255,255,255))
    switchscreen("",100,Load)
    

    start=time.time()
    elapsed = 0
    draw_on = False
    pygame.event.clear(pygame.MOUSEMOTION)
    last_pos = pygame.mouse.get_pos()
    lasttime = 0
    lastpress = 0
    while elapsed < large:
        (x,y) = pygame.mouse.get_pos()
        (q, m, k) = pygame.mouse.get_pressed()
        t = elapsed = (time.time() - start)
        if t == lasttime:
            pass
        else:
            f.write(str(j) + "," + str(cue) + "," + str(randword) + "," + str(x) + "," + str(-y) + "," + str(t) + "," + str(q) + "\n")
        e=pygame.event.poll()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:               
                exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if draw_on and t < (large-.05):
                if q == lastpress:
                    roundline(screen, color2, e.pos, last_pos,  radius)
                    pygame.display.update(pygame.draw.circle(screen, color2, e.pos, radius))
                else:
                    pygame.display.update(pygame.draw.circle(screen, color2, e.pos, radius))

            last_pos = e.pos
        lasttime = t
        lastpress = q


switchscreen('You are now finished drawing', (large*1000), Details)  
switchscreen('The next task will begin shortly.', (large*1000), Details)    


#write basic encoding data file, demographics, trial types, order and instructions
studytrials = open ( "./"+str(subject)+" - "+V+" - StudyTrials.csv", "w")
studytrials.write("Subject, Age, Gender, Item Number, TrialType, Word\n")

for i in range (0,maxTrials):
    studytrials.write(str(subject) + "," + str(age) + "," + str(gender) + "," + str(itemnumber[i]) + "," + str(instruct[i]) + "," + str(word[i]) + "\n")
studytrials.close()





Wait = "Please sit silently, and wait until the experimenter tells you to continue."
Conversion2 = "The experimenter will now switch the computer into laptop mode."
CRT = "For this next task, you will hear tones through the speakers and it will be your job to classify them as low, medium or high. You will have two seconds to classify each tone. Please respond as quickly and as accurately as you can."
Low = "The following is an example of a low tone. When you hear this tone, press 1."
Med = "The following is an example of a medium tone. When you hear this tone, press 2."
High = "The following is an example of a high tone. When you hear this tone, press 3."
Start = "If you do not have any questions, you can double-tap SPACE to start."


def playsound(sound,what):
    pygame.mixer.init()
    audio = pygame.mixer.Sound(sound)
    audio.play()
    start=time.time()
    elapsed = 0
    while elapsed < what:
        elapsed = (time.time() - start)
        e = pygame.event.poll()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                exit()
    pygame.display.flip()

screen.fill((255,255,255))

InstructionSpace(Wait)
InstructionSpace(Conversion2)
InstructionSpace(CRT)
InstructionSpace(Low)
playsound("low.wav",2)
InstructionSpace(Med)
playsound("med.wav",2)
InstructionSpace(High)
playsound("high.wav",2)
InstructionSpace(Start)
pygame.time.delay(3000)

stuff = ["low.wav","med.wav","high.wav"]*20
r.shuffle(stuff)

for tone in stuff:
    playsound(tone,2)

expTime = core.Clock()

Wait = "Please sit silently, and wait until the experimenter tells you to continue."
InstructionsTest = "In this next phase of the experiment, single words will be presented one at a time in the center of the screen. It will be your job to indicate whether you remember the word from the study phase or not, using the keyboard."
Rdescription = "We would like you to respond to the test using one of three options. A 'Remember' response means that you have a conscious recollection of specific contextual information about your initial encounter with the word, such as hearing a sound in the hall, or what you did when the word was presented"
Kdescription = "We would like you to respond to the test using one of three options. A 'Know' response means that you have only a feeling of familiarity; you believe that the word has been seen recently, but you cannot remember specific details from seeing the word"
Ndescription = "We would like you to respond to the test using one of three options. A 'New' response means that you did not encounter the word in the previous phase."
ResponseOptions1 = "If your response is 'Remember', press 1."
ResponseOptions2 = "If your response is 'Know', press 2."
ResponseOptions3 = "If your response is 'New', press 3."
Timing = "You will have three seconds to respond to each item. If you do not respond in time, you will hear a short tone. If this happens, remember to respond more quickly on the next trial."
Reiterate = "As a reminder, if you think an item is one that you saw in the study phase, you will answer either 'Remember' or 'Know', and if you DO NOT think that you saw the item in the study phase, you should respond 'New'."
Embark = "If you have any questions, please ask them now, because the experiment is about to begin."
Ready = "Ready?" 






def TestWord(contents, font):
    screen.fill((255,255,255))
    pygame.display.flip()
    prompt = font.render(contents,1,(0,0,0))
    screen.blit(prompt, (middlex - prompt.get_width() / 2, middley - prompt.get_height() / 2))
    pygame.display.flip()

def OldNew(font):
    Rresponse = font.render('Remember (1)',1, (0,0,0))
    screen.blit(Rresponse, (100, screen.get_height()-200))
    Kresponse = font.render('Know (2)',1, (0,0,0))
    screen.blit(Kresponse, ((screen.get_width()/2) - (Kresponse.get_width()/2), screen.get_height()-200))
    Nresponse = font.render('New (3)',1, (0,0,0))
    screen.blit(Nresponse, (screen.get_width() - (100 + Nresponse.get_width()), screen.get_height()-200))
    pygame.display.flip()

def CollectResp():
    expTime.reset()
    pygame.event.clear(pygame.KEYDOWN)
    now = 0
    ResponseGiven = False
    while now < recalltime:
        e = pygame.event.poll()
    now = expTime.getTime()
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
            exit()
        elif e.key == pygame.K_1:
            response.append('R')
            RT.append(expTime.getTime())
            if instruction == 'lure':
                accuracy.append(0)
            else:
                accuracy.append(1)
            ResponseGiven=True
            return
        elif e.key == pygame.K_2:
            response.append('K')
            RT.append(expTime.getTime())
            if instruction == 'lure':
                accuracy.append(0)
            else:
                accuracy.append(1)
            ResponseGiven=True
            return
        elif e.key == pygame.K_3:
            response.append('N')
            RT.append(expTime.getTime())
            if instruction == "lure":
                accuracy.append(1)
            else:
                accuracy.append(0)
            ResponseGiven=True
            return
    pygame.display.flip()
    if ResponseGiven==False:
        response.append(' - ')
        RT.append(' - ')
        accuracy.append(0)
        playsound("chirp.wav",0.1)	
	




InstructionSpace(Wait)
InstructionSpace(InstructionsTest)
InstructionSpace(Rdescription)
InstructionSpace(Kdescription)
InstructionSpace(Ndescription)
InstructionSpace(ResponseOptions1)
InstructionSpace(ResponseOptions2)
InstructionSpace(ResponseOptions3)
InstructionSpace(Timing)
InstructionSpace(Reiterate)
InstructionSpace(Embark)
InstructionSpace(Ready)
pygame.time.delay(3000)


condition=[]
word=[]
response=[]
accuracy=[]
RT=[]



r.shuffle(zipped)


for inst,stim in zipped:
    if inst == 1:
        instruction = "draw"
    elif inst == 2:
        instruction = "write"
    elif inst == 3:
        instruction = "lure"
    condition.append(instruction)
    randword = data[stim][0]    
    word.append(randword)

    TestWord("",Load)
    OldNew(Details)
    pygame.time.delay(250)
    pygame.display.flip()

    screen.fill((255,255,255))

    TestWord(randword,Load)
    OldNew(Details)
    CollectResp()
    pygame.time.delay(int((3-expTime.getTime())*1000))
   
    screen.fill((255,255,255))

TestWord('The Experiment is now complete.', Details)
pygame.time.delay(3000)
pygame.display.flip()  
TestWord('Thank you for participating.', Details)   
pygame.time.delay(3000)
pygame.display.flip() 



#write test trials
f = open ( "./"+str(subject)+"- "+V+" - TestTrials.csv", "w")
f.write("Subject, Age, Gender, Trial Type, Word, Response, Accuracy, RT\n")

for testTrial in range (0,320):
    f.write(str(subject) + "," + str(age) + "," + str(gender) + "," + str(condition[testTrial]) + "," + str(word[testTrial]) + "," + str(response[testTrial]) + "," + str(accuracy[testTrial]) + "," + str(RT[testTrial]) + "\n")
f.close()



pygame.quit()
core.quit() 
