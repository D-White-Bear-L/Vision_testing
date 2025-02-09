import cv2
import os
import time
import cv2
import mediapipe as mp

# 指定保存图片的文件夹路径
save_dir = r"C:\programme!\Postured vision testing\face_identify"  # 替换为你的目标文件夹路径

# 如果文件夹不存在，则创建
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# def face_detect():
#     cap = cv2.VideoCapture(0)

#     mpFace_dec = mp.solutions.face_detection
#     mpdraw = mp.solutions.drawing_utils
#     face_dec = mpFace_dec.FaceDetection(0.75)

#     Pre_time = 0
#     while 1:
#         res, img = cap.read()
#         img_rgb = cv2.cvtColor(img, code=cv2.COLOR_BGR2RGB)
#         Results = face_dec.process(img_rgb)
#         if Results.detections:
#             for id, detection in enumerate(Results.detections):
#                 bboxC = detection.location_data.relative_bounding_box
#                 h, w, c = img.shape
#                 bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
#                        int(bboxC.width * w), int(bboxC.height * h)
#                 cv2.rectangle(img, bbox, (0, 255, 0), 2)
#                 cv2.putText(img, "success", (bbox[0], bbox[1] - 20),
#                             cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

#         cv2.imshow('kobe', img)
#         cv2.waitKey(1)

#         ret, buffer = cv2.imencode('.jpg', img)
#         frame1 = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')

# 打开默认摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# 拍摄100张照片
for i in range(100):
    # 读取一帧画面
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

        # 构造图片保存路径和文件名
    filename = os.path.join(save_dir, f'lwx_{i+400:03d}.jpg')  # 使用03d格式化来确保文件名为三位数

    # 保存图片
    cv2.imwrite(filename, frame)
    print(f"rxz {i + 1:03d} face {filename}")

    # 等待一段时间，以便用户查看和调整摄像头（可选）
    time.sleep(0.1)  # 等待1秒，可以根据需要调整

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()