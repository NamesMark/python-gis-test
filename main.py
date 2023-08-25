import geopandas as gpd
import matplotlib.pyplot as plt
import math
from styles import COLORS, STYLES
from itertools import cycle

OUTPUT_SIZE = 3000
OUTPUT_RES = 300
MAX_ANGLE = 33

INPUT_PATH = 'sample/roads.shp'
OUTPUT_PATH = 'output/solution.png'
VARIED_STYLES = False

color_iter = cycle(COLORS)
style_iter = cycle(STYLES)

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

    print("SAVED FILE")
    plt.savefig(OUTPUT_PATH, dpi=OUTPUT_RES)

def pick_new_style():
    if VARIED_STYLES:
        return (next(color_iter), next(style_iter))
    return (next(color_iter), (None, None))

def get_vector_from_points(points):
    p1, p2 = points[-2], points[-1]
    return (p2[0] - p1[0], p2[1] - p1[1])

def angle_between(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
    cos_angle = dot_product / (mag_v1 * mag_v2)
    angle = math.degrees(math.acos(max(min(cos_angle, 1), -1)))
    if angle > 90 + MAX_ANGLE:
        angle = abs(angle - 180)
    #print(angle)
    return angle

def dfs_color(row, geodataframe, current_style):
    if row['style']:
        print(f"Row {row.name} already has style: {row['style']}")
        return

    geodataframe.at[row.name, 'style'] = current_style
    print(f"Assigning style {current_style} to row {row.name}")
    
    neighbors = geodataframe[geodataframe.geometry.touches(row.geometry) & ~geodataframe.index.isin([row.name])]

    print(f"Row {row.name} has {len(neighbors)} neighbors.")

    if neighbors.empty:
        return

    if len(neighbors) == 1:
        if not neighbors.iloc[0].style:
            print(f"Recursively coloring single neighbor of row {row.name}.")
            dfs_color(neighbors.iloc[0], geodataframe, current_style)
    else:
        target_vector = get_vector_from_points(list(row.geometry.coords))

        for _, neighbor in neighbors.iterrows():
            neighbor_vector = get_vector_from_points(list(neighbor.geometry.coords))
            angle = angle_between(target_vector, neighbor_vector)
            print(f"Angle between row {row.name} and neighbor {neighbor.name} is {angle} degrees.")

            if angle <= MAX_ANGLE:
                if not neighbor.style:
                    print(f"Recursively coloring neighbor {neighbor.name} because angle {angle} is less than {MAX_ANGLE} degrees.")
                    dfs_color(neighbor, geodataframe, current_style)
                else:        
                    print(f"Not coloring neighbor {neighbor.name} because angle it was already visited.")
            else:
                print(f"Not coloring neighbor {neighbor.name} because angle {angle} is more than {MAX_ANGLE} degrees")

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