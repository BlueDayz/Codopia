# This is the mathematical and statistical approach for an natural selection simulation 

# Section of Import and Packages
#%%
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
	df_creatures = pd.DataFrame({})
	array = np.zeros(shape = (1,1), dtype= (int), order = "C")


	def Spawn_Creature(self, X, Y):
		self.creatures_count += 1
		self.hunger_count = 3 # after 3 days a creature starves
		self.start_position_of_creature = (X, Y)
		self.list_of_existing_creatures.append(self.start_position_of_creature)
		
	def Find_nearest_Food(self,F): # Feed in the position of food and than check around the creature's position
		# The creature sees for 5 km if it sees food it will moves toward it, if not a random movement is triggered 
		self.F = F
		self.nearest_Food = self.F.Show_all_food()

		self.array = np.zeros(shape = (len(self.list_of_existing_creatures),len(self.nearest_Food)), dtype= (int), order = "C")

		for i in range(0, len(self.list_of_existing_creatures)):
			for j in range(0, len(self.nearest_Food)):
				self.array[i,j] = math.hypot(self.list_of_existing_creatures[i][0] - self.nearest_Food[j:j+1]["Fx"], self.list_of_existing_creatures[i][1] - self.nearest_Food[j:j+1]["Fy"])

		x = np.amin(self.array, axis = 1) # Find the minimum for each row = creature

		for z in range(0,len(x)): # len of minimums = rows 
			y = np.where(self.array[z,:] == np.amin(self.array[z,:])) # Find the row and colum index for the minimum value

			self.tmp_C = pd.DataFrame({"C_ID":z,"Cx":self.list_of_existing_creatures[z][0],"Cy":self.list_of_existing_creatures[z][1],"Nearest_Food":y[0][0],"NFx":self.nearest_Food[y[0][0]:y[0][0]+1]["Fx"],"NFy":self.nearest_Food[y[0][0]:y[0][0]+1]["Fy"],"Group":np.repeat("Paired_Creature",1),"Distance":x[z],"Arrival_Time[h]":int((x[z]/60)/self.standard_speed)})
			self.df_creatures = self.df_creatures.append(self.tmp_C,ignore_index=True)	

		print(self.df_creatures)

		def Grap_Food(self): # Move toward the food and if it reach the food so restore the hunger counter
			# Creature consumes food and restore the internal hunger_count to 3 days
			pass


# Class for Food	
class Food:
	df_foods = pd.DataFrame({})

	def Spawn_Food(self, X, Y):
		self.position_of_food = (X,Y)
		
		self.tmp_F = pd.DataFrame({"Fx":self.position_of_food[0],"Fy":self.position_of_food[1],"group":np.repeat("unpaired_food",1)})
		self.df_foods = self.df_foods.append(self.tmp_F,ignore_index=True)

	def Show_all_food(self): # Function to give the Creature an overview 
		return self.df_foods

	def Consume_Food(self): # If a creature reach the food delet it from the food list 
		pass

##### TestArea
#%%
C = Creatures()
F = Food()

min_distance = 0
max_distance = 15000
step = 1

##Important variable part !
Creature_spawn_amount = 10
Food_spawn_amount = 50

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
F_points = plt.scatter(F.df_foods["Fx"],F.df_foods["Fy"],s=15,marker="x",color="black")
C_points = plt.scatter(C.df_creatures["Cx"],C.df_creatures["Cy"],c = C.df_creatures.index,s=20,marker="o",cmap="Spectral")
NF_points = plt.scatter(C.df_creatures["NFx"],C.df_creatures["NFy"],c = C.df_creatures.index,s=15,marker="x",cmap="Spectral")


plt.colorbar(C_points, label="Creature",ticks=list(range(0,len(C.df_creatures["C_ID"]),1)))
plt.legend([F_points,C_points,NF_points],["unpaired Foods","paired Creatures","paired Foods"])

plt.ylabel("Y-Pos")
plt.xlabel("X-Pos")
plt.title("Creature and Food correlation [paired & unpaired]")

plt.show()