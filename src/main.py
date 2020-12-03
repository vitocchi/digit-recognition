import pytesseract

FILENAME = './2.jpg'

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
print(pytesseract.image_to_string(FILENAME, config='-psm 10'))
