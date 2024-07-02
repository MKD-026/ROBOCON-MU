print("loading")
import cv2
import numpy as np
from ultralytics import YOLO
import time
from logic import *
print("load complete")

# load model
model = YOLO("weights/yolov8n.pt", "v8")

#for video input
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()

prev_frame_time = 0
new_frame_time = 0
while True:
    # ret, frame = cap.read()
    frame = cv2.imread("data/test7.jpeg")
    image_height, image_width = frame.shape[0], frame.shape[1]
    imgcenter_x = image_width / 2
    imgcenter_y = image_height / 2

    new_frame_time = time.time()
    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.2, save=False)

    DP = detect_params[0].numpy()
    # print(DP)

    if len(DP) != 0:
        big_box = []
        for i in range(len(detect_params[0])):
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            center_x = (bb[0] + bb[2]) / 2
            center_y = (bb[1] + bb[3]) / 2
            cv2.rectangle(frame, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), (0, 255, 0), 3)

            # Extract bounding box coordinates
            x1, y1, x2, y2 = bb
            x = int(x1)
            y = int(y1)
            w = int(x2 - x1)
            h = int(y2 - y1)

            # Extract the region of interest (ROI) from the bounding box
            roi = frame[y:y + h, x:x + w]

            dominant_color, dominant_hue = get_dominant_color(roi)

            big_box.append((dominant_color, w, bb)) #appending to list

            cv2.putText(frame, str(dominant_color), (int(x + 20), int(y)),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)  # black color
            cv2.putText(frame, str(dominant_hue), (int(x + 20), int(y+10)),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)  # black color

        max_width = 0
        for color, width, bb in big_box:
            if color == "red" and width > max_width: #put correct color here
                max_width = width
                coord = bb #can extract coordinates here

        #call movement function based on coord value here
        '''
        movement_func()
        '''

    # Display the resulting frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "Q" pressed
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()

