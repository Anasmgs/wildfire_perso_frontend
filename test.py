
#!pip install ultralytics

from ultralytics import YOLO
import cv2

model = YOLO("yolov8_run2.pt")

# run trained model on uploaded image
res = model("test.jpg", save=True, show=True)

# res_plotted = res[0].plot()
# cv2.imshow("result", res_plotted)

