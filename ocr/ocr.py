import pytesseract
from utils import logger
import difflib
import os
import cv2

log = logger.get_logger(__name__)
log.setLevel(logger.INFO)

LOWERCASE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def binarizeImage(image, threshold, invert=False):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    t, binarized_img = cv2.threshold(gray_image, threshold, 255, threshold_type)
    return binarized_img


class FireRedNameReader:
    def __init__(self):
        self.name_index = self.load_pokemon_names()

    @staticmethod
    def load_pokemon_names(name_file=["PokemonNamesGens1-8.txt", "fakemon.txt"]):
        if isinstance(name_file, str):
            log.debug(f"Loading name file: {os.path.abspath(name_file)}")
            name_file = [name_file]

        name_index = []
        for filename in name_file:
            filename = os.path.join("database", filename)
            with open(filename, 'r') as file:
                name_index.extend([line.strip() for line in file])
        return name_index

    def read_pokemon_name(self, query_image, binarize=False):
        if binarize:
            query_image = binarizeImage(query_image, threshold=100)

        if log.level <= logger.DEBUG_WITH_IMAGES:
            cv2.imshow("image to read", query_image)
            cv2.waitKey()
        char_whitelist = f"{LOWERCASE_ALPHABET.upper()}{LOWERCASE_ALPHABET}- "
        raw_name = pytesseract.image_to_string(query_image, lang='eng', config=f'--psm 8')   # -c tessedit_char_whitelist={char_whitelist}')
        log.debug(f"Raw name: {raw_name}")
        matches = difflib.get_close_matches(raw_name.lower(), self.name_index, 1)
        if len(matches) != 0:
            return matches[0]
        else:
            return ""