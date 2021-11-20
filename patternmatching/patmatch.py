import cv2
from screencap.Screen import Screen
from utils import logger
from patternmatching import sift


log = logger.get_logger(__name__)
log.setLevel(logger.INFO)

STRATEGIES = {
    "sift": sift.SIFTMatcher,
}

class PatternMatcher:
    def __init__(self, path_to_pattern, strategy: str= "sift"):
        '''
        :param screen_dimensions: (tuple / list) cornerX, cornerY, width, height
        :param strategy: (string) the pattern matching algorithm to use
        '''
        self.load_pattern(path_to_pattern)
        self.strategy = STRATEGIES[strategy.lower()]()

    def find_pattern(self, query, n_matches=1):
        if self.pattern is None:
            raise ValueError("Pattern is None. Likely because it has not been loaded yet.")
        matched_patterns = self.strategy.find_matches(query, self.pattern, n_matches=n_matches)
        return matched_patterns

    def load_pattern(self, path_to_pattern):
        log.debug(f"Reading pattern: {path_to_pattern}")
        self.pattern = cv2.imread(path_to_pattern, 1)
        if self.pattern is None:
            raise FileNotFoundError(f"Could not load file {path_to_pattern}")
        if log.level <= logger.DEBUG_WITH_IMAGES:
            cv2.imshow("loaded pattern", self.pattern)
            cv2.waitKey(0)


if __name__ == "__main__":
    from roi.roi import ROI
    log.setLevel(logger.DEBUG)
    sift.log.setLevel(logger.DEBUG_WITH_IMAGES)
    screen_dims = (0, 0, 2560, 1440)
    screen = Screen(*screen_dims)
    path_to_pattern = r"C:\Users\Victor\Documents\OCRPokedex\patterns\pokemonswitchin.png"
    # path_to_pattern = r"C:\Users\Victor\Documents\OCRPokedex\patterns\HP.PNG"
    patmatch = PatternMatcher(path_to_pattern)
    if log.level <= logger.DEBUG_WITH_IMAGES:
        screen.showScreen(scale=0.5)
    screen.updateScreen()
    switchin_input_roi = ROI(0, (1 -  (129 / 1440) - 0.05) * screen.height,
                             screen.width, 129 / 1440 * screen.height)
    hp_input_roi = ROI(0, 0, screen.width, (1007 / 1440) * screen.height)
    locations = patmatch.find_pattern(switchin_input_roi.getROI(screen.getScreen()), n_matches=1)
    print(locations)
    cv2.waitKey(0)