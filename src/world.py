import json
import pygame as pg

class Country:
    def __init__(self, name:str, code:str, continent:str, coords:list) -> None:
        self.name = name
        self.code = code
        self.continent = continent
        self.coords = coords

        print(name)

    def draw(self, screen:pg.Surface, map_size:list, map_shift:pg.Vector2, map_zoom:int) -> None:
        pg.draw.polygon(
            screen,
            (0, 0, 0),
            [((map_size[0] / 2) + (x * map_zoom - map_shift.x), (map_size[1] / 2) - (y * map_zoom - map_shift.y)) for x, y in self.coords],
            1
        )


class World:
    MAP_SIZE = (1280, 720)

    # Praha is the middle of the map
    MAP_MID_COORDS = pg.Vector2(14.421389, 50.0875)
    MAP_MINMAX_ZOOM = (10, 70)

    def __init__(self) -> None:
        self.read_geo_data()
        self.map_shift = pg.Vector2(0, 0)
        self.map_zoom = (self.MAP_MINMAX_ZOOM[1] - self.MAP_MINMAX_ZOOM[0]) / 2
        self.countries = self.create_countries()

    def read_geo_data(self) -> None:
        with open('data/countries.json', 'r') as f:
            self.geo_data = json.load(f)

    def create_countries(self) -> dict:
        countries = {}
        for name, country in self.geo_data.items():
            xy_coords = []
            for coord in country['coordinates']:
                x = coord[0] - self.MAP_MID_COORDS.x
                y = coord[1] - self.MAP_MID_COORDS.y
                xy_coords.append(pg.Vector2(x, y))

            countries[name] = Country(name, country['code'], country['continent'], xy_coords)
        return countries

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

    def update(self) -> None:
        pass
