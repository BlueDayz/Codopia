import vpython as vp
import time

class Vector:
    def __init__(self,x1,x2,x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
    
    def as_vp_vector(self):
        return vp.vector(self.x1,self.x2,self.x3)
    
    def __add__(self, other):
        return Vector(self.x1 + other.x1, self.x2 + other.x2, self.x3 + other.x3)
    
    def distance_to(self, other):
        return ((self.x1-other.x1)**2 + (self.x2-other.x2)**2 + (self.x3-other.x3)**2)**0.5

class Scene:
    def __init__(self):
        self.canvas = vp.canvas()
        
    def update_scene(self):
        self.clear()
        
    def clear(self):
        while 0 < len(self.canvas.objects):
            self.canvas.objects[len(self.canvas.objects)-1].visible = False
            del self.scene.objects[len(self.canvas.objects)-1]

class Organism:
    def __init__(self, position, world):
        self.position = position
        self.colour = Vector(1,0.3,0.8)
        self.size = 0.5
        self.vp_object = vp.sphere(canvas = world.scene.canvas, pos = self.position.as_vp_vector(), radius = self.size, color = self.colour.as_vp_vector())
        
    def move(self, direction):
        self.position += direction
        self.vp_object.pos = self.position.as_vp_vector()

class World:
    def __init__(self):
        self.scene = Scene()
        self.organisms = []
        self.radius = 1000
        self.object = vp.sphere(canvas = self.scene.canvas, pos = vp.vector(0,0,0), radius = self.radius, color = vp.vector(0,1,0.3))
        
    def add_organism(self):
        new_organism = Organism(self)
        self.organisms += [new_organism]

def main():
    w = World()
    w.add_organism()
    while True:
        time.sleep(0.1)
        w.organisms[0].move(Vector(0.1,0,0))


main()