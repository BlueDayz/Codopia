# This is the mathematical and statistical approach for an natural selection simulation 

# Section of Import and Packages
#%%
import random
import math
import numpy as np
import matplotlib.pyplot as plt

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
	array = np.zeros(shape = (1,1), dtype= (int), order = "C")
	dict = {}

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

		#### Room for improvement of the nearest food finding algorithm

		# The Nearest Food finding algorithm via numpy and dicts
		self.array = np.zeros(shape = (len(self.list_of_existing_creatures),len(self.nearest_Food)), dtype= (int), order = "C")

		for i in range(0, len(self.list_of_existing_creatures)):
			for j in range(0, len(self.nearest_Food)):
				self.array[i,j] = math.hypot(self.list_of_existing_creatures[i][0] - self.nearest_Food[j][0], self.list_of_existing_creatures[i][1] - self.nearest_Food[j][1])
		
		x = np.amin(self.array, axis = 1) # Find the minimum for each row = creature

		for z in range(0,len(x)): # len of minimums = rows 
			y = np.where(self.array[z,:] == np.amin(self.array[z,:])) # Find the row and colum index for the minimum value
			self.dict[z] = {"Creature_ID":z,"Creature_Position":self.list_of_existing_creatures[z], "Nearest_Food_ID":y[0][0],"Food_Position":self.nearest_Food[y[0][0]], "Distance[meter]":x[z], "Arrival_Time[h]":int((x[z]/60)/self.standard_speed)} # puts everything into a dict ordered

		# Just a method to show the dict prettier ... unimportant!
		print("{0:^16s}  {1:^16s}  {2:^16s}  {3:^16s}  {4:^16s}  {5:^16s}  {6:^16s}".format('Case', 'Creature_ID', 'Creature_Position', 'Nearest_Food_ID', 'Food_Position','Distance[meter]', 'Arrival_Time[h]'))
		for k,v in self.dict.items():
			CID, CPos, NFID, FPos, Dis, Arriv = v.items()

			print("{0:^16d}  {1:^16d}  {2:^16s}  {3:^16d}  {4:^16s}  {5:^16d}  {6:^16d}".format(k,CID[1],str(CPos[1]),NFID[1],str(FPos[1]),Dis[1],Arriv[1]))

		# only for presentation
		# print("\n",self.array)

		######
		
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
F = Food()

min_distance = 0
max_distance = 15000
step = 1

Creature_spawn_amount = 4
Food_spawn_amount = 8

for i in range(0,Creature_spawn_amount):
	x = random.randrange(min_distance, max_distance,step)
	y = random.randrange(min_distance, max_distance,step)

	C.Spawn_Creature(x, y)


for j in range(0, Food_spawn_amount):
	x = random.randrange(min_distance, max_distance,step)
	y = random.randrange(min_distance, max_distance,step)

	F.Spawn_Food(x, y)

C.Find_nearest_Food(F)
#%%

### Plot of the closest food to the creatures
n = len(C.list_of_existing_creatures)
colors = list(range(0,n))
z=0




plt.figure("All food all creatures")

px = list(map(lambda x:x[0], C.list_of_existing_creatures))
py = list(map(lambda x:x[1], C.list_of_existing_creatures))

Unlucky_C_plot = plt.scatter(px, py, c = "black", cmap = "bwr", marker="o")


px = list(map(lambda x:x[0], F.list_of_existing_foods))
py = list(map(lambda x:x[1], F.list_of_existing_foods))

Unwanted_F_plot = plt.scatter(px, py, c = "black", cmap = "bwr", marker="^")

plt.show()


# Next figure to show the different Creatures - Food pairs whic hare the nearest to each other - lets see if its stays....
plt.figure("Nearest Food for Creature")

#Lists for the scatter plot
C_list = []
F_list = []

#A way to extract nested dicts in python and give them to a list
for key, values in C.dict.items():
	CID, CPos, NFID, FPos, Dist, ArrTim = values.items()
	C_list.append((CPos[1][0],CPos[1][1]))
	F_list.append((FPos[1][0],FPos[1][1]))

#x and y coodinates of every nested entry in the dict for each case
px = list(map(lambda x:x[0], C_list))
py = list(map(lambda x:x[1], C_list))

#creature plot
C_plot = plt.scatter(px,py, c = colors, cmap = "bwr", marker ="o")

#same for the food
px = list(map(lambda x:x[0], F_list))
py = list(map(lambda x:x[1], F_list))

F_plot = plt.scatter(px, py, c = colors, cmap = "bwr", marker ="^")
plt.legend([C_plot,F_plot],["Paired Creatures","Paired Food"], bbox_to_anchor=(1.05, 1))
plt.colorbar()

# Colorbar and legend have to been fixed ....
plt.show()


#####

# Functions for the statistics

# Plot after every tick of time the amount of creatures and food
# Later make a graphical output to follow the crature how its moving or atleast store the path for each crature 