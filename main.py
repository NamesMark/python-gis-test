import math
import geopandas as gpd
import matplotlib.pyplot as plt
from random import choice
from itertools import cycle
from styles import COLORS, STYLES
from shapely.geometry import Point, LineString

OUTPUT_SIZE = 3000
OUTPUT_RES = 300
MAX_ANGLE = 50              # street continuation threshold 

INPUT_PATH = 'sample/roads.shp'
OUTPUT_PATH = 'output/solution_varied.png'
VARIED_STYLES = True

color_iter = cycle(COLORS)

def read_shp(file_path):
    return gpd.read_file(file_path)

def plot(geodataframe):
    dimension = OUTPUT_SIZE / OUTPUT_RES
    fig, ax = plt.subplots(figsize=(dimension, dimension))

    for _, row in geodataframe.iterrows():
        if row.geometry:
            style = row['style']
            x, y = row.geometry.xy
            ax.plot(x, y, color=style[0], dashes=style[1])

    print("✅ SAVED FILE")
    plt.savefig(OUTPUT_PATH, dpi=OUTPUT_RES)

def pick_new_style():
    if VARIED_STYLES:
        return (next(color_iter), choice(STYLES))
    return (next(color_iter), (None, None))

def angle_between(v1, v2):
    """Returns an angle between two vectors <= 90 degrees"""
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
    cos_angle = dot_product / (mag_v1 * mag_v2)
    angle = math.degrees(math.acos(max(min(cos_angle, 1), -1)))
    return min(angle,180-angle)

def dfs_color(row, geodataframe, current_style):
    """Recursively colors continuous streets"""
    if row['style']:
        return

    geodataframe.at[row.name, 'style'] = current_style
    
    # We treat start and end point of the current street separately to check the intersection angle with the correct segment
    start_point = Point(row.geometry.coords[0])
    end_point = Point(row.geometry.coords[-1])
    
    start_segment   = LineString([row.geometry.coords[0],   row.geometry.coords[1]])
    end_segment     = LineString([row.geometry.coords[-1],  row.geometry.coords[-2]])
    
    start_candidates = geodataframe.loc[
        geodataframe.geometry.intersects(start_point) & 
        ~geodataframe.index.isin([row.name])
    ]
    end_candidates = geodataframe.loc[
        geodataframe.geometry.intersects(end_point) & 
        ~geodataframe.index.isin([row.name])
    ]
    
    start_neighbor = identify_street_continuation(start_segment, start_candidates)
    end_neighbor = identify_street_continuation(end_segment, end_candidates)
    
    if start_neighbor is not None: 
        dfs_color(start_neighbor, geodataframe, current_style)
    if end_neighbor is not None:
        dfs_color(end_neighbor, geodataframe, current_style)
        
def identify_street_continuation(segment, neighbors):
    """
    Determine the best neighboring street segment to continue coloring.
    If there's only one neighbor, return it.
    If there are multiple (crossroads) - choose the smallest if it's also smaller than our MAX_ANGLE heuristic
    """
    if neighbors.empty:
        return None

    if len(neighbors) == 1:
        if neighbors.iloc[0].style:
            return None
        return neighbors.iloc[0]
    
    target_vector = (segment.coords[1][0] - segment.coords[0][0], 
                     segment.coords[1][1] - segment.coords[0][1])
    smallest_angle = float('inf')
    smallest_angle_neighbor = None
    
    for _, neighbor in neighbors.iterrows():
        # Check if we intersect the start of neighbor, otherwise consider that we intersect it's end
        if Point(neighbor.geometry.coords[0]).intersects(segment):
            neighbor_vector = (neighbor.geometry.coords[1][0]  - neighbor.geometry.coords[0][0], 
                               neighbor.geometry.coords[1][1]  - neighbor.geometry.coords[0][1])
        else:
            neighbor_vector = (neighbor.geometry.coords[-1][0] - neighbor.geometry.coords[-2][0], 
                               neighbor.geometry.coords[-1][1] - neighbor.geometry.coords[-2][1])

        angle = angle_between(target_vector, neighbor_vector)

        if angle < smallest_angle:
            smallest_angle_neighbor = neighbor
            smallest_angle = angle
            
    if smallest_angle <= MAX_ANGLE:
        return smallest_angle_neighbor
    else:
        return None

def main():
    geodataframe = read_shp(INPUT_PATH)
    geodataframe['style'] = None 

    for _, row in geodataframe.iterrows():
        if row.isna().all():
            continue

        if not geodataframe.loc[row.name, 'style']:
            current_style = pick_new_style()
            dfs_color(row, geodataframe, current_style)

    plot(geodataframe)

if __name__ == "__main__":
    main()