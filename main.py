import vpython as vp
import time
import math


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


class Scene:
    def __init__(self):
        self.canvas = vp.canvas()

    def clear(self):
        while 0 < len(self.canvas.objects):
            self.canvas.objects[len(self.canvas.objects)-1].visible = False
            del self.scene.objects[len(self.canvas.objects)-1]


class Organism:
    def __init__(self, planet, position, colour=Vector(1, 0.3, 0.8)):
        self.position = position
        self.colour = colour
        self.size = 2
        self.vp_object = vp.sphere(
            canvas=planet.scene.canvas,
            pos=self.position.as_vp_vector(),
            radius=self.size,
            color=self.colour.as_vp_vector()
        )

    def move_to_vec(self, direction, steps=1):
        self.position += steps * direction / abs(direction)
        self.vp_object.pos = self.position.as_vp_vector()

    def move_to_deg(self, planet, deg_lat, deg_long):
        self.position = planet.coordinate_to_vector(deg_lat, deg_long)
        print(self.position)
        self.vp_object.pos = self.position.as_vp_vector()


class Planet:
    def __init__(self):
        self.scene = Scene()
        self.organisms = []
        self.radius = 100
        self.object = vp.sphere(
            canvas=self.scene.canvas,
            pos=vp.vector(0, 0, 0),
            radius=self.radius,
            color=vp.vector(0, 1, 0.3)
        )

    def add_organism(self, deg_lat, deg_long):
        v = self.coordinate_to_vector(deg_lat, deg_long)
        new_organism = Organism(
            planet=self,
            position=v
        )
        self.organisms += [new_organism]

    def coordinate_to_vector(self, deg_lat, deg_long):
        rad_lat = deg_lat * math.pi / 180
        rad_long = deg_long * math.pi / 180

        vz_lat = (-1) ** ((deg_lat + 89) // 180)
        vz_long = (-1) ** ((deg_long + 89) // 180)

        if (
            (deg_lat == 90 or deg_lat == 270)
            and (deg_long == 90 or deg_long == 270)
        ):
            u = vz_lat * vz_long * self.radius
            v = Vector(0, 0, u)
        elif deg_lat == 90 or deg_lat == 270:
            u = vz_lat * vz_long * self.radius * (
                1 / (
                    (math.tan(rad_lat) * math.cos(rad_long)) ** 2
                    + math.cos(rad_long) ** 2
                    + math.sin(rad_long) ** 2
                )
            ) ** 0.5
            v = Vector(
                u * math.sin(rad_long),
                u * math.cos(rad_long),
                u * math.tan(rad_lat) * math.cos(rad_long)
            )
        else:
            u = vz_lat * vz_long * self.radius * (
                1 / (
                    (math.tan(rad_long) * math.cos(rad_lat)) ** 2
                    + math.cos(rad_lat) ** 2
                    + math.sin(rad_lat) ** 2
                )
            ) ** 0.5
            v = Vector(
                u * math.tan(rad_long) * math.cos(rad_lat),
                u * math.cos(rad_lat),
                u * math.sin(rad_lat)
            )
        return v

    def vector_to_coordinate(self, deg_lat, deg_long):
        return 0


class FlatPlanet:
    def __init__(self):
        self.scene = Scene()
        self.organisms = []
        self.length = 100
        self.height = 10
        self.width = 100
        self.object = vp.box(
            canvas=self.scene.canvas,
            pos=vp.vector(0, 0, 0),
            color=vp.vector(0, 1, 0.3),
            length=self.length,
            height=self.height,
            width=self.width
        )

    def add_organism(self, x1, x2):
        v = Vector(x1, x2, self.height)
        new_organism = Organism(
            planet=self,
            position=v
        )
        self.organisms += [new_organism]


def main():
    w = FlatPlanet()
    w.add_organism(30, 30)
    while True:
        print("Type x1:")
        x1 = float(input())
        print("Type x2:")
        x2 = float(input())
        print("Type steps:")
        steps = float(input())
        w.organisms[0].move_to_vec(Vector(x1, x2, 0), steps)


main()
