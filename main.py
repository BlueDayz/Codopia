import vpython as vp
import time
# import math
import random
# import plotnine as pn
import matplotlib.pyplot as plt
import pandas as pd


class Vector:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    def __abs__(self):
        return (
            (self.x1)**2
            + (self.x2)**2
            + (self.x3)**2
        )**0.5

    def __add__(self, other):
        return Vector(
            self.x1 + other.x1,
            self.x2 + other.x2,
            self.x3 + other.x3
        )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 * other,
                x2=self.x2 * other,
                x3=self.x3 * other
            )

    def __repr__(self):
        return (
            '(' + str(self.x1)
            + ', ' + str(self.x2)
            + ', ' + str(self.x3) + ')'
        )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 / other,
                x2=self.x2 / other,
                x3=self.x3 / other
            )

    def as_vp_vector(self):
        return vp.vector(self.x1, self.x2, self.x3)

    def distance_to(self, other):
        return (
            (self.x1-other.x1)**2
            + (self.x2-other.x2)**2
            + (self.x3-other.x3)**2
        )**0.5

    def as_unit_vector(self):
        norm = abs(self)
        return Vector(
            x1=self.x1 / norm,
            x2=self.x2 / norm,
            x3=self.x3 / norm
        )


class Environment:
    def __init__(self):
        self.canvas = vp.canvas()
        self.time = 0
        self.planet = FlatPlanet(self)
        self.organisms = []
        self.data = pd.DataFrame(columns=['time', 'num_organisms'])

    def add_organism(self, x1, x3):
        v = Vector(x1, self.planet.height / 2, x3)
        new_organism = Organism(
            environment=self,
            position=v
        )
        self.organisms += [new_organism]

    def collect_data(self):
        self.data = self.data.append({
            'time': self.time,
            'num_organisms': len(self.organisms)
        }, ignore_index=True)

    def plot(self):
        plt.scatter(self.time, len(self.organisms), c='black')
        plt.pause(0.05)
        # p = (
        #     pn.ggplot(self.data)
        #     + pn.aes(x='time', y='num_organisms')
        #     + pn.geom_point()
        #     # + scale_x_continuous(breaks = range(0,360,90))
        #     # + scale_y_continuous(breaks = range(0,360,90))
        #     # + scale_fill_grey(start = 0, end = 1)
        # )
        # p.draw(show=True)

    def remove_organism(self, organism):
        i = 0
        while i < len(self.organisms):
            if self.organisms[i] is organism:
                del self.organisms[i]
                break
            i += 1
        organism.vp_object.visible = False
        del organism.vp_object
        del organism

    def check_organisms(self):
        i = 0
        while i < len(self.organisms):
            if self.organisms[i].energy < 0:
                self.remove_organism(self.organisms[i])
            for other in self.organisms:
                if self.organisms[i] is other:
                    continue
                if (
                    self.organisms[i].position.distance_to(other.position)
                    < self.organisms[i].seeing_distance
                    and self.time - self.organisms[i].birth
                    >= self.organisms[i].age_of_fertility
                    and self.time - self.organisms[i].last_reproduced
                    >= self.organisms[i].time_of_infertility
                    and self.time - other.birth
                    >= other.age_of_fertility
                    and self.time - other.last_reproduced
                    >= other.time_of_infertility
                ):
                    if type(self.organisms[i]) == type(other):
                        if self.organisms[i].energy >= 30:
                            self.add_organism(
                                self.organisms[i].position.x1
                                + self.organisms[i].seeing_distance * (
                                    (-1) ** random.getrandbits(1)
                                ),
                                self.organisms[i].position.x3
                                + self.organisms[i].seeing_distance * (
                                    (-1) ** random.getrandbits(1)
                                )
                            )
                            self.organisms[i].energy -= 30
                            self.organisms[i].last_reproduced
                            other
                            self.organisms[len(self.organisms)-1]
                    elif self.organisms[i].size > other.size:
                        self.remove_organism(other)
                        self.organisms[i].energy += other.energy
            i += 1

    def next_timeframe(self):
        self.collect_data()
        self.plot()
        self.time += 1
        for o in self.organisms:
            o.next_move()
        self.check_organisms()

    def clear(self):
        while 0 < len(self.canvas.objects):
            self.canvas.objects[len(self.canvas.objects)-1].visible = False
            del self.scene.objects[len(self.canvas.objects)-1]


class Organism:
    def __init__(self, environment, position, colour=Vector(1, 0.3, 0.8)):
        self.position = position
        self.colour = colour
        self.size = 2
        self.vp_object = vp.sphere(
            canvas=environment.canvas,
            pos=self.position.as_vp_vector(),
            radius=self.size,
            color=self.colour.as_vp_vector()
        )
        self.energy = 100
        self.speed = 1
        self.seeing_distance = 4
        self.birth = environment.time
        self.last_reproduced = 0
        self.age_of_fertility = 10
        self.time_of_infertility = 1

    def move_to_vec(self, direction, steps=1):
        self.position += direction * steps / abs(direction)
        self.vp_object.pos = self.position.as_vp_vector()

    def move_to_deg(self, planet, deg_lat, deg_long):
        self.position = planet.coordinate_to_vector(deg_lat, deg_long)
        print(self.position)
        self.vp_object.pos = self.position.as_vp_vector()

    def next_move(self):
        if self.energy >= 0:
            self.move_to_vec(
                Vector(
                    -1 + (1--1) * random.random(),
                    0,
                    -1 + (1--1) * random.random()
                ),
                self.speed
            )
            self.energy -= self.speed


