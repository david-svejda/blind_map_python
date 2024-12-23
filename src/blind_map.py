import pygame as pg
from src.world import World

class BlindMapGame:
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock, window_size: pg.Vector2) -> None:
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.playing = True
        self.world = World()

    def run(self) -> None:
        while self.playing:
            self.clock.tick(60)
            self.screen.fill((255, 255, 255))
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False

        self.world.events()

    def update(self) -> None:
        self.world.update()

    def draw(self) -> None:
        self.world.draw(self.screen)

