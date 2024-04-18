
import math


# class Shape:
#     def __init__(self, name):
#         self.name = name

#     def perimeter(self):
#         raise NotImplementedError("permieter")
    
#     def area(self):
#         raise NotImplementedError("area")
    
#     def density(self, weight):
#         return weight / self.area()


# class Square(Shape):
#     def __init__(self, name, side):
#         super().__init__(name)
#         self.side = side

#     def perimeter(self):
#         return 4 * self.side
    
#     def area(self):
#         return self.side ** 2
    

# class Circle(Shape):
#     def __init__(self, name, radius):
#         super().__init__(name)
#         self.radius = radius

#     def perimeter(self):
#         return 2 * math.pi * self.radius
    
#     def area(self):
#         return math.pi * self.radius ** 2


def shape_density(thing, weight):
    return weight / call(thing, "area")


def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }


Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new
}


#############################

def square_perimeter(thing):
    return 4 * thing["side"]


def square_area(thing):
    return thing["side"] ** 2


def square_larger(thing, size):
    return call(thing, "area") > size


def square_new(name, side):
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new
}


#############################

def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]


def circle_area(thing):
    return math.pi * thing["radius"] ** 2


def circle_larger(thing, size):
    return call(thing, "area") > size


def circle_new(name, radius):
    return make(Shape, name) | {
        "radius": radius,
        "_class": Circle
    }


Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle",
    "_parent": Shape,
    "_new": circle_new
}


#############################

def make(cls, *args):
    return cls["_new"](*args)


def find (cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")


def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)


#############################

if __name__ == '__main__':
    examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        print(f"{n}: {d:.2f}")
        
