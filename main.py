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

def read_shp(file_path):
    shp = shapefile.Reader(file_path)
    return shp.shapes()
    
def plot(streets):
    dimension = OUTPUT_SIZE/OUTPUT_RES
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
    
class Street:
    def __init__(self, shape):
        self.shape = shape
        start_point = Point(shape.points[0])
        end_point = Point(shape.points[-1])
        self.start_segment = Segment(self, start_point, Point(shape.points[1]))
        self.end_segment = Segment(self, end_point, Point(shape.points[-2]))
        start_point.add_segment(self.start_segment)
        end_point.add_segment(self.end_segment)
        
        self.color = None
        
class Segment:
    def __init__(self, street, start, end):
        self.street = street
        self.start_point = start
        self.end_point = end
        start.add_segment(self)
        end.add_segment(self)
        
        self.neighbors = []
        
    def add_neighbor(self, neighbor):
        angle = self.compute_angle(neighbor)
        self.neighbors.append((neighbor, angle))

    def compute_angle(self, neighbor):
        vec1 = (self.end_point.coordinates[0] - self.start_point.coordinates[0], 
                self.end_point.coordinates[1] - self.start_point.coordinates[1])
        vec2 = (neighbor.end_point.coordinates[0] - neighbor.start_point.coordinates[0], 
                neighbor.end_point.coordinates[1] - neighbor.start_point.coordinates[1])
        return angle_between(vec1, vec2)

class Point:
    def __init__(self, coordinates):
        self.segments = []
        self.coordinates = coordinates
        
    def add_segment(self, segment):
        if segment not in self.segments:
            self.segments.append(segment)

def angle_between(v1, v2):
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    cos_angle = dot_product / (mag_v1 * mag_v2)
    angle = math.degrees(math.acos(max(min(cos_angle, 1), -1)))
    angle = abs(180-angle)
    print(angle)
    return angle

def dfs_color(street, current_color, visited=set()):
    if street.color or street in visited:
        print(f"This street has a color or was visited before")
        return
    visited.add(street)
    
    if len(street.start_segment.neighbors) == 0 and len(street.end_segment.neighbors) == 0:
        street.color = current_color
        print(f"No neighbors found, coloring")
        return
    for neighbor, angle in street.start_segment.neighbors:
        if len(street.start_segment.neighbors) == 1 and not neighbor.street.color:
            dfs_color(neighbor.street, current_color)
        elif angle<MAX_ANGLE and not neighbor.street.color:
            dfs_color(neighbor.street, current_color)
        elif not neighbor.street.color:
            new_color = pick_new_color()
            dfs_color(neighbor.street, new_color)
            
    for neighbor, angle in street.end_segment.neighbors:
        if len(street.end_segment.neighbors) == 1 and not neighbor.street.color:
            dfs_color(neighbor.street, current_color)
        elif angle<MAX_ANGLE and not neighbor.street.color:
            dfs_color(neighbor.street, current_color)
        elif not neighbor.street.color:
            new_color = pick_new_color()
            dfs_color(neighbor.street, new_color)
        

shapes = read_shp(INPUT_PATH)

streets = []
crossroads = []

for shape in shapes:
    if shape.points:
        streets.append(Street(shape))
        crossroads.append(streets[-1].start_segment.start_point)
        crossroads.append(streets[-1].end_segment.end_point)

for i, crossroad in enumerate(crossroads):
    for j, potential_neighbor in enumerate(crossroads):
        if i != j and crossroad.coordinates == potential_neighbor.coordinates:
            for segment1 in crossroad.segments:
                for segment2 in potential_neighbor.segments:
                    if segment1 != segment2:
                        segment1.add_neighbor(segment2)
                        segment2.add_neighbor(segment1)

for street in streets:
    print(f"Trying a new street")
    current_color = pick_new_color()
    dfs_color(street, current_color)

plot(streets)