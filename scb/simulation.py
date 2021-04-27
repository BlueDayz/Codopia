import random
from graphics import *
from win32api import GetSystemMetrics

# Initalization of a Creation Object as Class with different properties

class Creature:
    def __init__(self, name, properties = 0, stomach = 0): # Stomach and properties will be added later - name is just for fun   
        self.name = name  
        self.properties = properties
        self.stomach = stomach

        self.MakeWindow()
        self.CreationOfCreatur(self.name)

    def MakeWindow(self):
        self.hight = GetSystemMetrics(1) # Detecting the width and hight of the monitor for drawing a window
        self.wide = GetSystemMetrics(0)
        self.window = (self.wide, self.hight)
        return self.window
                
    def CreationOfCreatur(self, name):
        self.name = str(name)
        self.win = GraphWin(self.name + "'s crazy life", self.MakeWindow()[0], self.MakeWindow()[1]) # Draws the window with Creaturs name and scaling of monitor
        c = Circle(Point(random.randrange(0, self.MakeWindow()[0],1),random.randrange(0, self.MakeWindow()[1],1)),30) # Circle as representation of the creature - for now
        c.setFill("red")
        c.draw(self.win)
        self.win.getMouse() # Waiting command for the window until a click appears
        self.win.close

x = Creature("Bob")