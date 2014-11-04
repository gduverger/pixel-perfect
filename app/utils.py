import os
import json
import base64
import requests

from PIL import Image, ImageChops, ImageOps
from io import BytesIO

from project import settings

from app import forms as app_forms
from app import models as app_models


BROWSERS = [
    {
        "os": "OS X",
        "os_version": "Lion",
        "browser": "chrome",
        "browser_version": "14.0"
    }, {
        "os": "Windows",
        "os_version": "7",
        "browser_version": "11.0",
        "browser": "ie"
    }
]


def get_headers():
    return {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': base64.b64encode(str.encode('%s:%s' % (settings.BROWSERSTACK_USERNAME, settings.BROWSERSTACK_PASSWORD))),
        #'Accept': 'application/json',
        #'Content-Length': 1
    }


def get_json_response(request):
    if request.status_code == requests.codes.ok:
        try:
            return request.json()
        except Exception as e:
            # TODO ValueError
            return None


def request_screenshots(test):
    data = {
        "url": test.url,
        "callback_url": settings.BROWSERSTACK_CALLBACK_URL,
        "win_res": "1280x1024",
        "mac_res": "1280x1024",
        "quality": "compressed",
        "wait_time": 5,
        "orientation": "portrait",
        "browsers": BROWSERS
    }

    request = requests.post(settings.BROWSERSTACK_URL, data=json.dumps(data), headers=get_headers())
    json_response = get_json_response(request)

    if json_response:
        test.browserstack_job_id = json_response.get('job_id')
        test.save()
        for screenshot in json_response.get('screenshots'):
            app_models.Screenshot.objects.get_or_create(browserstack_screenshot_id=screenshot.get('id'), defaults={'test': test})


def get_screenshots(test):
    url = '%s/%s.json' % (settings.BROWSERSTACK_URL, test.browserstack_job_id)
    request = requests.get(url)
    json_response = get_json_response(request)

    if json_response and json_response.get('state') == 'done':
        for s in json_response.get('screenshots'):
            if s.get('state') == 'done':

                screenshot, _ = app_models.Screenshot.objects.get_or_create(browserstack_screenshot_id=s.get('id'))
                screenshot.test = test
                screenshot.browserstack_screenshot_image_url = s.get('image_url')
                screenshot.browserstack_screenshot_os = s.get('os')
                screenshot.browserstack_screenshot_os_version = s.get('os_version')
                screenshot.browserstack_screenshot_browser = s.get('browser')
                screenshot.browserstack_screenshot_browser_version = s.get('browser_version')
                screenshot.save()

                image = flat_image(get_image(screenshot.browserstack_screenshot_image_url))
                save_image(image, settings.MEDIA_ROOT_SCREENSHOTS, screenshot.browserstack_screenshot_id)
                diff = diff_images(Image.open(test.mock.path), image)
                save_image(diff, settings.MEDIA_ROOT_DIFFS, screenshot.browserstack_screenshot_id)


def get_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def flat_image(image):
    image.load()
    _image = Image.new("RGB", image.size, (255, 255, 255))
    try:
        _image.paste(image, mask=image.split()[3]) # 3 is the alpha channel
    except IndexError as e:
        _image.paste(image)
    return _image


def save_image(image, path, name):
    image.save('%s/%s.png' % (path, name))


def diff_images(mock, screenshot):
    difference = ImageChops.difference(mock, screenshot)
    difference_invert = ImageChops.invert(difference)
    difference_invert_convert = difference_invert.convert('L')
    difference_invert_convert_colorize = ImageOps.colorize(difference_invert_convert, (255, 0, 255), (255, 255, 255))
    return ImageChops.darker(difference_invert_convert_colorize, mock)
