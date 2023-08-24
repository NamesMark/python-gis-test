import shapefile
import matplotlib.pyplot as plt
import random
import math

from styles import COLORS, STYLES
from itertools import cycle

OUTPUT_SIZE = 3000
OUTPUT_RES = 300
MAX_ANGLE = 45

INPUT_PATH = 'sample/roads.shp'
OUTPUT_PATH = 'output/solution.png'

VARIED_STYLES = True

color_iter = cycle(COLORS)
style_iter = cycle(STYLES)
    
class Street:
    def __init__(self, shape):
        self.shape = shape
        self.style = None

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
        ax.plot(x, y, color=street.style[0], dashes=street.style[1])
    print("SAVED FILE")
    plt.savefig(OUTPUT_PATH, dpi=OUTPUT_RES)

def pick_new_style():
    if VARIED_STYLES:
        return (next(color_iter), next(style_iter))
    return (next(color_iter), (None, None))

def get_vector_from_points(points):
    return (points[-1][0] - points[-2][0], points[-1][1] - points[-2][1])


def dfs_color(street, all_streets, current_style):
    if street.style:
        return
    
    street.style = current_style
    neighbors = check_neighbors(street, all_streets)
    if not neighbors:
        return
    if len(neighbors) == 1:
        dfs_color(neighbors[0], all_streets, current_style)
    else:
        target_points = street.shape.points
        target_vector = get_vector_from_points(target_points)

        for neighbor in neighbors:
            neighbor_points = neighbor.shape.points
            neighbor_vector = get_vector_from_points(neighbor_points)

            angle = angle_between(target_vector, neighbor_vector)

            if angle <= MAX_ANGLE:
                dfs_color(neighbor, all_streets, current_style)
            
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

def angle_between(v1, v2):
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    if mag_v1 == 0 or mag_v2 == 0:
        return 0
    cos_angle = dot_product / (mag_v1 * mag_v2)
    angle = math.degrees(math.acos(max(min(cos_angle, 1), -1)))
    if angle>90+MAX_ANGLE:
        angle = abs(angle-180)
    #print(angle)
    return angle

def main():
    all_streets = read_shp(INPUT_PATH)

    for street in all_streets:
        if not street.style:
            current_style = pick_new_style()
            dfs_color(street, all_streets, current_style)

    plot(all_streets)

if __name__ == "__main__":
    main()