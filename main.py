import shapefile
import matplotlib.pyplot as plt

OUTPUT_SIZE = 3000
OUTPUT_RES = 300

def read_shp(file_path):
    shp = shapefile.Reader(file_path)
    return shp.shapes()

#def color_streets(shapes):
    # TODO

def plot_streets(colored_shapes):
    dimension = OUTPUT_SIZE/OUTPUT_RES
    fig, ax = plt.subplots(figsize=(dimension, dimension))

    for shape in colored_shapes:
        x = [point[0] for point in shape.points]
        y = [point[1] for point in shape.points]
        ax.plot(x, y, 'r:')
    plt.savefig('output/solution_uncolored.png', dpi=OUTPUT_RES)

shapes = read_shp('sample/roads.shp')
#print(shapes)
plot_streets(shapes) # plot sample in a single style 
#colored_shapes = color_streets(shapes)
#plot_streets(colored_shapes)
