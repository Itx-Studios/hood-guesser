import random
import webbrowser
from shapely.geometry import Polygon, Point

# Points of the munich polygon
points = [
    (48.208008, 11.605111), (48.196182, 11.624471), (48.194353, 11.631883),
    (48.180712, 11.627659), (48.176503, 11.648172), (48.139742, 11.652056),
    (48.122286, 11.666725), (48.110429, 11.719189), (48.100785, 11.657304),
    (48.063318, 11.693028), (48.212721, 11.565294), (48.055677, 11.593203),
    (48.086642, 11.603002), (48.085278, 11.558499), (48.030019, 11.533594),
    (48.073822, 11.512568), (48.214564, 11.549712), (48.204278, 11.546143),
    (48.204138, 11.506807), (48.194939, 11.500610), (48.182511, 11.455205),
    (48.165304, 11.454247), (48.163313, 11.410021), (48.134725, 11.429184),
    (48.133120, 11.482959), (48.112126, 11.502463), (48.076273, 11.514995)
]

# Create polygon
polygon = Polygon(points)

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

def main():
    point = random_point_in_polygon(polygon)
    print(f"koordinaten: {point}")
    open_map(point.x, point.y)

if __name__ == "__main__":
    main()
