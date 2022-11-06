#!/usr/bin/python3
import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw
import face_recognition
import random

from picamera2.picamera2 import *

boss_names = []

face_databases_dir = 'face_database'
user_names = []
user_faces_encodings = []

files = os.listdir(face_databases_dir)

information = []

display_process = []

def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    pil_img = img
    if isinstance(img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGBA2RGB))
    draw = ImageDraw.Draw(pil_img)
    fontStyle = ImageFont.truetype(
        "/usr/share/fonts/simsun.ttc", textSize, encoding="utf-8")
    draw.text(position, text, textColor, font=fontStyle)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2RGBA)
    img[:] = cv2_img[:]
    return cv2_img


def draw_faces(request):
    stream = request.picam2.stream_map["main"]
    fb = request.request.buffers[stream]
    with fb.mmap(0) as b:
        im = np.array(b, copy=False, dtype=np.uint8).reshape((h0, w0, 4))
        clear_flag = True
        for (top, right, bottom, left), name in information:
            if clear_flag:
                for process in display_process:
                    process.kill()
                display_process.clear()
                clear_flag = False
            color = (0, 255, 0)
            if name in boss_names:
                color = (0, 0, 255)
            cv2.rectangle(im, (left, top), (right, bottom), color, 2)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(im, name, (left, top - 10), font, 0.5, color, 1)
            im = cv2AddChineseText(im, name, (int(left), int(top - 10)), textColor=color)
            cv2.imwrite(f"detected_face_{name}.png", im)
            os.chmod(f"detected_face_{name}.png", 777)
            pic = Image.fromarray(im)
            pic.show()
            pic.save
            random.randint(0,10)
        del im


def detect_faces(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(user_faces_encodings, face_encoding)
        name = 'Unknown'
        for index, is_match in enumerate(matches):
            if is_match:
                name = user_names[index]
                break
        names.append(name)
    return zip(face_locations, names)


for image_shot_name in files:
    user_name, _ = os.path.splitext(image_shot_name)
    user_names.append(user_name)

    image_file_name = os.path.join(face_databases_dir, image_shot_name)
    image_file = face_recognition.load_image_file(image_file_name)
    face_encoding = face_recognition.face_encodings(image_file)[0]
    user_faces_encodings.append(face_encoding)

normalSize = (640, 480)
lowresSize = (320, 240)

rconSize = (160, 120)

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
resolution = lowresSize
config = picam2.preview_configuration(main={"size": resolution},
                                      lores={"size": resolution, "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
stride = picam2.stream_configuration("lores")["stride"]

picam2.request_callback = draw_faces

picam2.start()

start_time = time.monotonic()
# Run for 10 seconds so that we can include this example in the test suite.
while time.monotonic() - start_time < 100:
    buffer = picam2.capture_buffer("lores")
    rgb = cv2.cvtColor(buffer.reshape(h1 * 3 // 2, w1), cv2.COLOR_YUV2RGB_I420)
    # grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
    # rgb = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)
    cv2.resize(rgb, rconSize)
    information = detect_faces(rgb)

cv2.destroyAllWindows()
