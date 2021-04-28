import random
from graphics import *
from win32api import GetSystemMetrics

# Initalization of a Creation Object as Class with different properties

class Creatures:

    creature_count = 0 # To keep count how many creatures are created
    list_c = [] # A list for the graphical object of all creatures
    list_names = [] # A list of all names for all cratures
    hight = GetSystemMetrics(1) # Detecting the width and hight of the monitor for drawing a window
    wide = GetSystemMetrics(0)

    # Initial properties of a crature
    def __init__(self, properties = 0, stomach = 0): # Stomach and properties will be added later - name is just for fun   
        self.properties = properties
        self.stomach = stomach

    # Creates a window with the detected hight and wide and a name of all cratures
    def CreationOfWindow(self): 
        title = " ".join(self.list_names) # join together the names in the list to a string for the title
        self.win = GraphWin(title + "'crayz life", self.wide, self.hight) # Draws the window with Creaturs name and scaling of monitor
    
    # The Function for creating a Creature                   
    def CreationOfCreature(self, name = "Bob"):
        self.name = name #name for crature importatnt 
        self.color = ("red","green","blue","pink") # Example for color pallet -> use a real one
        self.circle_diameter = 30 # Diameter of grapical object
        self.adjusted_hight = self.hight - self.circle_diameter # adjusted wide and hight so the cicles do not go over the rim (due to their own diameter)
        self.adjusted_wide = self.wide - self.circle_diameter

        self.list_names.append(self.name) # Adding the creature's name to the name list
        c = Circle(Point(random.randrange(0, self.adjusted_wide,1),random.randrange(0, self.adjusted_hight,1)),self.circle_diameter) # Circle as representation of the creature - for now
        c.setFill(self.color[self.creature_count]) # Different colors for the different creatures based on their cration
        self.list_c.append(c) # Adding all grapical object to a list for drawing later
        
        self.creature_count += 1 # Add +1 to the crature count

    #Draw the created creatures to the crated window
    def DrawCreatures(self):
        for i in range(len(self.list_c)): # Draws all cratures from the list to the crated window
          self.list_c[i].draw(self.win)

        self.win.getMouse() # Waiting command for the window until a click appears
        self.win.close # closes window after mouseclick
        

#Test Area where I crate three cratures in the variable x and crate a Window as well as drawing the cratures to it
x = Creatures()

x.CreationOfCreature("Bob")
x.CreationOfCreature("Heinz")
x.CreationOfCreature("Mannfred")

x.CreationOfWindow()
x.DrawCreatures()