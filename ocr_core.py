import pytesseract
from PIL import Image
from PIL import ImageFilter

def process_image(image):
    image_cache = Image.open(image)
    image_cache.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image_cache, lang='eng+chi_sim+chi_tra')
