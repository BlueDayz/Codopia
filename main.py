import vpython as vp
import time
import math



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

    def __repr__(self):
        return '(' + str(self.x1) + ', ' + str(self.x2) + ', ' + str(self.x3) + ')'

class Scene:
    def __init__(self):
        self.canvas = vp.canvas()

    def clear(self):
        while 0 < len(self.canvas.objects):
            self.canvas.objects[len(self.canvas.objects)-1].visible = False
            del self.scene.objects[len(self.canvas.objects)-1]

class Organism:
    def __init__(self, world, position, colour = Vector(1,0.3,0.8)):
        self.position = position
        self.colour = colour
        self.size = 10
        self.vp_object = vp.sphere(canvas = world.scene.canvas, pos = self.position.as_vp_vector(), radius = self.size, color = self.colour.as_vp_vector())

    def move_vec(self, direction):
        self.position += direction
        self.vp_object.pos = self.position.as_vp_vector()

    def move_to(self, world, deg_lat, deg_long):
        self.position = world.coordinate_to_vector(deg_lat, deg_long)
        print(self.position)
        self.vp_object.pos = self.position.as_vp_vector()


class World:
    def __init__(self):
        self.scene = Scene()
        self.organisms = []
        self.radius = 100
        self.object = vp.sphere(canvas = self.scene.canvas, pos = vp.vector(0,0,0), radius = self.radius, color = vp.vector(0,1,0.3))

    def add_organism(self, deg_lat, deg_long):
        v = self.coordinate_to_vector(deg_lat, deg_long)
        new_organism = Organism(world = self, position = v)
        self.organisms += [new_organism]

    def coordinate_to_vector(self, deg_lat, deg_long):
        rad_lat = deg_lat * math.pi / 180
        rad_long = deg_long * math.pi / 180
        
        vz_lat = (-1) ** ((deg_lat + 89) // 180)
        vz_long = (-1) ** ((deg_long + 89) // 180)
        
        if (deg_lat == 90 or deg_lat == 270) and (deg_long == 90 or deg_long == 270):            
            u = vz_lat * vz_long * self.radius
            v = Vector(0, 0, u)
        elif deg_lat == 90 or deg_lat == 270:
            u = vz_lat * vz_long * self.radius * (1 / ((math.tan(rad_lat) * math.cos(rad_long)) ** 2 + math.cos(rad_long) ** 2 + math.sin(rad_long) ** 2) ) ** 0.5
            v = Vector(u * math.sin(rad_long), u * math.cos(rad_long), u * math.tan(rad_lat) * math.cos(rad_long))
        else:
            u = vz_lat * vz_long * self.radius * (1 / ((math.tan(rad_long) * math.cos(rad_lat)) ** 2 + math.cos(rad_lat) ** 2 + math.sin(rad_lat) ** 2) ) ** 0.5
            v = Vector(u * math.tan(rad_long) * math.cos(rad_lat), u * math.cos(rad_lat), u * math.sin(rad_lat))
        return v

    def vector_to_coordinate(self, deg_lat, deg_long):
        return 0


def main():
    w = World()
    la = 0
    lo = 0
    w.add_organism(la, lo)
    while True:
        print("Type int:")
        i = int(input())
        while i > 0:
            time.sleep(0.05)
            la += 1
            lo += 1
            print("la: " + str(la) + "\n")
            print("lo: " + str(lo) + "\n")
            w.organisms[0].move_to(w,la, lo)
            i -= 1
            
def test():
    w = World()
    la = 0
    lo = 0
    w.add_organism(la, lo)
    with open("positions.txt", "w") as f:
        f.write("Latitude\tLongitude\tx\ty\tz\n")
    for la in [0,90,180,270,360]:#range(0,360):
        for lo in range(0,360, 10): #[0,90,180,270,360]:#
            time.sleep(0.05)
            w.organisms[0].move_to(w,la,lo)
            with open("positions.txt", "a") as f:
                f.write(str(la) +"\t"+
                        str(lo)+"\t"+
                        str(w.organisms[0].position.x1)+"\t"+
                        str(w.organisms[0].position.x2)+"\t"+
                        str(w.organisms[0].position.x3)+"\n")       

#main()
test()