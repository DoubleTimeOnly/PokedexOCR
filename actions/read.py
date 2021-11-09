from patternmatching.patmatch import PatternMatcher
from ocr.ocr import FireRedNameReader
from roi.roi import ROI
import cv2
import numpy as np


class ActionFilter:
    def __init__(self, matcher: PatternMatcher, roi: ROI, n_matches: int, name_reader: FireRedNameReader=None):
        self.roi = roi
        self.n_matches = n_matches
        self.matcher = matcher
        self.name_reader = name_reader
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
        locations = self.matcher.find_pattern(image, n_matches=self.n_matches)
        for i, point in enumerate(locations):
            self.roi.x, self.roi.y = point
            name_img = self.roi.getROI(image)
            name = self.name_reader.read_pokemon_name(name_img, binarize=True)
            debug_images.append(name_img)
            if len(name) > 0:
                atLeastOneValidName = True
            pokemon_names.append(name)

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
