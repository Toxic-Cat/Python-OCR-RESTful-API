import pytesseract
from PIL import Image
from PIL import ImageFilter
from io import StringIO

def process_image(image):
    image_cache = Image.open(StringIO(image))
    image_cache.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image_cache)
