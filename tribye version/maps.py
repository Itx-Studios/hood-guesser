import sys
import threading
import math
import pygame
import random
import webbrowser
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

# ---------------------------
# Gemeinsame Funktionalität: Zufälligen Punkt innerhalb eines Polygons ermitteln
# ---------------------------
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

def random_point_in_polygon(points):
    min_lat = min(p[0] for p in points)
    max_lat = max(p[0] for p in points)
    min_lon = min(p[1] for p in points)
    max_lon = max(p[1] for p in points)
    while True:
        random_lat = random.uniform(min_lat, max_lat)
        random_lon = random.uniform(min_lon, max_lon)
        if point_in_polygon((random_lat, random_lon), points):
            return random_lat, random_lon

# Funktion zur Berechnung der Entfernung (Haversine-Formel)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Erdradius in Kilometern
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Globale Variable zur Speicherung der "tatsächlichen" Koordinaten (Street View)
shared_coords = None

# ---------------------------
# Pygame-Anwendung
# ---------------------------
def run_pygame():
    global shared_coords
    pygame.init()
    clock = pygame.time.Clock()
    
    base_path = os.path.dirname(__file__)
    # Bilder einmal laden (zur Performance-Verbesserung)
    title_img = pygame.image.load(os.path.join(base_path, "title_img.png"))
    lobby_img = pygame.image.load(os.path.join(base_path, "lobby_img.png"))
    re_img = pygame.image.load(os.path.join(base_path, "re_img.png"))
    
    background_image = title_img
    screen_width, screen_height = background_image.get_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Google Maps mit zufälligem Punkt im Polygon öffnen")

    running = True
    in_lobby = False
    click_area = pygame.Rect(238, 469, 523, 109)  # Bereich für Google Maps/Street View
    play_area = pygame.Rect(231, 448, 523, 109)   # Bereich für „Spielen“

    # Initialen zufälligen Punkt ermitteln
    shared_coords = random_point_in_polygon(points)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"Pygame - Mouse clicked at: {mouse_pos}")

                if not in_lobby:
                    if play_area.collidepoint(mouse_pos):
                        print("Pygame - Play area clicked, wechsle in Lobby.")
                        background_image = lobby_img
                        in_lobby = True
                    else:
                        print("Pygame - Außerhalb des Play-Bereichs geklickt.")
                else:
                    if click_area.collidepoint(mouse_pos):
                        print("Pygame - Google Maps/Street View Bereich geklickt.")
                        # Neuen zufälligen Punkt berechnen und als tatsächliche Koordinate setzen
                        shared_coords = random_point_in_polygon(points)
                        random_lat, random_lon = shared_coords
                        url = f"https://www.google.com/maps?q=&layer=c&cbll={random_lat},{random_lon}"
                        webbrowser.open(url)
                        background_image = re_img
                        screen.blit(background_image, (0, 0))
                        pygame.display.flip()

        screen.blit(background_image, (0, 0))
        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()

# ---------------------------
# PyQt-Anwendung: OSM Map mit Button, der beim Klick den tatsächlichen Punkt (shared_coords) als grünen Marker anzeigt
# ---------------------------
html = """
<!DOCTYPE html>
<html>
<head>
  <title>OSM Map</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    html, body, #map {
      height: 100%;
      margin: 0;
      padding: 0;
    }
    /* Rotes Fadenkreuz in der Mitte */
    #crosshair {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 10px;
      height: 10px;
      background-color: red;
      border-radius: 50%;
      transform: translate(-50%, -50%);
      pointer-events: none;
      z-index: 1000;
    }
  </style>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
  <div id="map"></div>
  <div id="crosshair"></div>
  <script>
    // Karte initial auf München zentrieren
    var map = L.map('map').setView([48.1351, 11.5820], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);
  </script>
</body>
</html>
"""

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSM Map mit tatsächlichen Koordinaten")
        self.setGeometry(100, 100, 2000, 1600)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.setCentralWidget(self.container)

        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        
        # Button zum Anzeigen des tatsächlichen (Street View) Punkts als grünen Marker
        self.save_button = QPushButton("Tatsächliche Koordinaten anzeigen")
        self.save_button.clicked.connect(self.show_actual_point)

        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.save_button)
    
    def show_actual_point(self):
        global shared_coords
        if shared_coords is not None:
            actual_lat, actual_lon = shared_coords
            # Erstelle einen grünen Marker an den tatsächlichen Koordinaten
            js_update_marker = f"""
            if (window.actualMarker) {{
                map.removeLayer(window.actualMarker);
            }}
            window.actualMarker = L.circleMarker([{actual_lat}, {actual_lon}], {{
                color: 'green',
                fillColor: 'green',
                fillOpacity: 1,
                radius: 5
            }}).addTo(map);
            """
            self.browser.page().runJavaScript(js_update_marker)
            QMessageBox.information(self, "Tatsächliche Koordinaten", f"Tatsächliche Koordinaten: {actual_lat}, {actual_lon}")
        else:
            QMessageBox.warning(self, "Fehler", "Tatsächliche Koordinaten sind noch nicht verfügbar.")

# ---------------------------
# Main: Starte PyQt-Anwendung und Pygame-Thread
# ---------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_window = MapWindow()
    map_window.show()

    # Pygame-Anwendung in separatem Thread starten (als daemon)
    pygame_thread = threading.Thread(target=run_pygame, daemon=True)
    pygame_thread.start()

    sys.exit(app.exec_())