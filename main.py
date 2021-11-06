from screencap.Screen import Screen
from patternmatching.patmatch import PatternMatcher
from roi.roi import ROI
from utils import logger
import cv2


log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG_WITH_IMAGES)

class PokeDex:
    def __init__(self, screen_dims):
        self.screen = Screen(*screen_dims)
        self.matcher = PatternMatcher()
        # if log.level <= logger.DEBUG_WITH_IMAGES:
        #     self.screen.showScreen(scale=0.5)
        self.roi = ROI(0, 0, 0.2*self.screen.width, 0.1*self.screen.height, offsetX=-0.1*self.screen.width, offsetY=-0.12*self.screen.height)

    def load_pattern(self, pattern_path):
        self.matcher.load_pattern(pattern_path)

    def read_pokemon_names(self):
        self.screen.updateScreen()
        locations = self.matcher.find_pattern(self.screen.getScreen(), n_matches=2)
        for point in locations:
            self.roi.x = point[0]
            self.roi.y = point[1]
            name_img = self.roi.getROI(self.screen.getScreen())
            cv2.imshow("name", name_img)
            cv2.waitKey()



def main():
    screen_dims = (0, 0, 2560, 1440)
    pattern_path = r"C:\Users\Victor\Documents\OCRPokedex\patterns\HP.PNG"
    pokedex = PokeDex(screen_dims)
    pokedex.load_pattern(pattern_path)
    pokedex.read_pokemon_names()


if __name__ == '__main__':
    main()

