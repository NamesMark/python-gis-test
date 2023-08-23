import shapefile
import matplotlib.pyplot as plt
import random

from colors import COLORS

OUTPUT_SIZE = 3000
OUTPUT_RES = 300

def read_shp(file_path):
    shp = shapefile.Reader(file_path)
    return shp.shapes()

def color_streets(shapes):
    colors = []
    for _ in shapes:
        colors.append(random.choice(COLORS))
    return colors

def plot_streets(shapes, colors):
    dimension = OUTPUT_SIZE/OUTPUT_RES
    fig, ax = plt.subplots(figsize=(dimension, dimension))

    for shape, color in zip(shapes, colors):
        x = [point[0] for point in shape.points]
        y = [point[1] for point in shape.points]
        ax.plot(x, y, color=color)  
    plt.savefig('output/solution.png', dpi=OUTPUT_RES)

shapes = read_shp('sample/roads.shp')
#print(shapes)
#plot_streets(shapes) # plot sample in a single style 
colors = color_streets(shapes)
plot_streets(shapes, colors)
