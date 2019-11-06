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
    fillColor = [1] * 3,
    #lineColor = [1] * 3,
    # edges = 128
) # define circle with certain radius and edge that will be drawn on screen


def draw(file_name, xLoc):
    """ Takes in filename and column location of x coordinates """
    
    df = pd.read_excel(file_name)
    df = df.fillna("None") # fill all nan values with "None" string
    length = len(df) - 1
    
    for i in range(length): # loop through rows of points 
        
        firstPoint = array([df[xLoc][i], df[xLoc + 1][i]]) # xLoc + 1 = yLoc ==> column location of y coordinates 
        secondPoint = array([df[xLoc][i + 1], df[xLoc + 1][i + 1]])
        
        if df[xLoc][i] != "None" and df[xLoc][i + 1] != "None":
            line = visual.Line(mywin, start = tuple(firstPoint), end = tuple(secondPoint), lineWidth=5) # connect the points of the lines being drawn
            line.draw()
            
        elif df[xLoc][i] != "None": # need one point to draw circle (similar to drawing.py implementation)
            circle.pos = firstPoint
            circle.draw()
                 
            
if __name__ == "__main__":
    draw("mouseClicks.xlsx", 0)
        
        