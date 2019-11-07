from psychopy import visual, event, core, monitors
import pandas as pd

monitor_name = "ObiMonitor"
scnWidth, scnHeight = monitors.Monitor(monitor_name).getSizePix()

mywin = visual.Window([scnWidth-10, scnHeight-10], units="pix",
                  monitor=monitor_name, fullscr=False, waitBlanking=False, allowGUI=True)
                  
circle = visual.Circle(
    win=mywin,
    units="pix",
    radius=2,
    fillColor=[-1, -1, -1],
    lineWidth=0)

line = visual.Line(mywin, lineColor=[-1, -1, -1], lineWidth=5)


def draw(file_name, xLoc):
    """ Takes in filename and column location of x coordinates """
    
    df = pd.read_excel(file_name)
    df = df.fillna("None")  # fill all nan values with "None" string
    length = len(df) - 1
    
    for i in range(length):  # loop through rows of points
    
        drawLine = False
        drawCircle = False
        firstPoint = tuple([df[xLoc][i], df[xLoc + 1][i]])  # xLoc + 1 = yLoc ==> column location of y coordinates
        secondPoint = tuple([df[xLoc][i + 1], df[xLoc + 1][i + 1]])
        
        if df[xLoc][i] != "None" and df[xLoc][i + 1] != "None":
            # connect the points of the lines being drawn
            line.start = firstPoint
            line.end = secondPoint
            drawLine = True
            
        if df[xLoc][i] != "None":  # need one point to draw circle (similar to drawing.py implementation)
            circle.pos = firstPoint
            drawCircle = True

        if drawCircle:
            circle.draw()
        if drawLine:
            line.draw()

        mywin.flip(clearBuffer=False)
        
    for i in range(5):
        mywin.flip(clearBuffer=True)

            
if __name__ == "__main__":
    draw("mouseClicks.xlsx", 3)
