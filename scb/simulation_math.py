# This is the mathematical and statistical approach for an natural selection simulation 

# Section of Import and Packages
#%%
import random
import math
import numpy as np

#%%
# Class for the Environment
class Environment:
	dimention = (150000,150000) # meters
	day = 16 # h
	days = 0
	
	def Spawn_Environment(self):
		# rectangle with dimention and days as fields for cratures and food to spawn
		pass

# Maybe it would be smart to collect positions of creatures and food in the environment and load it only once - like live for better performance !


# Class for Creatures 
class Creatures:
	creatures_count = 0
	list_of_existing_creatures = []
	standard_speed = 3 # Km/h
	standard_step_size = 0.7 # meters
	standard_vision_of_field = 5 # Km
	standard_size = 1.80 # meters
	array_creature_food_distance = np.array([[["Creature"], ["Food"], ["Distance"]]])

	def Spawn_Creature(self, X, Y):
		self.creatures_count += 1
		self.hunger_count = 3 # after 3 days a creature starves
		self.start_position_of_creature = (X, Y)
		self.list_of_existing_creatures.append(self.start_position_of_creature)
		
		# create a object with all conditions
		# store the object on a list (later move it around and change hunger over time and distance)

	def Find_nearest_Food(self,F): # Feed in the position of food and than check around the creature's position
		# The creature sees for 5 km if it sees food it will moves toward it, if not a random movement is triggered 
		self.F = F
		self.nearest_Food = self.F.Show_all_food() # define the smalles value in the list to the own position
		for i in range(0, len(self.list_of_existing_creatures)):
			for j in range(0, len(self.nearest_Food)):
				dist = math.hypot(self.list_of_existing_creatures[i][0] - self.nearest_Food[j][0], self.list_of_existing_creatures[i][1] - self.nearest_Food[j][1])
				self.array_creature_food_distance = np.append(self.array_creature_food_distance, [[[i], [j], [dist]]], axis = 2)

		# self.list_of_existing_creatures[counter] get your own position related to the food distance, give out nearest food position....

	def Grap_Food(self): # Move toward the food and if it reach the food so restore the hunger counter
		# Creature consumes food and restore the internal hunger_count to 3 days
		pass



# Class for Food	
class Food:
	food_count = 0
	list_of_existing_foods = []

	def Spawn_Food(self, X, Y):
		self.position_of_food = (X,Y)
		self.list_of_existing_foods.append(self.position_of_food)
		self.food_count += 1

	def Show_all_food(self): # Function to give the Creature an overview 
		return self.list_of_existing_foods

	def Consume_Food(self): # If a creature reach the food delet it from the food list 
		pass

##### TestArea
#%%
C = Creatures()
C.Spawn_Creature(75000, 75000)
C.Spawn_Creature(10000, 10000)

F = Food()
F.Spawn_Food(5000, 5000)
F.Spawn_Food(7000, 7000)
F.Spawn_Food(9000, 9000)
F.Spawn_Food(12000, 12000)
F.Spawn_Food(15000, 15000)


#%%
C.Find_nearest_Food(F)

x = C.array_creature_food_distance
y = np.argwhere(x[0,2,:] == min(x[0,2,:]))
z1 = x[0,2,y].astype(float)
z2 = x[0,1,y].astype(float)
z3 = x[0,0,y].astype(float)

print(f"The entry with the lowest distance is: {y} \n") 
print(f"The lowest value in the whole entry is: {z1} \n")
print(f"The the food object which is nearest is: {z2} to the animal: {z3} \n")

# ==> use the index to find the food piece and creature number, than move them towards the cooridnates 

#####

# Functions for the statistics

# Plot after every tick of time the amount of creatures and food
# Later make a graphical output to follow the crature how its moving or atleast store the path for each crature 