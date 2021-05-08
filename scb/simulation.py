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
    list_positions_of_creatures = []
    hight = GetSystemMetrics(1) 
    wide = GetSystemMetrics(0)
    my_color = ("red","yellow","blue","green","purple")

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
        self.circle_diameter = 30 
        self.adjusted_hight = self.hight - self.circle_diameter
        self.adjusted_wide = self.wide - self.circle_diameter

        self.list_names.append(self.name) 
        self.position_creature = (random.randrange(0, self.adjusted_wide, 1),random.randrange(0, self.adjusted_hight, 1))
        self.list_positions_of_creatures.append(self.position_creature)
        c = Circle(Point(self.position_creature[0],self.position_creature[1]), self.circle_diameter) # Circle as representation of the creature - for now
        c.setFill(self.my_color[self.creature_count]) # Different colors for the different creatures based on their creation
        self.list_c.append(c) 
        self.creature_count += 1 

    #Draw the created creatures to the crated window
    def DrawCreatures(self):
        for i in range(len(self.list_c)): # Draws all cratures from the list to the crated window
          self.list_c[i].draw(self.win)

        # Moves aroud all creatures randomly (until hitting the border) until the interruption of the consols happend 
        try:
            while (True):
                for i in range(len(self.list_c)): # all creatures of the list
                    if (self.list_positions_of_creatures[i][0] >= self.wide - 40) or (self.list_positions_of_creatures[i][1] >= self.hight - 40): # better way for border detection !!
                        self.list_c[i].move(random.randrange(-10,0,1),random.randrange(-10,0,1))
                        time.sleep(0.01)

                    elif(self.list_positions_of_creatures[i][0] <= 0 + 40) or (self.list_positions_of_creatures[i][1] <= 0 + 40):
                        self.list_c[i].move(random.randrange(0,10,1),random.randrange(0,10,1))
                        time.sleep(0.01)

                    else:
                        self.list_c[i].move(random.randrange(-10,10,1),random.randrange(-10,10,1))
                        time.sleep(0.01)

        except KeyboardInterrupt: # Better solution for Movement stop and canceling !
            self.win.getMouse()
            self.win.close 

# Food is not working due to that the windows is crated in the Creature class so Food classes has no access 
# MakeWindow has to be a class at its own ! => how to pass variables between different classes ?

class Food:
    list_f = []
    list_position_of_food = []
    food_count = 0
    hight = GetSystemMetrics(1) 
    wide = GetSystemMetrics(0)
    
    def __init__(self, saturation = 0, size = 10):
        self.saturation = saturation
        self.size = size

    def Creation_of_Food(self):
        self.diameter_food = 10
        self.color = "green"
        self.adjusted_hight = self.hight - self.diameter_food
        self.adjusted_wide = self.wide - self.diameter_food

        self.position_of_food = (random.randrange(0, self.adjusted_wide, 1),random.randrange(0, self.adjusted_hight, 1))
        self.list_position_of_food.append(self.position_of_food)

        f = Circle(Point(self.position_of_food[0],self.position_of_food[1]), self.diameter_food) 
        f.setFill(self.color)
        self.list_f.append(f) 

        self.food_count += 1


    def Draw_Food(self):
        for i in range(len(self.list_f)): # Draws all cratures from the list to the crated window
          self.list_f[i].draw(self.win)



#Test Area where I crate three cratures in the variable x and crate a Window as well as drawing the cratures to it
x = Creatures()

while True:
    if(x.creature_count == 0):
        x.CreationOfCreature(input("Please choose a name for your first Creature:  "))
    if(x.creature_count > 0) and (x.creature_count <= 5):
        while True:
            z = input("Do you want to create another creature(max = 5) [y/n]")
            z = str(z)
            if (z == "y"):
                x.CreationOfCreature(input("Please choose a name for another Creature:  "))
                break
            if (z == "n"):
                x.CreationOfWindow()
                x.DrawCreatures()
                break
            print("Your answer was incorrect")
    if(x.creature_count >= 5):
        print("Sry maximal creature number is 5")
        x.CreationOfWindow()
        x.DrawCreatures()