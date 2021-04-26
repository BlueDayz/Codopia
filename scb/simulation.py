import random
from graphics import *


class TestWindow:
    def __init__(self, name, width, hight):
        self.name = str(name)
        self.width = int(width)
        self.hight = int(hight)
    

    def MyMakeWindow(self):
        
        win = GraphWin(self.name, self.width, self.hight) #Definition of the Window with WindowName, Width and Hight
        c = Circle(Point(self.width / 2, self.hight / 2), self.hight / 20) #Definiton of a Circle at a specific point with a specific diameter
        c.draw(win) #draw the window for the circle
        win.getMouse() #hold the window until mouseclick
        win.close #closes windows after mouseclick

x = TestWindow(input("Bitte Namen eingeben:  "),input("Bitte Weite eingeben:  "),input("Bitte Weite eingeben:  "))
x.MyMakeWindow() #Calls function for Window of new object of Class Testwindow