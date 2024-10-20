import pygame
import random
import webbrowser
import os

# Punkte für das Polygon
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

# Funktion, um einen zufälligen Punkt innerhalb des Polygons zu finden
def random_point_in_polygon(points):
    min_lat = min(p[0] for p in points)
    max_lat = max(p[0] for p in points)
    min_lon = min(p[1] for p in points)
    max_lon = max(p[1] for p in points)

    while True:
        random_lat = random.uniform(min_lat, max_lat)
        random_lon = random.uniform(min_lon, max_lon)
        random_point = (random_lat, random_lon)
        
        if point_in_polygon(random_point, points):
            return random_point

# Funktion zum Prüfen, ob ein Punkt in einem Polygon liegt (Ray-Casting Algorithmus)
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Pygame initialisieren
pygame.init()

# Lade das erste Bild als Hintergrund
image_path = os.path.join(os.path.dirname(__file__), "title_img.png")
background_image = pygame.image.load(image_path)

# Fenstergröße entsprechend der Bildgröße setzen
screen_width, screen_height = background_image.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Google Maps mit zufälligem Punkt im Polygon öffnen")

# Hauptschleife
running = True
in_lobby = False
click_area = pygame.Rect(238, 469, 523, 109)  # Klickbereich für Google Maps
play_area = pygame.Rect(231, 448, 523, 109)  # Bereich für „Spielen“

# Zufälligen Punkt initialisieren
random_lat, random_lon = random_point_in_polygon(points)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse clicked at: {mouse_pos}")  # Debugging-Ausgabe
            
            if not in_lobby:  # Wenn nicht in der Lobby
                if play_area.collidepoint(mouse_pos):
                    print("Clicked on the play area!")  # Debugging-Ausgabe
                    # Lade das Lobby-Bild
                    lobby_image_path = os.path.join(os.path.dirname(__file__), "lobby_img.png")
                    background_image = pygame.image.load(lobby_image_path)
                    in_lobby = True  # Wechsel in den Lobby-Modus
                else:
                    print("Clicked outside the play area.")  # Debugging-Ausgabe
            else:
                # Prüfen, ob der Klick im Bereich für Google Maps war
                if click_area.collidepoint(mouse_pos):
                    print("Opening Google Maps...")  # Debugging-Ausgabe
                    # Berechne einen neuen Punkt im Polygon
                    random_lat, random_lon = random_point_in_polygon(points)
                    # Öffne Google Maps mit dem neuen Punkt
                    url = f"https://www.google.com/maps?q=&layer=c&cbll={random_lat},{random_lon}"
                    webbrowser.open(url)
                    
                    # Wechsle zu einem neuen Bild (re_img)
                    re_image_path = os.path.join(os.path.dirname(__file__), "re_img.png")
                    background_image = pygame.image.load(re_image_path)

                    # Aktualisiere das Fenster und zeige das neue Bild
                    screen.blit(background_image, (0, 0))
                    pygame.display.flip()

    # Zeichne das Hintergrundbild
    screen.blit(background_image, (0, 0))

    # Aktualisiere das Fenster
    pygame.display.flip()

# Beende Pygame
pygame.quit()