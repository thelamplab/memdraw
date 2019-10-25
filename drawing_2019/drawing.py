from psychopy import visual, event, core, monitors
import pandas as pd

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

globalClock = core.Clock()
myMouse = event.Mouse(visible = True, win = mywin)
    
    
# function to follow mouse click of user and plots circle whenever mouse click occurs
def draw_circles(time):
    all_locations = [] # list to hold all the mouse click locations
    mouse_click_locations = []
    
    while globalClock.getTime() < time:
        if myMouse.getPressed()[0]: # if user is left clicking on mouse
            currentPos = myMouse.getPos()
            circle.pos = currentPos # get mouse position and store it to circle position
            mouse_click_locations.append(currentPos)
        
            
            if len(mouse_click_locations) > 1: 
                line = visual.Line(mywin, start = tuple(mouse_click_locations[-2]), end = tuple(mouse_click_locations[-1]), lineWidth=5) # connect the points of the lines being drawn
                line.draw()
                
            circle.draw()
            
        else:
            mouse_click_locations = [] # reset locations the locations whenever mouse is no longer clicked
    
        mywin.flip(clearBuffer=False)
    #event.waitKeys() # wait for key to be pressed
    
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
        globalClock.reset() # result the global clock if input to function is true 

if __name__ == "__main__":
    
    instructions("Draw a cat")
    nextSlide(False)
    draw_circles(10)
    nextSlide(True)
    instructions("Draw a dog")
    nextSlide(False)
    draw_circles(10)
    mywin.close()
    core.quit()
            
# refresh_rate = 60.0
# default_time = 10
# time_window = int(default_time * refresh_rate)
# 
# mouse_click_locations = [] # list to store mouse click locations
#     
# for time in range(time_window):
#     mouse_loc = myMouse.getPos()
#     mouse_click = myMouse.getPressed()
#     
#     if mouse_click: 
#         if mouse_loc == mouse_click_locations[-1]: # don't add duplicate locations
#             pass
#         else:
#             mouse_click_locations.append(mouse_loc)
#     
#     mywin.flip()
#     myMouse.clickReset()
# 
# 
# print(mouse_click_locations)


#circle.draw()
#mywin.flip()
#event.waitKeys()

# draw_circles(15)
# core.quit()
# mywin.close()