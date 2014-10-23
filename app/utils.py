import base64
import requests

from app import forms as app_forms
from app import models as app_models

try:
    import simplejson as json
except ImportError:
    import json


BROWSERSTACK_USERNAME = 'gduverger'
BROWSERSTACK_PASSWORD = 'mHKhd7NvNgdJ8EoKxARp'
#BROWSERSTACK_AUTHORIZATION = 'Z2R1dmVyZ2VyOm1IS2hkN052TmdkSjhFb0t4QVJw'
BROWSERSTACK_URL = 'http://www.browserstack.com/screenshots'
BROWSERSTACK_CALLBACK_URL = 'http://0.0.0.0:5000/callback'

BROWSERS = [
    {
        #"device": null,
        "os": "OS X",
        "browser_version": "14.0",
        "os_version": "Lion",
        "browser": "chrome"
    }, {
        #"device": null,
        "os": "Windows",
        "browser_version": "11.0",
        "os_version": "7",
        "browser": "ie"
    }
]


def get_headers():
    return {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': base64.b64encode(str.encode('%s:%s' % (BROWSERSTACK_USERNAME, BROWSERSTACK_PASSWORD))),
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


def get_screenshots(test):
    url = '%s/%s.json' % (BROWSERSTACK_URL, test.browserstack_job_id)
    request = requests.get(url)
    json_response = get_json_response(request)
    if json_response and json_response.get('state') == 'done':
        for screenshot in json_response.get('screenshots'):
            if screenshot.get('state') == 'done':
                s, _ = app_models.Screenshot.objects.get_or_create(browserstack_screenshot_id=screenshot.get('id'))
                s.test = test
                s.browserstack_screenshot_thumb_url = screenshot.get('thumb_url')
                s.browserstack_screenshot_image_url = screenshot.get('image_url')
                s.save()


def request_screenshots(test):

    data = {
        "url": test.link,
        "callback_url": BROWSERSTACK_CALLBACK_URL,
        "win_res": "1024x768",
        "mac_res": "1920x1080",
        "quality": "compressed",
        "wait_time": 5,
        "orientation": "portrait",
        "browsers": BROWSERS
    }

    request = requests.post(BROWSERSTACK_URL, data=json.dumps(data), headers=get_headers())
    json_response = get_json_response(request)

    if json_response:
        test.browserstack_job_id = json_response.get('job_id')
        test.save()
        for screenshot in json_response.get('screenshots'):
            app_models.Screenshot.objects.get_or_create(browserstack_screenshot_id=screenshot.get('id'), defaults={'test': test})
