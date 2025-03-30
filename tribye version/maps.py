import sys
import threading
import pygame
import random
import webbrowser
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
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

# Gemeinsame Variable zur Speicherung des zuletzt ermittelten Punkts
shared_coords = None

# ---------------------------
# Pygame-Anwendung
# ---------------------------
def run_pygame():
    global shared_coords
    pygame.init()

    # Titelbild laden
    base_path = os.path.dirname(__file__)
    title_image_path = os.path.join(base_path, "title_img.png")
    background_image = pygame.image.load(title_image_path)

    # Fenstergröße an Bildgröße anpassen
    screen_width, screen_height = background_image.get_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Google Maps mit zufälligem Punkt im Polygon öffnen")

    running = True
    in_lobby = False
    # Definierte Klickbereiche (Koordinaten und Größe anpassen, falls erforderlich)
    click_area = pygame.Rect(238, 469, 523, 109)  # Bereich für Google Maps
    play_area = pygame.Rect(231, 448, 523, 109)   # Bereich für „Spielen“

    # Initialen zufälligen Punkt ermitteln (wird später aktualisiert)
    shared_coords = random_point_in_polygon(points)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at: {mouse_pos}")  # Debug-Ausgabe

                if not in_lobby:
                    if play_area.collidepoint(mouse_pos):
                        print("Clicked on the play area!")
                        # Lobby-Bild laden
                        lobby_image_path = os.path.join(base_path, "lobby_img.png")
                        background_image = pygame.image.load(lobby_image_path)
                        in_lobby = True
                    else:
                        print("Clicked outside the play area.")
                else:
                    if click_area.collidepoint(mouse_pos):
                        print("Opening Google Maps...")
                        # Neuen zufälligen Punkt im Polygon berechnen
                        shared_coords = random_point_in_polygon(points)
                        random_lat, random_lon = shared_coords
                        # Google Maps mit dem neuen Punkt öffnen
                        url = f"https://www.google.com/maps?q=&layer=c&cbll={random_lat},{random_lon}"
                        webbrowser.open(url)
                        # Neues Bild (re_img) laden
                        re_image_path = os.path.join(base_path, "re_img.png")
                        background_image = pygame.image.load(re_image_path)
                        # Fenster aktualisieren
                        screen.blit(background_image, (0, 0))
                        pygame.display.flip()

        # Hintergrundbild zeichnen und Fenster aktualisieren
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

    pygame.quit()

# ---------------------------
# PyQt-Anwendung: OSM Map mit Button zum Speichern der Koordinaten
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
  </style>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
  <div id="map"></div>
  <script>
    // Karte wird initial auf München zentriert
    var map = L.map('map').setView([48.1351, 11.5820], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Permanenter roter Marker (Startposition: München)
    window.savedMarker = L.circleMarker([48.1351, 11.5820], {
      color: 'red',
      fillColor: 'red',
      fillOpacity: 1,
      radius: 5
    }).addTo(map);
  </script>
</body>
</html>
"""

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSM Map mit Koordinatenspeicherung")
        self.setGeometry(100, 100, 2000, 1600)

        # Container und Layout
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.setCentralWidget(self.container)

        # QWebEngineView zur Anzeige der Karte
        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        
        # Button zum Abfragen des Kartenmittelpunkts und Platzieren eines roten Punktes
        self.save_button = QPushButton("Koordinaten speichern")
        self.save_button.clicked.connect(self.save_center)

        # Hinzufügen der Widgets zum Layout
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.save_button)
    
    def save_center(self):
        # JavaScript-Code, um das aktuelle Zentrum der Karte abzurufen
        js = "var center = map.getCenter(); [center.lat, center.lng];"
        self.browser.page().runJavaScript(js, self.handle_center)
    
    def handle_center(self, result):
        if result:
            lat, lng = result
            print("Zentrum Koordinaten:", lat, lng)
            # Marker (roter Punkt) an der neuen Position platzieren bzw. verschieben
            js_add_marker = f"""
            if (window.savedMarker) {{
                map.removeLayer(window.savedMarker);
            }}
            window.savedMarker = L.circleMarker([{lat}, {lng}], {{
                color: 'red',
                fillColor: 'red',
                fillOpacity: 1,
                radius: 5
            }}).addTo(map);
            """
            self.browser.page().runJavaScript(js_add_marker)
        else:
            print("Fehler beim Abrufen der Koordinaten.")

# ---------------------------
# Main: Starten der PyQt-Anwendung und des Pygame-Threads
# ---------------------------
if __name__ == '__main__':
    # PyQt-Anwendung starten (muss im Hauptthread laufen)
    app = QApplication(sys.argv)
    map_window = MapWindow()
    map_window.show()

    # Pygame in einem separaten Thread starten
    pygame_thread = threading.Thread(target=run_pygame, daemon=True)
    pygame_thread.start()

    sys.exit(app.exec_())