import pygame
import math
import webbrowser

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

center_lat = sum([p[0] for p in points]) / len(points)
center_lon = sum([p[1] for p in points]) / len(points)

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Google Maps Koordinaten Öffnen")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            url = f"https://www.google.com/maps?q=&layer=c&cbll={center_lat},{center_lon}"
            webbrowser.open(url)
            running = False  

    screen.fill((255, 255, 255))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Klicke hier, um Google Maps zu öffnen", True, (0, 0, 0))
    screen.blit(text, (50, screen_height // 2 - 18))

    pygame.display.flip()

pygame.quit()