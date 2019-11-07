from psychopy import visual, event, core, monitors
import pandas as pd
from numpy import array 

monitor_name = "ObiMonitor"
scnWidth, scnHeight = monitors.Monitor(monitor_name).getSizePix()

mywin = visual.Window([scnWidth-10, scnHeight-10], units="pix",
                  monitor=monitor_name, fullscr=False, waitBlanking=False, allowGUI=True)

circle = visual.Circle(
    win = mywin,
    units = "pix",
    radius = 2,
    fillColor = [-1] * 3,
    lineWidth = 0
    #lineColor = [1] * 3,
    # edges = 128
) # define circle with certain radius and edge that will be drawn on screen

line = visual.Line(mywin, lineColor=[-1, -1, -1], lineWidth=5)

globalClock = core.Clock()
myMouse = event.Mouse(visible = True, win = mywin)
    
    
# function to follow mouse click of user and plots circle whenever mouse click occurs
def draw_circles(time):
    all_locations = [] # list to hold all the mouse click locations
    mouse_click_locations = [] # temporarily holds clicks while mouse is clicked
    
    while globalClock.getTime() < time:
        if myMouse.getPressed()[0]: # if user is left-clicking on mouse
            currentPos = myMouse.getPos()
            circle.pos = currentPos # get mouse position and store it to circle position
            mouse_click_locations.append(currentPos)
        
            
            if len(mouse_click_locations) > 1 and (mouse_click_locations[-2] != None).all(): 
                line.start = tuple(mouse_click_locations[-2])
                line.end = tuple(mouse_click_locations[-1]) # connect the points of the lines being drawn
                line.draw()
                
            circle.draw()
            
        else:
            all_locations.extend(mouse_click_locations) # add the mouse click locations to track all the clicks
            mouse_click_locations = [] # resets locations whenever mouse is no longer clicked
            mouse_click_locations.append(array([None, None])) # indicates mouse was not clicked during time point 
    
        mywin.flip(clearBuffer=False)
    
    return all_locations

# function to display instructions to the user
def instructions(txt):
    directions = visual.TextStim(mywin, text = txt, pos = (260, 200), color = (-1,-1,-1))
    directions.draw()
    mywin.flip()
    event.waitKeys()

# function to update window and reset globalClock if necessary 
def nextSlide(clkrst):
    mywin.update()
    if clkrst:
        globalClock.reset() # reset the global clock if input to function is true 

def createDF(locations, drawing_name): # take list of locations and create dataframe
    df_x = pd.DataFrame(pd.Series([locs[0] for locs in locations]))
    df_y = pd.DataFrame(pd.Series([locs[1] for locs in locations]))
    df_name = pd.DataFrame(pd.Series([drawing_name] * len(locations)))
    
    df = mergeDF(df_x, df_y)
    df = mergeDF(df, df_name)
    
    return df

def mergeDF(firstDF, secondDF): # merge two dataframe into one dataframe 
    return pd.concat([firstDF, secondDF], ignore_index = True, axis = 1)

if __name__ == "__main__":

    df = pd.DataFrame()
    
    instructions("Draw a cat")
    nextSlide(False)
    catLocations = draw_circles(20)
    df_cat = createDF(catLocations, "cat")
    df = mergeDF(df, df_cat)
    
    nextSlide(True)
    
    instructions("Draw a dog")
    nextSlide(False)
    dogLocations = draw_circles(20)
    df_dog = createDF(dogLocations, "dog")
    df = mergeDF(df, df_dog)
    
    df.to_excel("mouseClicks.xlsx", index = False)
    mywin.close()
    core.quit()
            