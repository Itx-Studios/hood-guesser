import random
import webbrowser
from shapely.geometry import Polygon, Point
import json
import os

def load_points(polygon_name):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "config.json"), "r") as file:
        config = json.loads(file)
        return config["polygons"][polygon_name]

# Get random point inside the polygon
def random_point_in_polygon(polygon: Polygon):
    min_x, min_y, max_x, max_y = polygon.bounds

    while True:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        
        if polygon.contains(random_point):
            return random_point

# Open google street view at the specified coordinates
def open_map(latitude, longitude):
    url = f'http://maps.google.com/maps?q=&layer=c&cbll={latitude},{longitude}'
    webbrowser.open(url) 

def open_in_polygon(polygon_name):
    points = load_points(polygon_name)
    polygon = Polygon(points)
    
    point = random_point_in_polygon(polygon)
    print(f"koordinaten: {point}")
    open_map(point.x, point.y)
