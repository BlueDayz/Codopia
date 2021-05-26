import vpython as vp
import time
# import math
import random
# import plotnine as pn
import matplotlib.pyplot as plt
import pandas as pd
import keyboardthread


def random_num_in_radius(number, radius=0.1):
    return number + (
        radius * random.random()
        * (-1) ** random.getrandbits(1)
    )


class Vector:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    def __abs__(self):
        return (
            self.x1 ** 2
            + self.x2 ** 2
            + self.x3 ** 2
        )**0.5

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 + other,
                x2=self.x2 + other,
                x3=self.x3 + other
            )
        elif isinstance(other, Vector):
            return Vector(
                self.x1 + other.x1,
                self.x2 + other.x2,
                self.x3 + other.x3
            )

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 - other,
                x2=self.x2 - other,
                x3=self.x3 - other
            )
        elif isinstance(other, Vector):
            return Vector(
                self.x1 - other.x1,
                self.x2 - other.x2,
                self.x3 - other.x3
            )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 * other,
                x2=self.x2 * other,
                x3=self.x3 * other
            )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                x1=self.x1 / other,
                x2=self.x2 / other,
                x3=self.x3 / other
            )

    def __repr__(self):
        return (
            '(' + str(self.x1)
            + ', ' + str(self.x2)
            + ', ' + str(self.x3) + ')'
        )

    def __str__(self):
        return self.__repr__()

    def as_vp_vector(self):
        return vp.vector(self.x1, self.x2, self.x3)

    def distance_to(self, other):
        return (
            (self.x1 - other.x1) ** 2
            + (self.x2 - other.x2) ** 2
            + (self.x3 - other.x3) ** 2
        ) ** 0.5

    def as_unit_vector(self):
        norm = abs(self)
        return Vector(
            x1=self.x1 / norm,
            x2=self.x2 / norm,
            x3=self.x3 / norm
        )

    def random_vec_in_radius(self, radius=0.1, x1='#', x2='#', x3='#'):
        if x1 == '#':
            x1 = random_num_in_radius(self.x1, radius)
        elif x1 == '=':
            x1 = self.x1
        if x2 == '#':
            x2 = random_num_in_radius(self.x2, radius)
        elif x2 == '=':
            x2 = self.x2
        if x3 == '#':
            x3 = random_num_in_radius(self.x3, radius)
        elif x3 == '=':
            x3 = self.x3
        return Vector(x1, x2, x3)


