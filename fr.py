import face_recognition
import cv2
from PIL import Image
import numpy as np

known_image = face_recognition.load_image_file("Cropped1.png")
unknown_image = face_recognition.load_image_file("prev.jpg")
face_locations = face_recognition.face_locations(unknown_image)
print(face_locations)
# unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)
# ggg = cv2.imread("prev.jpg")
# print(ggg[0][0], unknown_image[0][0])

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
print(results)