# class Planet:
#     def __init__(self):
#         self.scene = Environment()
#         self.organisms = []
#         self.radius = 100
#         self.object = vp.sphere(
#             canvas=self.scene.canvas,
#             pos=vp.vector(0, 0, 0),
#             radius=self.radius,
#             color=vp.vector(0, 1, 0.3)
#         )
#
#     def add_organism(self, deg_lat, deg_long):
#         v = self.coordinate_to_vector(deg_lat, deg_long)
#         new_organism = Organism(
#             environment=self,
#             position=v
#         )
#         self.organisms += [new_organism]
#
#     def coordinate_to_vector(self, deg_lat, deg_long):
#         rad_lat = deg_lat * math.pi / 180
#         rad_long = deg_long * math.pi / 180
#
#         vz_lat = (-1) ** ((deg_lat + 89) // 180)
#         vz_long = (-1) ** ((deg_long + 89) // 180)
#
#         if (
#             (deg_lat == 90 or deg_lat == 270)
#             and (deg_long == 90 or deg_long == 270)
#         ):
#             u = vz_lat * vz_long * self.radius
#             v = Vector(0, 0, u)
#         elif deg_lat == 90 or deg_lat == 270:
#             u = vz_lat * vz_long * self.radius * (
#                 1 / (
#                     (math.tan(rad_lat) * math.cos(rad_long)) ** 2
#                     + math.cos(rad_long) ** 2
#                     + math.sin(rad_long) ** 2
#                 )
#             ) ** 0.5
#             v = Vector(
#                 u * math.sin(rad_long),
#                 u * math.cos(rad_long),
#                 u * math.tan(rad_lat) * math.cos(rad_long)
#             )
#         else:
#             u = vz_lat * vz_long * self.radius * (
#                 1 / (
#                     (math.tan(rad_long) * math.cos(rad_lat)) ** 2
#                     + math.cos(rad_lat) ** 2
#                     + math.sin(rad_lat) ** 2
#                 )
#             ) ** 0.5
#             v = Vector(
#                 u * math.tan(rad_long) * math.cos(rad_lat),
#                 u * math.cos(rad_lat),
#                 u * math.sin(rad_lat)
#             )
#         return v
#
#     def vector_to_coordinate(self, deg_lat, deg_long):
#         return 0


<<<<<<< HEAD
class FlatPlanet:
    def __init__(self, environment):
        self.organisms = []
        self.length = 100
        self.height = 4
        self.width = 100
        self.object = vp.box(
            canvas=environment.canvas,
            pos=vp.vector(0, 0, 0),
            color=vp.vector(0.8, 0.5, 0.3),
            length=self.length,
            height=self.height,
            width=self.width
        )
=======
    def coordinate_to_vector(self, deg_lat, deg_long):
        rad_lat = deg_lat * math.pi / 180
        rad_long = deg_long * math.pi / 180
        
        vz_lat = (-1) ** ((deg_lat + 89) // 180)
        vz_long = (-1) ** ((deg_long + 89) // 180)
        
        if (deg_lat == 90 or deg_lat == 270) and (deg_long == 90 or deg_long == 270):            
            u = vz_lat * vz_long * self.radius
            v = Vector(0, 0, u)
        elif deg_long == 90 or deg_long == 270:
            u = vz_lat * vz_long * self.radius * (1 / ((math.tan(rad_lat) * math.cos(rad_long)) ** 2 + math.cos(rad_long) ** 2 + math.sin(rad_long) ** 2) ) ** 0.5
            v = Vector(u * math.sin(rad_long), u * math.cos(rad_long), u * math.tan(rad_lat) * math.cos(rad_long))
        else:
            u = vz_lat * vz_long * self.radius * (1 / ((math.tan(rad_long) * math.cos(rad_lat)) ** 2 + math.cos(rad_lat) ** 2 + math.sin(rad_lat) ** 2) ) ** 0.5
            v = Vector(u * math.tan(rad_long) * math.cos(rad_lat), u * math.cos(rad_lat), u * math.sin(rad_lat))
        return v

    def vector_to_coordinate(self, v):
        rad_lat = math.asin(v.x3/self.radius)
        rad_long = math.asin(v.x1/self.radius)
        deg_lat = rad_lat * 180 / math.pi 
        deg_long = rad_long * 180 / math.pi
        return (str(deg_lat) + "\t" + str(deg_long) + "\n")
        
>>>>>>> bc741bd3509ecf42fced3d922e879be10af8dcac


def main():
    e = Environment()
    e.add_organism(5, 5)
    e.add_organism(5, -5)
    e.add_organism(-5, 5)
    e.add_organism(-5, -5)
    while True:
<<<<<<< HEAD
        time.sleep(0.2)
        e.next_timeframe()
    # while True:
    #     print("Type x1:")
    #     x1 = float(input())
    #     print("Type x3:")
    #     x3 = float(input())
    #     print("Type steps:")
    #     steps = float(input())
    #     w.organisms[0].move_to_vec(Vector(x1, 0, x3), steps)


main()
=======
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
        f.write("Latitude\tLongitude\tx\ty\tz\tlat\tlong\n")
    for la in [0,90,180,270,360]:#range(0,360):
        for lo in range(0,360, 10): #[0,90,180,270,360]:#
            time.sleep(0.05)
            w.organisms[0].move_to(w,la,lo)
            with open("positions.txt", "a") as f:
                f.write(str(la) +"\t"+
                        str(lo)+"\t"+
                        str(w.organisms[0].position.x1)+"\t"+
                        str(w.organisms[0].position.x2)+"\t"+
                        str(w.organisms[0].position.x3)+"\t"+ w.vector_to_coordinate(w.organisms[0].position)+"\n")       

#main()
test()
>>>>>>> bc741bd3509ecf42fced3d922e879be10af8dcac
