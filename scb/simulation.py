import random
import time
from graphics import *
from win32api import GetSystemMetrics

# Initalization of a Creation Object as Class with different properties

class Creatures:
    #Class statements for counting the creatures, saving them and their names and to get the window size
    creature_count = 0
    list_c = [] 
    list_names = [] 
    hight = GetSystemMetrics(1) 
    wide = GetSystemMetrics(0)

    # Initial properties of a crature
    def __init__(self, properties = 0, stomach = 0): # Stomach and properties will be added later - name is just for fun   
        self.properties = properties
        self.stomach = stomach

    # Creates a window with the detected hight and wide and a name of all cratures, alsow adds a title of all names
    def CreationOfWindow(self): 
        title = " ".join(self.list_names) 
        self.win = GraphWin(title + "'crayz life", self.wide, self.hight) 
    
    # The Function for creating a Creature, with name, color, a size and adjusted window sizes so cratures spawn not outside             
    def CreationOfCreature(self, name = "Bob"):
        self.name = name 
        self.color = ("red","green","blue","pink") # Example for color pallet -> use a real one
        self.circle_diameter = 30 
        self.adjusted_hight = self.hight - self.circle_diameter
        self.adjusted_wide = self.wide - self.circle_diameter

        self.list_names.append(self.name) 
        c = Circle(Point(random.randrange(0, self.adjusted_wide, 1),random.randrange(0, self.adjusted_hight, 1)), self.circle_diameter) # Circle as representation of the creature - for now
        c.setFill(self.color[self.creature_count]) # Different colors for the different creatures based on their creation
        self.list_c.append(c) 
        self.creature_count += 1 

    #Draw the created creatures to the crated window
    def DrawCreatures(self):
        for i in range(len(self.list_c)): # Draws all cratures from the list to the crated window
          self.list_c[i].draw(self.win)

        # Moves aroud all creatures randomly until the interruption of the consols happend
        try:
            while True:
                for i in range(len(self.list_c)):
                    self.list_c[i].move(random.randrange(-10,10,1),random.randrange(-10,10,1))
                    time.sleep(0.005)

        except KeyboardInterrupt: # Better solution for Movement stop and canceling !
            self.win.getMouse()
            self.win.close 
              
#Test Area where I crate three cratures in the variable x and crate a Window as well as drawing the cratures to it
x = Creatures()

while True:
    if(x.creature_count == 0):
        x.CreationOfCreature(input("Please choose a name for your first Creature:  "))
    if(x.creature_count > 0) and (x.creature_count <= 4):
        while True:
            z = input("Do you want to create another creature(max = 4) [y/n]")
            z = str(z)
            if (z == "y"):
                x.CreationOfCreature(input("Please choose a name for another Creature:  "))
                break
            if (z == "n"):
                x.CreationOfWindow()
                x.DrawCreatures()
                break
            print("Your answer was incorrect")
    if(x.creature_count >= 4):
        print("Sry maximal creature number is 4")
        x.CreationOfWindow()
        x.DrawCreatures()