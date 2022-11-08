import curses

import cv2
import numpy

# any stream that cv2.VideoCapture can open
stream = 0  # "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"

# size of the color pickers
size = 50

# open video stream and get geometry
cap = cv2.VideoCapture(stream)
height, width, _ = (cap.read()[1]).shape

# color pickers
picker1_index = (
    slice((height // 2 - size), (height // 2 + size)),
    slice((1 * width // 3 - size), (1 * width // 3 + size)),
)
picker2_index = (
    slice((height // 2 - size), (height // 2 + size)),
    slice((2 * width // 3 - size), (2 * width // 3 + size)),
)

# misc initializations
screen = curses.initscr()
numpy.set_printoptions(formatter={"float_kind": "{0:.3f}".format})

# loop through video frames
while cap.isOpened():
    img = cap.read()[1]

    # read and process the color patches
    patch1 = img[picker1_index]
    patch2 = img[picker2_index]
    total1 = numpy.average(patch1)
    total2 = numpy.average(patch2)
    rgb1 = numpy.flip(numpy.average(patch1, axis=(0, 1)))
    rgb2 = numpy.flip(numpy.average(patch2, axis=(0, 1)))

    # print color
    screen.clear()
    screen.addstr(0, 1, "R     G     B")
    screen.addstr(0, 21, "Total")
    screen.addstr(
        1,
        0,
        f"{rgb1 / sum(rgb1)}",
    )
    screen.addstr(1, 21, f"{total1 / 255:.3f}")
    screen.addstr(
        2,
        0,
        f"{rgb2 / sum(rgb2)}",
    )
    screen.addstr(2, 21, f"{total2 / 255:.3f}")
    screen.addstr(4, 0, "Press 'q' to quit.")
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
