import json
import os.path

import pygame as pg
from shapely.geometry import Point, Polygon

class Country:
    def __init__(self, name:str, code:str, continent:str, coords:list) -> None:
        self.name = name
        self.code = code
        self.continent = continent
        self.coords = coords
        self.polygon = Polygon(self.coords)

    def draw(self, screen:pg.Surface, map_size:list, map_shift:pg.Vector2, map_zoom:int) -> None:
        pg.draw.polygon(
            screen,
            (0, 0, 0),
            [((map_size[0] / 2) + (x * map_zoom - map_shift.x), (map_size[1] / 2) - (y * map_zoom - map_shift.y)) for x, y in self.coords],
            1
        )

    def is_inside(self, position: pg.Vector2) -> bool:
        result = False
        self.polygon = Polygon(self.coords)
        if Point(position.x, position.y).within(self.polygon):
            result = True
        return result

class River:
    def __init__(self, name:str, coords:list) -> None:
        self.name = name
        self.coords = coords

    def draw(self, screen:pg.Surface, map_size:list, map_shift:pg.Vector2, map_zoom:int) -> None:
        pg.draw.lines(
            screen,
            (135, 206, 250),
            False,
            [((map_size[0] / 2) + (x * map_zoom - map_shift.x), (map_size[1] / 2) - (y * map_zoom - map_shift.y)) for x, y in self.coords],
            1
        )
        '''
        pg.draw.polygon(
            screen,
            (135, 206, 250),
            [((map_size[0] / 2) + (x * map_zoom - map_shift.x), (map_size[1] / 2) - (y * map_zoom - map_shift.y)) for x, y in self.coords],
            1
        )
        '''

class World:
    MAP_SIZE = (1280, 720)

    # Praha is the middle of the map
    MAP_MID_COORDS = pg.Vector2(14.421389, 50.0875)
    MAP_MINMAX_ZOOM = (5, 70)

    def __init__(self) -> None:
        self.selected_country = None
        self.last_hoovered_country = None
        self.geo_data = {}
        self.river_data = {}
        self.map_shift = pg.Vector2(0, 0)
        self.map_zoom = (self.MAP_MINMAX_ZOOM[1] - self.MAP_MINMAX_ZOOM[0]) / 2

        self.read_geo_data()

        self.countries = self.create_countries()
        self.rivers = self.create_rivers()

    def read_geo_data(self) -> None:
        if os.path.isfile('data/countries.json'):
            with open('data/countries.json', 'r') as f:
                self.geo_data = json.load(f)

        if os.path.isfile('data/rivers.json'):
            with open('data/rivers.json', 'r') as f:
                self.river_data = json.load(f)

    def create_countries(self) -> dict:
        countries = {}
        for name, country in self.geo_data.items():
            xy_coords = []
            for coord in country['coordinates']:
                x = coord[0] - self.MAP_MID_COORDS.x
                y = coord[1] - self.MAP_MID_COORDS.y
                xy_coords.append(pg.Vector2(x, y))

            countries[name] = Country(country['country'], country['country_code'], country['continent'], xy_coords)
        return countries

    def create_rivers(self) -> dict:
        rivers = {}
        for name, coords in self.river_data.items():
            xy_coords = []
            for coord in coords:
                x = coord[0] - self.MAP_MID_COORDS.x
                y = coord[1] - self.MAP_MID_COORDS.y
                xy_coords.append(pg.Vector2(x, y))

            rivers[name] = River(name, xy_coords)
        return rivers

    def events(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_LSHIFT]:
            if keys[pg.K_UP]:
                if self.map_zoom < self.MAP_MINMAX_ZOOM[1]:
                    self.map_zoom += 1
            if keys[pg.K_DOWN]:
                if self.map_zoom > self.MAP_MINMAX_ZOOM[0]:
                    self.map_zoom -= 1
        else:
            if keys[pg.K_LEFT]:
                self.map_shift.x += 2
            if keys[pg.K_RIGHT]:
                self.map_shift.x -= 2
            if keys[pg.K_UP]:
                self.map_shift.y += 2
            if keys[pg.K_DOWN]:
                self.map_shift.y -= 2
            if keys[pg.K_SPACE]:
                self.map_shift = pg.Vector2(0, 0)

    def draw(self, screen:pg.Surface) -> None:
        for country in self.countries.values():
            country.draw(screen, self.MAP_SIZE, self.map_shift, self.map_zoom)

        for river in self.rivers.values():
            river.draw(screen, self.MAP_SIZE, self.map_shift, self.map_zoom)

        text = ''
        if self.last_hoovered_country is not None:
            text = self.last_hoovered_country.name
        text_surface = pg.font.SysFont(None, 24).render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)
        screen.blit(
            text_surface,
            text_rect
        )

    def update(self, screen:pg.Surface) -> None:
        self.selected_country = None
        mouse_pos = pg.mouse.get_pos()
        for country in self.countries.values():
            if country.is_inside(
                pg.Vector2(
                    (mouse_pos[0] - self.MAP_SIZE[0] / 2 + self.map_shift.x) / self.map_zoom,
                    (mouse_pos[1] - self.MAP_SIZE[1] / 2 - self.map_shift.y) / (-self.map_zoom))
                ):
                self.selected_country = country
                break

        if self.selected_country is not None:
            if self.last_hoovered_country is None or self.last_hoovered_country.name != self.selected_country.name:
                if self.last_hoovered_country is not None:
                    #clean polygon of last_hoovered_country
                    pass
                self.last_hoovered_country = self.selected_country
                #highlight polygon of selected_country
                print(self.selected_country.name)
            else:
                pass
        else:
            if self.last_hoovered_country is not None:
                #clean polygon of last_hoovered_country
                pass
            self.last_hoovered_country = None