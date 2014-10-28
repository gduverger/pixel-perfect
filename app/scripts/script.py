#!/usr/bin/python

import sys, os
import requests

from PIL import Image, ImageChops, ImageOps
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main(argv):
    mock = Image.open(os.path.join(BASE_DIR, 'mock.png'))
    #mock_response = requests.get('http://upload.wikimedia.org/wikipedia/commons/thumb/1/11/EBay_former_logo.svg/306px-EBay_former_logo.svg.png')
    #mock = Image.open(BytesIO(mock_response.content))
    mock = flat(mock)
    mock.save(os.path.join(BASE_DIR, 'mock.rgb.png'))
    print(mock)

    shot = Image.open(os.path.join(BASE_DIR, 'shot.png'))
    #shot_request = requests.get('http://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/318px-EBay_logo.svg.png')
    #shot = Image.open(BytesIO(shot_request.content))
    shot = flat(shot)
    shot.save(os.path.join(BASE_DIR, 'shot.rgb.png'))
    print(shot)

    """
    ImageChops.darker(mock, shot).save(os.path.join(BASE_DIR, 'darker.png'))
    ImageChops.lighter(mock, shot).save(os.path.join(BASE_DIR, 'lighter.png'))
    #ImageChops.logical_and(mock, shot).save(os.path.join(BASE_DIR, 'logical_and.png'))
    #ImageChops.logical_or(mock, shot).save(os.path.join(BASE_DIR, 'logical_or.png'))
    ImageChops.multiply(mock, shot).save(os.path.join(BASE_DIR, 'multiply.png'))
    ImageChops.screen(mock, shot).save(os.path.join(BASE_DIR, 'screen.png'))
    subtract = ImageChops.subtract(mock, shot)
    subtract.save(os.path.join(BASE_DIR, 'subtract.png'))
    ImageChops.invert(subtract).save(os.path.join(BASE_DIR, 'subtract-invert.png'))
    """

    difference = ImageChops.difference(mock, shot)
    difference.save(os.path.join(BASE_DIR, 'difference.rgb.png'))
    difference_invert = ImageChops.invert(difference)
    difference_invert.save(os.path.join(BASE_DIR, 'difference-invert.rgb.png'))
    difference_invert_convert = difference_invert.convert('L')
    difference_invert_convert_colorize = ImageOps.colorize(difference_invert_convert, (255, 0, 255), (255, 255, 255))
    difference_invert_convert_colorize.save(os.path.join(BASE_DIR, 'difference_invert_convert_colorize.rgb.png'))
    ImageChops.darker(difference_invert_convert_colorize, mock).save(os.path.join(BASE_DIR, 'difference_invert_convert_colorize_darker.rgb.png'))

    print("DONE!")

def flat(image):
    image.load()
    flat_image = Image.new("RGB", image.size, (255, 255, 255))
    try:
        flat_image.paste(image, mask=image.split()[3]) # 3 is the alpha channel
    except IndexError as e:
        flat_image.paste(image)
    return flat_image

if __name__ == "__main__":
    main(sys.argv[1:])
