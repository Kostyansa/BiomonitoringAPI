import random


def color_randomizer(labels_quantity):
    colors = {}
    for i in range(-1, labels_quantity):
        colors[i] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    return colors


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def rude_filter(image, kernel = (5, 5)):
    for i in image.shape[0]:
        for j in image.shape[1]:
            pass