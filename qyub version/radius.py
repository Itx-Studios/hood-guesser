import random
import math
import webbrowser

CENTER = (48.1374179, 11.5754723)
RADIUS = 0.07

def random_point_in_circle(center, radius):
    theta = random.uniform(0, 2 * math.pi)
    
    r = radius * math.sqrt(random.uniform(0, 1))
    
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.sin(theta)
    
    return (x, y)

def open_map(latitude, longitude):
    url = f'http://maps.google.com/maps?q=&layer=c&cbll={latitude},{longitude}'
    webbrowser.open(url) 

def open_in_radius():
    point = random_point_in_circle(CENTER, RADIUS)
    open_map(point[0], point[1])
