from PIL import Image
import numpy

def take_screenshot(device):
    image_file_name = 'screenshot.png'
    screenshot = device.screencap()

    with open(image_file_name, 'wb') as file:
        file.write(screenshot)

    return image_file_name


def is_black(r, g, b):
    return int(r) + int(g) + int(b) == 0


def transition_points(screenshot_file):
    image = Image.open(screenshot_file)
    image_data = numpy.array(image, dtype=numpy.uint8)

    # take only the r,g,b values and ignore alpha
    pixels = [pixel[:3] for pixel in image_data[2000]]

    gray = True
    piller_1_end_found = False
    piller_2_start_found = False
    piller_2_end_found = False
    transitions = []

    for idx, pixel in enumerate(pixels):
        # print(idx, pixel)
        # skipping initial gray area
        if is_black(*pixel):
            gray = False

        if not gray:
            if not is_black(*pixel) and not piller_1_end_found:
                transitions.append(idx)
                piller_1_end_found = True

            if is_black(*pixel) and piller_1_end_found and not piller_2_start_found:
                transitions.append(idx)
                piller_2_start_found = True

            if not is_black(*pixel) and piller_1_end_found and piller_2_start_found and not piller_2_end_found:
                transitions.append(idx)
                piller_2_end_found = True

    return transitions


def get_distance(transitions, coefficient=0.98):
    piller_1_end, piller_2_start, piller_2_end = transitions

    distance = (piller_2_start - piller_1_end) + (piller_2_end - piller_2_start) / 2
    adjusted_distance = distance * coefficient

    return distance, adjusted_distance