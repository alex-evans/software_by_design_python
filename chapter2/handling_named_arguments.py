# The final version of call declares a parameter called *args
# to capture all the positional arguments of the method being 
# called and then spreads them in the actual call. Modify it 
# to capture and spread named arguments as well.

def square_new(name, side):
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new
}


def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)


def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")


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


def main():
    examples = [square_new("sq", 3), circle_new("ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        print(f"{n}: {d:.2f}")