class Environment:
    def __init__(self):
        self.canvas = vp.canvas(
            width=1280,
            height=800
        )
        self.canvas.camera.rotate(
            angle=30,
            axis=vp.vector(1, 0, 0),
            origin=vp.vector(0, 0, 0)
        )
        self.time = 0
        self.planet = FlatPlanet(self)
        self.organisms = []
        self.data = pd.DataFrame(
            columns=[
                'time',
                'num_organisms',
                'num_fungi',
                'num_plants',
                'num_animals'
            ]
        )

    def add_organism(self, v, type, **kwargs):
        if isinstance(self.planet, FlatPlanet):
            v = Vector(v.x1, self.planet.height / 2, v.x3)
        if type == 'fungus':
            new_organism = Fungus(
                environment=self,
                position=v,
                **kwargs
            )
        elif type == 'plant':
            new_organism = Plant(
                environment=self,
                position=v,
                **kwargs
            )
        elif type == 'animal':
            new_organism = Animal(
                environment=self,
                position=v,
                **kwargs
            )
        else:
            return 'no type'
        # i = 0
        # while i < len(self.organisms):
        #     if (
        #         self.organisms[i].distance_to(new_organism)
        #         < (self.organisms[i].size + new_organism.size) / 2
        #     ):
        #         return 'not added'
        self.organisms += [new_organism]
        return 'added'

    def collect_data(self):
        self.data = self.data.append({
            'time': self.time,
            'num_organisms': len(self.organisms),
            'num_fungi': sum(
                1 if isinstance(x, Fungus) else 0 for x in self.organisms
            ),
            'num_plants': sum(
                1 if isinstance(x, Plant) else 0 for x in self.organisms
            ),
            'num_animals': sum(
                1 if isinstance(x, Animal) else 0 for x in self.organisms
            )
        }, ignore_index=True)

    def plot(self):
        plt.clf()
        plt.plot(
            self.data['time'],
            self.data['num_organisms'],
            color='black',
            label='total'
        )
        plt.plot(
            self.data['time'],
            self.data['num_fungi'],
            color=(0.24, 0.15, 0.13),
            label='fungi'
        )
        plt.plot(
            self.data['time'],
            self.data['num_plants'],
            color=(0.2, 0.4, 0.1),
            label='plants'
        )
        plt.plot(
            self.data['time'],
            self.data['num_animals'],
            color=(0.7, 0.2, 0.3),
            label='animals'
        )
        plt.legend()
        # plt.ion()
        # plt.gcf().canvas.draw_idle()
        # plt.gcf().canvas.start_event_loop(0.3)
        # plt.show(block=False)
        plt.pause(0.05)

    def remove_organism(self, organism):
        i = 0
        while i < len(self.organisms):
            if self.organisms[i] is organism:
                j = 1
                while j <= self.organisms[i].size:
                    self.add_organism(
                        self.organisms[i].position.random_vec_in_radius(
                            radius=self.organisms[i].action_radius
                        ),
                        type='fungus'
                    )
                    j += 1
                del self.organisms[i]
                break
            i += 1
        organism.vp_object.visible = False
        del organism.vp_object
        del organism

    def check_organisms(self):
        for this_organism in self.organisms:
            if this_organism.get_type() == 'plant':
                if this_organism.energy > 16:
                    this_organism.energy -= 16
                    self.add_organism(
                        this_organism.position.random_vec_in_radius(
                            radius=this_organism.action_radius
                        ),
                        type='plant'
                    )
            elif this_organism.get_type() == 'animal':
                for other in self.organisms:
                    if this_organism is other:
                        continue
                    if (
                        this_organism.position.distance_to(other.position)
                        < this_organism.action_radius
                    ):
                        if (
                            this_organism.get_type() == other.get_type()
                            and self.time - this_organism.birth
                            >= this_organism.age_of_fertility
                            and self.time - this_organism.last_reproduced
                            >= this_organism.time_of_infertility
                            and self.time - other.birth
                            >= other.age_of_fertility
                            and self.time - other.last_reproduced
                            >= other.time_of_infertility
                        ):
                            if this_organism.energy >= 30:
                                self.add_organism(
                                    this_organism.position.random_vec_in_radius(
                                        radius=this_organism.action_radius
                                    ),
                                    type='animal',
                                    energy=30
                                )
                                this_organism.energy -= 30
                                this_organism.last_reproduced = self.time
                                other.last_reproduced = self.time
                                self.organisms[len(self.organisms)-1]
                        elif this_organism.mouth_size > other.size:
                            this_organism.energy += other.energy
                            self.remove_organism(other)
                        elif other.get_type() == 'plant':
                            this_organism.energy += this_organism.mouth_size
                            other.energy -= this_organism.mouth_size
                            other.size -= this_organism.mouth_size
                            other.update()
            elif this_organism.get_type() == 'fungus':
                pass
            if (
                this_organism.energy <= 0
                or self.time - this_organism.birth
                > this_organism.max_age
            ):
                self.remove_organism(this_organism)
                continue

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
    def __init__(
        self,
        environment,
        position,
        size=0,
        energy=0,
        speed=0,
        action_radius=0,
        last_reproduced=0,
        age_of_fertility=0,
        time_of_infertility=0,
        max_age=0,
        colour=Vector(1, 0.3, 0.8)
    ):
        self.position = position
        self.colour = colour
        self.size = size
        self.vp_object = vp.sphere(
            canvas=environment.canvas,
            pos=self.position.as_vp_vector(),
            radius=self.size / 2,
            color=self.colour.as_vp_vector()
        )
        self.energy = energy
        self.speed = speed
        self.action_radius = action_radius
        self.birth = environment.time
        self.last_reproduced = last_reproduced
        self.age_of_fertility = age_of_fertility
        self.time_of_infertility = time_of_infertility
        self.max_age = max_age

    def __repr__(self):
        return (
            '(' + self.get_type() + ', '
            + str(self.position) + ')'
        )

    def __str__(self):
        return self.__repr__()

    def update(self):
        self.vp_object.radius = self.size / 2
        self.vp_object.position = self.position.as_vp_vector()

    def get_type(self):
        return 'organsim'

    def move_in_direction(self, direction, steps=1):
        self.position += direction.as_unit_vector() * steps
        self.vp_object.pos = self.position.as_vp_vector()

    def next_move(self):
        pass


