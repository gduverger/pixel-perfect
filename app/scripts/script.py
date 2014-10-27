#!/usr/bin/python

import sys, os

from PIL import Image, ImageChops

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main(argv):
    mock = Image.open(os.path.join(BASE_DIR, 'mock.png'))
    print(mock)

    shot = Image.open(os.path.join(BASE_DIR, 'shot.png'))
    print(shot)

    ImageChops.darker(mock, shot).save(os.path.join(BASE_DIR, 'darker.png'))
    ImageChops.difference(mock, shot).save(os.path.join(BASE_DIR, 'difference.png'))
    ImageChops.lighter(mock, shot).save(os.path.join(BASE_DIR, 'lighter.png'))
    ImageChops.logical_and(mock, shot).save(os.path.join(BASE_DIR, 'logical_and.png'))
    ImageChops.logical_or(mock, shot).save(os.path.join(BASE_DIR, 'logical_or.png'))
    ImageChops.multiply(mock, shot).save(os.path.join(BASE_DIR, 'multiply.png'))
    ImageChops.screen(mock, shot).save(os.path.join(BASE_DIR, 'screen.png'))
    ImageChops.subtract(mock, shot).save(os.path.join(BASE_DIR, 'screen.png'))

    print("DONE!")

if __name__ == "__main__":
    main(sys.argv[1:])
