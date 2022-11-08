import curses

import cv2
import numpy

stream = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"

size = 3

cap = cv2.VideoCapture(stream)
height, width, _ = (cap.read()[1]).shape
picker1_index = (
    slice((height // 2 - size), (height // 2 + size)),
    slice((1 * width // 3 - size), (1 * width // 3 + size)),
)
picker2_index = (
    slice((height // 2 - size), (height // 2 + size)),
    slice((2 * width // 3 - size), (2 * width // 3 + size)),
)

screen = curses.initscr()
numpy.set_printoptions(formatter={"float_kind": "{0:.2f}".format})
while cap.isOpened():
    img = cap.read()[1]
    patch1 = img[picker1_index]
    patch2 = img[picker2_index]
    total1 = numpy.average(patch1)
    total2 = numpy.average(patch2)
    bgr1 = numpy.flip(numpy.average(patch1, axis=(0, 1)))
    bgr2 = numpy.flip(numpy.average(patch2, axis=(0, 1)))

    # print color
    screen.clear()
    screen.addstr(0, 1, "R    G    B")
    screen.addstr(0, 18, "Total")
    screen.addstr(
        1,
        0,
        f"{bgr1 / sum(bgr1)}",
    )
    screen.addstr(1, 18, f"{total1 / 255:.3f}")
    screen.addstr(
        2,
        0,
        f"{bgr2 / sum(bgr2)}",
    )
    screen.addstr(2, 18, f"{total2 / 255:.3f}")
    screen.addstr(4, 0, "Press 'q' to quit.")
    screen.refresh()

    # mark the picking location
    img[picker1_index] = 255 - img[picker1_index]
    img[picker2_index] = 255 - img[picker2_index]

    cv2.imshow("Frame", numpy.array(img, dtype=numpy.uint8))
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
