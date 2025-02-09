import cv2
import mediapipe as mp
mpdraw=None
Pre_time=None
def face_detect():
    global mpdraw,Pre_time
    cap = cv2.VideoCapture(0)

    mpFace_dec = mp.solutions.face_detection
    mpdraw = mp.solutions.drawing_utils
    face_dec = mpFace_dec.FaceDetection(0.75)

    Pre_time = 0
    while 1:
        res, img = cap.read()
        img_rgb = cv2.cvtColor(img, code=cv2.COLOR_BGR2RGB)
        Results = face_dec.process(img_rgb)
        if Results.detections:
            for id, detection in enumerate(Results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(img, bbox, (0, 255, 0), 2)
                cv2.putText(img, "success", (bbox[0], bbox[1] - 20),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow('kobe', img)
        cv2.waitKey(1)

        # ret, buffer = cv2.imencode('.jpg', img)
        # frame1 = buffer.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
        

face_detect()