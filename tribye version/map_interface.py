import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

# HTML-Code für die OpenStreetMap mit Leaflet, zentriert auf München, inklusive eines permanenten roten Markers
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
    // Karte initialisieren, zentriert auf München
    var map = L.map('map').setView([48.1351, 11.5820], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Permanenter roter Marker an der Startposition (München)
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
        self.setWindowTitle("OSM Map mit permanentem roten Punkt")
        self.setGeometry(100, 100, 800, 600)
        
        # Zentrales Widget und Layout
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.setCentralWidget(self.container)
        
        # QWebEngineView zum Anzeigen der Karte
        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        
        # Button, um das aktuelle Kartenzentrum abzufragen und den Marker zu verschieben
        self.save_button = QPushButton("Koordinaten speichern")
        self.save_button.clicked.connect(self.save_center)
        
        # Widgets dem Layout hinzufügen
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.save_button)
    
    def save_center(self):
        # JavaScript-Code, um das Zentrum der Karte zu ermitteln
        js = "var center = map.getCenter(); [center.lat, center.lng];"
        self.browser.page().runJavaScript(js, self.handle_center)
    
    def handle_center(self, result):
        if result:
            lat, lng = result
            print("Zentrum Koordinaten:", lat, lng)
            # Den bestehenden Marker an die neue Position verschieben
            js_update_marker = f"window.savedMarker.setLatLng([{lat}, {lng}]);"
            self.browser.page().runJavaScript(js_update_marker)
        else:
            print("Fehler beim Abrufen der Koordinaten.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())