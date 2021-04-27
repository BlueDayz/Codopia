import random
from graphics import *
from win32api import GetSystemMetrics

# Initalization of a Creation Object as Class with different properties

class Creature:
    def __init__(self, name, x_position, y_position, properties = 0, stomach = 0): # Stomach and properties will be added later - name is just for fun
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
        self.properties = properties
        self.stomach = stomach
        
    def CreationOfCreatur(self):
        y = int(GetSystemMetrics(0)) # Detecting the width and hight of the monitor for drawing a window
        x = int(GetSystemMetrics(1))

        win = GraphWin(self.name + "'s crazy life", y, x) # Draws the window with Creaturs name and scaling of monitor
        c = Circle(Point(self.x_position,self.y_position),30) # Circle as representation of the creature - for now
        c.draw(win)
        win.getMouse() # Waiting command for the window until a click appears
        win.close

x = Creature(input("Please enter a name for the Creature:  "),input("Please enter a X-Position for your Creature: "),input("Please enter a Y-Position for your Creature: "))
x.CreationOfCreatur()