import pytesseract
import os
import time
from PIL import Image, ImageDraw

IMAGE_SIZE = 100
POINT_INTERVAL = 1000


def chunks_to_image(list: list):
    for i in range(0, len(list), POINT_INTERVAL):
        yield list[i:i + POINT_INTERVAL]


def get_standalized_points(points: list) -> list:
    x_points = []
    y_points = []
    standalized = []
    for index, point in enumerate(points):
        if len(point) != 2:
            raise Exception("invalid point", point)
        if index == 0:
            continue
        x_points.append(point[0])
        y_points.append(point[1])
    max_x: int = max(x_points)
    min_x: int = min(x_points)
    max_y: int = max(y_points)
    min_y: int = min(y_points)
    for index in range(len(x_points)):
        x_point = x_points[index]
        y_point = y_points[index]
        standalized.append(((x_point - min_x) * IMAGE_SIZE / float(max_x), (y_point - min_y) * IMAGE_SIZE / float(max_y)))
    return standalized


def endpoint(points: list):
    timestamp = time.time()
    outputdir = 'output/' + str(int(timestamp))
    os.makedirs(outputdir)
    if len(points) == 0:
        raise Exception("there is no point")
    standalized = get_standalized_points(points)
    print(standalized)
    print('num of generated images = ' + str(max([len(standalized) - POINT_INTERVAL, 1])))
    num_of_point = len(standalized)
    for index in range(num_of_point):
        im = Image.new('1', (IMAGE_SIZE, IMAGE_SIZE))
        draw = ImageDraw.Draw(im)
        image_points = standalized[index: index + POINT_INTERVAL]
        draw.line(image_points, 1)
        print(index)
        print(image_points)
        print(pytesseract.image_to_string(im, config='--psm 10 -c tessedit_char_whitelist=0123456789'))
        im.save(outputdir + '/' + str(index) + '.jpg')
        if len(image_points) < POINT_INTERVAL:
            break


FILENAME = './images/2.jpg'

# labview
# https://forums.ni.com/t5/LabVIEW-Caf%C3%A9/Python%E3%81%A8LabVIEW%E3%82%92%E7%B5%B1%E5%90%88%E3%81%97%E3%81%A6%E4%BD%BF%E3%81%8A%E3%81%86/td-p/3992449?profile.language=en

# to generate image file, use pillow

# about psm
# Page segmentation modes:
#  0    Orientation and script detection(OSD) only.
#  1    Automatic page segmentation with OSD.
#  2    Automatic page segmentation, but no OSD, or OCR.
#  3    Fully automatic page segmentation, but no OSD. (Default)
#  4    Assume a single column of text of variable sizes.
#  5    Assume a single uniform block of vertically aligned text.
#  6    Assume a single uniform block of text.
#  7    Treat the image as a single text line.
#  8    Treat the image as a single word.
#  9    Treat the image as a single word in a circle.
# 10    Treat the image as a single character.
print(pytesseract.image_to_string(FILENAME, config='--psm 10 -c tessedit_char_whitelist=0123456789'))
# endpoint([[0, 0], [1, 10], [2, 6], [3, 4], [4, 6], [5, 10], [1, 20], [5, 20]])


def gen_points():
    points = []
    for i in range(100):
        points.append([i, i])
    return points


endpoint(
    gen_points()
)
