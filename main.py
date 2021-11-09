from screencap.Screen import Screen
from patternmatching.patmatch import PatternMatcher
from pokeapi.api import Pokemon
from roi.roi import ROI
from utils import logger
from actions.read import GetFixturedROI, EndFilter
import cv2
from ocr.ocr import FireRedNameReader
import numpy as np


log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG)


class PokeDex:
    def __init__(self, screen_dims):
        self.screen = Screen(*screen_dims)
        if log.level <= logger.DEBUG_WITH_IMAGES:
            self.screen.showScreen(scale=0.5, duration=0)
            cv2.destroyAllWindows()
        self.name_reader = FireRedNameReader()
        self.cached_pokemon = {}

        switchin_pattern = r"C:\Users\Victor\Documents\OCRPokedex\patterns\pokemonswitchin.png"
        switchinPokemonMatcher = PatternMatcher(switchin_pattern)
        switchin_roi = ROI(0, 0, 0.25 * self.screen.width, 0.07 * self.screen.height,
                           offsetX=0.1*self.screen.width, offsetY=-0.025*self.screen.height)
        switchin_matcher = GetFixturedROI(switchinPokemonMatcher, switchin_roi, n_matches=1,
                                      name_reader=self.name_reader)

        hp_pattern = r"C:\Users\Victor\Documents\OCRPokedex\patterns\HP.PNG"
        activePokemonMatcher = PatternMatcher(hp_pattern)
        hp_roi = ROI(0, 0, 0.2 * self.screen.width, 0.07 * self.screen.height,
                         offsetX=-0.08*self.screen.width, offsetY=-0.09*self.screen.height)
        active_matcher = GetFixturedROI(activePokemonMatcher, hp_roi, n_matches=2,
                                        name_reader=self.name_reader)

        self.matcher = None
        for action in [switchin_matcher, active_matcher][::-1]:
            if self.matcher is None:
                self.matcher = EndFilter()
            action.setSuccessor(self.matcher)
            self.matcher = action


    def read_pokemon_names(self):
        self.screen.updateScreen()
        pokemon_names, debug_images = self.matcher.read(self.screen.getScreen())
        print("-" * 50)
        for pokemon_name in pokemon_names:
            if pokemon_name not in self.cached_pokemon:
                self.cached_pokemon[pokemon_name] = Pokemon(pokemon_name)
            pokemon = self.cached_pokemon[pokemon_name]
            print(pokemon, "\n")

        if len(debug_images) > 0:
            cv2.imshow("images read", np.vstack(debug_images))
            cv2.waitKey()


def main():
    screen_dims = (0, 0, 2560, 1440)
    pokedex = PokeDex(screen_dims)
    while True:
        pokedex.read_pokemon_names()


if __name__ == '__main__':
    main()

