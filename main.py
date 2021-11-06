from screencap.Screen import Screen
from patternmatching.patmatch import PatternMatcher
from roi.roi import ROI
from utils import logger
import cv2
from ocr.ocr import FireRedNameReader


log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG_WITH_IMAGES)

class PokeDex:
    def __init__(self, screen_dims):
        self.screen = Screen(*screen_dims)
        self.matcher = PatternMatcher()
        # if log.level <= logger.DEBUG_WITH_IMAGES:
        #     self.screen.showScreen(scale=0.5)
        self.roi = ROI(0, 0, 0.2*self.screen.width, 0.07*self.screen.height,
                       offsetX=-0.08*self.screen.width, offsetY=-0.09*self.screen.height)

    def load_pattern(self, pattern_path):
        self.matcher.load_pattern(pattern_path)

    def read_pokemon_names(self):
        self.screen.updateScreen()
        locations = self.matcher.find_pattern(self.screen.getScreen(), n_matches=2)
        for i, point in enumerate(locations):
            self.roi.x = point[0]
            self.roi.y = point[1]
            name_img = self.roi.getROI(self.screen.getScreen())
            gray_name_img = cv2.cvtColor(name_img, cv2.COLOR_BGR2GRAY)
            t, binarized_img = cv2.threshold(gray_name_img, 100, 255, cv2.THRESH_BINARY)
            print(FireRedNameReader.read_pokemon_name(binarized_img))
            cv2.imshow(f"name{i}", binarized_img)
            cv2.waitKey(1)


def main():
    screen_dims = (0, 0, 2560, 1440)
    pattern_path = r"C:\Users\Victor\Documents\OCRPokedex\patterns\HP.PNG"
    pokedex = PokeDex(screen_dims)
    pokedex.load_pattern(pattern_path)
    while True:
        pokedex.read_pokemon_names()


if __name__ == '__main__':
    main()

