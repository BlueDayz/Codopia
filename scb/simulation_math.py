# This is the mathematical and statistical approach for an natural selection simulation 

# Section of Import and Packages
import random


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

	def Spawn_Creature(self):
		self.creatures_count += 1
		self.start_position_of_creature = (75000,75000)
		self.list_of_existing_creatures.append(self.start_position_of_creature)
		self.hunger_count = 3 # after 3 days a creature starves
		# create a object with all conditions
		# store the object on a list (later move it around and change hunger over time and distance)

	def Find_nearest_Food(self,F): # Feed in the position of food and than check around the creature's position
		# The creature sees for 5 km if it sees food it will moves toward it, if not a random movement is triggered 
		self.F = F
		self.nearest_Food = self.F.Show_all_food() # define the smalles value in the list to the own position
		# metric to substract from food position the creatures position => than the lowest to use...
		
		# self.list_of_existing_creatures[counter] get your own position related to the food distance, give out nearest food position....

	def Grap_Food(self): # Move toward the food and if it reach the food so restore the hunger counter
		# Creature consumes food and restore the internal hunger_count to 3 days
		pass



# Class for Food	
class Food:
	food_count = 0
	list_of_existing_foods = []

	def Spawn_Food(self):
		self.position_of_food = (90000,90000)
		self.list_of_existing_foods.append(self.position_of_food)
		self.food_count += 1

	def Show_all_food(self): # Function to give the Creature an overview 
		return self.list_of_existing_foods

	def Consume_Food(self): # If a creature reach the food delet it from the food list 
		pass

##### TestArea

C = Creatures()
C.Spawn_Creature()

F = Food()
F.Spawn_Food()

C.Find_nearest_Food(F)
#####

# Functions for the statistics

# Plot after every tick of time the amount of creatures and food
# Later make a graphical output to follow the crature how its moving or atleast store the path for each crature 