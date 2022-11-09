import curses

import cv2
import numpy

# any stream that cv2.VideoCapture can open
stream = 0  # "rtsp://rtsp.stream/pattern"

# size of the color pickers
size = 0.5


# open video stream and get geometry
cap = cv2.VideoCapture(stream)
height, width, _ = (cap.read()[1]).shape

# color pickers
size = int(size * height / 6)
picker1_index = (
    slice((height // 3 - size), (height // 3 + size)),
    slice((width // 2 - size), (1 * width // 2 + size)),
)
picker2_index = (
    slice((2 * height // 3 - size), (2 * height // 3 + size)),
    slice((width // 2 - size), (width // 2 + size)),
)

# misc initializations
screen = curses.initscr()
numpy.set_printoptions(formatter={"float_kind": "{0:.3f}".format})

# loop through video frames
while cap.isOpened():
    img = numpy.float32(cap.read()[1])

    # read and process the color patches
    patch1 = img[picker1_index]
    patch2 = img[picker2_index]
    total1 = numpy.average(patch1)
    total2 = numpy.average(patch2)
    rgb1 = numpy.flip(numpy.average(patch1, axis=(0, 1)))
    rgb2 = numpy.flip(numpy.average(patch2, axis=(0, 1)))
    hsv1 = numpy.average(cv2.cvtColor(patch1, cv2.COLOR_BGR2HSV_FULL), axis=(0, 1))
    hsv2 = numpy.average(cv2.cvtColor(patch2, cv2.COLOR_BGR2HSV_FULL), axis=(0, 1))
    print(hsv1)

    # print RGB
    screen.clear()
    screen.addstr(0, 0, "Press 'q' to quit.")
    screen.addstr(2, 1, "R     G     B")
    screen.addstr(2, 21, "Total")
    screen.addstr(
        3,
        0,
        f"{rgb1 / sum(rgb1)}",
    )
    screen.addstr(3, 21, f"{total1 / 255:.3f}")
    screen.addstr(
        4,
        0,
        f"{rgb2 / sum(rgb2)}",
    )
    screen.addstr(4, 21, f"{total2 / 255:.3f}")

    # print HSV
    screen.addstr(6, 1, "H       S     V")
    screen.addstr(7, 0, f"{hsv1}")
    screen.addstr(8, 0, f"{hsv2}")
    screen.refresh()

    # mark the picking location
    img[picker1_index] = 255 - img[picker1_index]
    img[picker2_index] = 255 - img[picker2_index]

    # display frame until 'q' is pressed
    cv2.imshow("Frame", numpy.array(img, dtype=numpy.uint8))
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
