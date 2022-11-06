#!/usr/bin/python3

import cv2
import numpy as np
import matplotlib.pyplot as plt

from picamera2.picamera2 import *

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.preview_configuration(main={"size": (640, 480)},
                                      lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]

picam2.start()

buffer = picam2.capture_buffer("lores")
print(f'buffer size: {buffer.shape} test: {len(buffer) / 320 / 240}')
print(f'w0 h0 = {w0} {h0}  w1 h2 = {w1} {h1}')
grey = buffer[:s1 * h1].reshape((h1, s1))
# yuv = (320, 240)
rgb = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)
cv2.imwrite('test.jpg', grey)
