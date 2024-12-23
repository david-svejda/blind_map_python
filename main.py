import pygame as pg
import sys
from src.blind_map import BlindMapGame

pg.init()
pg.mixer.init()
pg.font.init()

WIDTH, HEIGHT = 1280, 720
window_size = pg.Vector2(WIDTH, HEIGHT)

screen = pg.display.set_mode(window_size)
clock = pg.time.Clock()

pg.display.set_caption("Slepá mapa")

blind_map = BlindMapGame(screen, clock, window_size)
blind_map.run()

pg.quit()
sys.exit()

