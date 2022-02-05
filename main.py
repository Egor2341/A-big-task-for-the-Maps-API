import os

import pygame
import requests

lon = "37.530887"
lat = "55.703118"
delta = "0.001"
running = True
screen = pygame.display.set_mode((600, 450))
'''0.02, 0.03, 0.05, 0.09, 0.18, 0.35, 0.7'''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if float(delta) * 2 < 90:
                    delta = str(float(delta) * 2)
            elif event.key == pygame.K_PAGEUP:
                if float(delta) / 2 >= 0.000125:
                    delta = str(float(delta) / 2)
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        os.remove(map_file)

pygame.quit()