class Fungus(Organism):
    def __init__(
        self,
        environment,
        position,
        size=0.2,
        energy=10,
        speed=0,
        action_radius=2,
        last_reproduced=0,
        age_of_fertility=0,
        time_of_infertility=0.1,
        max_age=100,
        colour=Vector(0.24, 0.15, 0.13)
    ):
        Organism.__init__(
            self=self,
            environment=environment,
            position=position,
            size=size,
            energy=energy,
            speed=speed,
            action_radius=action_radius,
            last_reproduced=last_reproduced,
            age_of_fertility=age_of_fertility,
            time_of_infertility=time_of_infertility,
            colour=colour,
            max_age=max_age
        )

    def get_type(self):
        return 'fungus'


class Plant(Organism):
    def __init__(
        self,
        environment,
        position,
        size=1,
        energy=1,
        speed=0,
        action_radius=10,
        last_reproduced=0,
        age_of_fertility=1,
        time_of_infertility=1,
        max_age=100,
        colour=Vector(0.2, 0.4, 0.1)
    ):
        Organism.__init__(
            self=self,
            environment=environment,
            position=position,
            size=size,
            energy=energy,
            speed=speed,
            action_radius=action_radius,
            last_reproduced=last_reproduced,
            age_of_fertility=age_of_fertility,
            time_of_infertility=time_of_infertility,
            colour=colour,
            max_age=max_age
        )

    def next_move(self):
        self.energy += 1
        self.size += 0.1
        self.update()

    def get_type(self):
        return 'plant'


class Animal(Organism):
    def __init__(
        self,
        environment,
        position,
        size=4,
        energy=100,
        speed=1,
        action_radius=2,
        last_reproduced=0,
        age_of_fertility=10,
        time_of_infertility=1,
        max_age=50,
        mouth_size=1,
        colour=Vector(0.7, 0.2, 0.3)
    ):
        self.mouth_size = mouth_size
        Organism.__init__(
            self=self,
            environment=environment,
            position=position,
            size=size,
            energy=energy,
            speed=speed,
            action_radius=action_radius,
            last_reproduced=last_reproduced,
            age_of_fertility=age_of_fertility,
            time_of_infertility=time_of_infertility,
            colour=colour,
            max_age=max_age
        )

    def get_type(self):
        return 'animal'

    def next_move(self):
        if self.energy > 0:
            self.move_in_direction(
                self.position - self.position.random_vec_in_radius(x2='='),
                self.speed
            )
            self.energy -= self.speed


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


def main():
    e = Environment()
    inp = ['']

    def callback_new_organism(inp, environment=e, output_mut=inp):
        if inp == 'f':
            type = 'fungus'
        elif inp == 'p':
            type = 'plant'
        elif inp == 'a':
            type = 'animal'
        elif inp == 'x':
            output_mut[0] = 'x'
            return 0
        else:
            return 0
        environment.add_organism(
            Vector(-10+20*random.random(), 0, -10+20*random.random()),
            type=type
        )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    e.add_organism(
        Vector(-10+20*random.random(), 0, -10+20*random.random()),
        type='plant'
    )
    kthread = keyboardthread.KeyboardThread(callback_new_organism)
    i = 0
    while 'x' not in inp:
        i += 1
        if i == 32:
            for j in range(0, 10):
                e.add_organism(
                    Vector(-10+20*random.random(), 0, -10+20*random.random()),
                    type='animal'
                )
        time.sleep(0.2)
        e.next_timeframe()
    e.canvas.delete()


main()
