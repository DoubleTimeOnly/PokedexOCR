import pytesseract
from utils import logger

log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG)

LOWERCASE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class FireRedNameReader:
    def __init__(self):
        pass

    @staticmethod
    def read_pokemon_name(query_image):
        return pytesseract.image_to_string(query_image, lang='eng', config=f'--psm 8 -c tessedit_char_whitelist={LOWERCASE_ALPHABET.upper()}')