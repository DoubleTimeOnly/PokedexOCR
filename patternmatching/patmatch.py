import cv2
from screencap.Screen import Screen
from utils import logger
from patternmatching import sift


log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG)

STRATEGIES = {
    "sift": sift.SIFTMatcher,
}

class PatternMatcher:
    def __init__(self, strategy: str="sift"):
        '''
        :param screen_dimensions: (tuple / list) cornerX, cornerY, width, height
        :param strategy: (string) the pattern matching algorithm to use
        '''
        self.pattern = None
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
    screen_dims = (0, 0, 2560, 1440)
    screen = Screen(*screen_dims)
    patmatch = PatternMatcher()
    if log.level <= logger.DEBUG_WITH_IMAGES:
        screen.showScreen(scale=0.5)
    patmatch.load_pattern(r"C:\Users\Victor\Documents\OCRPokedex\patterns\HP.PNG")
    screen.updateScreen()
    locations = patmatch.find_pattern(screen.getScreen(), n_matches=2)
    print(locations)
    assert len(locations) == 2