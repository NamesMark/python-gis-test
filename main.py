import shapefile
import matplotlib.pyplot as plt
import random
import math

from colors import COLORS
from itertools import cycle

OUTPUT_SIZE = 3000
OUTPUT_RES = 300
MAX_ANGLE = 45

INPUT_PATH = 'sample/roads_tiny.shp'
OUTPUT_PATH = 'output/solution.png'

color_iter = cycle(COLORS)
    
class Street:
    def __init__(self, shape):
        self.shape = shape
        self.color = None

def read_shp(file_path):
    shp = shapefile.Reader(file_path)
    return [Street(shape) for shape in shp.shapes()]

def plot(streets):
    dimension = OUTPUT_SIZE / OUTPUT_RES
    fig, ax = plt.subplots(figsize=(dimension, dimension))

    for street in streets:
        shape = street.shape
        x = [point[0] for point in shape.points]
        y = [point[1] for point in shape.points]
        ax.plot(x, y, color=street.color)
    print("SAVED FILE")
    plt.savefig(OUTPUT_PATH, dpi=OUTPUT_RES)

def pick_new_color():
    return next(color_iter)

def dfs(street, all_streets, current_color):
    if not street.color:
        street.color = current_color

        neighbors = check_neighbors(street, all_streets)
        if not neighbors:
            return
        
        for neighbor in neighbors:
            
            dfs(neighbor, all_streets, current_color)
            
def check_neighbors(target_street, all_streets):
    neighbors = []
    target_points = target_street.shape.points
    if not target_points:
        return
    start_point = target_points[0]
    end_point = target_points[-1]

    for street in all_streets:
        if street is not target_street: 
            street_points = street.shape.points
            if not street_points:
                continue
            street_start = street_points[0]
            street_end = street_points[-1]

            if start_point == street_start or start_point == street_end or \
               end_point == street_start or end_point == street_end:
                neighbors.append(street)

    return neighbors

def compute_angle(self, neighbor):
    vec1 = ()
    vec2 = ()
    return angle_between(vec1, vec2)

def angle_between(v1, v2):
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    cos_angle = dot_product / (mag_v1 * mag_v2)
    angle = math.degrees(math.acos(max(min(cos_angle, 1), -1)))
    angle = abs(180-angle)
    print(angle)
    return angle

def main():
    pick_new_color()
    all_streets = read_shp(INPUT_PATH)

    for street in all_streets:
        if not street.color:
            current_color = pick_new_color()
            dfs(street, all_streets, current_color)

    plot(all_streets)

if __name__ == "__main__":
    main()