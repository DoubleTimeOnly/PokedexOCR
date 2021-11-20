from patternmatching.patmatch import PatternMatcher
from ocr.ocr import FireRedNameReader
from roi.roi import ROI
from utils import logger
import numpy as np
import cv2

log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG)


class ActionFilter:
    def __init__(self, matcher: PatternMatcher, output_roi: ROI,
                 n_matches: int, input_roi: ROI=None, name_reader: FireRedNameReader=None,
                 name="action filter"):
        self.input_roi = input_roi
        self.output_roi = output_roi
        self.n_matches = n_matches
        self.matcher = matcher
        self.name_reader = name_reader
        self.name = name
        if name_reader is None:
            self.name_reader = FireRedNameReader()

        self._successor = None

    def setSuccessor(self, newSuccessor):
        self._successor = newSuccessor

    def read(self, image):
        raise NotImplementedError


class GetFixturedROI(ActionFilter):
    def read(self, image):
        atLeastOneValidName = False
        pokemon_names = []
        debug_images = []
        if self.input_roi is not None:
            query_image = self.input_roi.getROI(image.copy())

        if log.level <= logger.DEBUG_WITH_IMAGES:
            cv2.imshow(f"{self.name} input images", query_image)
            cv2.waitKey(1)

        locations = self.matcher.find_pattern(query_image, n_matches=self.n_matches)
        for i, point in enumerate(locations):
            self.output_roi.x, self.output_roi.y = point
            name_img = self.output_roi.getROI(query_image)
            name = self.name_reader.read_pokemon_name(name_img, binarize=True)
            debug_images.append(name_img)
            if len(name) > 0:
                atLeastOneValidName = True
            pokemon_names.append(name)

        if len(debug_images) > 0 and log.level <= logger.DEBUG_WITH_IMAGES:
            cv2.imshow(f"{__name__} debug images", np.vstack(debug_images))
        if atLeastOneValidName:
            return pokemon_names, debug_images
        else:
            return self._successor.read(image)


class EndFilter(ActionFilter):
    def __init__(self):
        pass

    def read(self, image):
        print("Could not find any matches")
        return [], []
