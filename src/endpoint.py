import pytesseract
import os
import statistics
import time
from PIL import Image, ImageDraw


class NoDigitRecognizedError(Exception):
    pass


#
# constant
#
# 画像のpixel数
IMAGE_SIZE = 100
# 画像を構成する点の数
POINT_INTERVAL = 15
# 描画した画像を保存する
SAVE_IMAGES = False
# 削除する軌跡末尾の点の数
SLICE_POINT_NUM = 5


# standalize_points
# 計測した点のリストから画像用の点のリストに変換
# 画像のpixel範囲に収まるように標準化し、
# 計測時のy軸方向を画像描画時のy軸方向に反転させる
#
# 計測時
# y
# |
# |
# |________ x
#
# 画像描画時
#  _______ x
# |
# |
# y
def standalize_points(points: list) -> list:
    x_points = []
    y_points = []
    standalized = []
    for index, point in enumerate(points):
        if len(point) != 2:
            raise Exception("invalid point", point)
        if index == 0:
            continue
        x_points.append(point[0])
        y_points.append(-point[1])
    max_x: int = max(x_points)
    min_x: int = min(x_points)
    max_y: int = max(y_points)
    min_y: int = min(y_points)
    for index in range(len(x_points)):
        x_point = x_points[index]
        y_point = y_points[index]
        standalized.append(((x_point - min_x) * IMAGE_SIZE / float(max_x - min_x), (y_point - min_y) * IMAGE_SIZE / float(max_y - min_y)))
    return standalized


def recognize_digit(image) -> int:
    '''
    画像から数字を認識して返却する。
    数字が認識できなかった場合はNoDigitRecognizedErrorをraiseする。
    '''
    ans_str = pytesseract.image_to_string(image, config='--psm 10 -c tessedit_char_whitelist=0123456789')
    # 改行コードを削除して数字データだけ抽出
    # 数字を認識した場合は['1'], ['2']など
    # 認識しなかった場合は空のlist []
    ans: list = ans_str.split()
    if len(ans) == 0:
        raise NoDigitRecognizedError()
    return int(ans[0])


def recognize_digit_from_locus_points(points: list) -> int:
    '''
    点の軌跡を受け取り、
    定められた点の数で軌跡を区切って画像を描画する。
    その画像に対して数字認識を行う。
    最も多く認識された数字を返す。
    '''
    if SAVE_IMAGES:
        timestamp = time.time()
        outputdir = 'output/' + str(int(timestamp))
        os.makedirs(outputdir)

    answers = []
    for index in range(len(points)):
        im = Image.new('1', (IMAGE_SIZE, IMAGE_SIZE), 1)
        draw = ImageDraw.Draw(im)
        image_points = standalize_points(points[index: index + POINT_INTERVAL])
        draw.line(image_points, 0)
        print('index:' + str(index))
        print(image_points)
        try:
            ans = recognize_digit(im)
            answers.append(ans)
        except NoDigitRecognizedError:
            pass
        if SAVE_IMAGES:
            im.save(outputdir + '/' + str(index) + '.jpg')
        if len(image_points) < POINT_INTERVAL:
            break
    # 数字を一度も認識しなかった場合は-1を返す
    if len(answers) == 0:
        return -1
    # 数字を一度以上認識した場合は、最も多く認識した数字を返す
    return statistics.mode(answers)


def endpoint(locas_points: list) -> int:
    '''
    Labviewから呼び出される関数
    Labviewから座標点の軌跡をリストで受け取り、判定した数字を返す
    認識できた数字がなかった場合は-1を返す
    '''
    if len(locas_points) <= SLICE_POINT_NUM:
        raise Exception("there is no point")
    return recognize_digit_from_locus_points(locas_points[:-SLICE_POINT_NUM])


if __name__ == '__main__':
    import csv
    csv_file = open("18_points/three.csv", "r", newline="")
    # リスト形式
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    points = []
    for row in f:
        points.append([float(row[0]), float(row[1])])
    print(points)
    print(endpoint(
        points
    ))
