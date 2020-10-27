from ppadb.client import Client
import time

import utils

ADB_DEFAULT_HOST = '127.0.0.1'
ADB_DEFAULT_PORT = 5037
SLEEP_TIMEOUT = 2.5

adb = Client(host=ADB_DEFAULT_HOST, port=ADB_DEFAULT_PORT)
devices = adb.devices()

if len(devices) == 0:
    print('no devices attached')
    quit()

phone = devices[0]

while True:
    screenshot_file = utils.take_screenshot(phone)

    transitions = utils.transition_points(screenshot_file)

    distance, adjusted_distance = utils.get_distance(transitions, 0.96)

    print(distance, adjusted_distance)

    phone.shell(f'input touchscreen swipe 500 500 500 500 {int(adjusted_distance)}')

    time.sleep(SLEEP_TIMEOUT)
