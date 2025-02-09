import asyncio
import cv2
import websockets
import base64
import mediapipe as mp
import random
import time
import numpy as np
import base64
import serial
import pyttsx3
import threading
from concurrent.futures import ThreadPoolExecutor

value = None
experience_img = 0
# hand_style = None  # 定义全局变量
shared_data = {"hand_style":None}
lock= asyncio.Lock()#锁对象

def choose_random_value(arr):#定义一个函数，在一个列表中选取随机值
    # 使用 random 模块的 choice 函数选择一个随机元素
    random_value = random.choice(arr)
    return random_value

#********************检测函数**************
def identity(frame):
    global last_change_time,correct_count,width,current_size_index,wrong_count,level,window_width,window_height, value,hand_tip
    # 判断手部姿势，显示放在左上角
    if hand_tip.x < arm.x - 0.05:
        cv2.putText(frame, f"{L}", (10, 400), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        value = 2  # 取出done的动作的值，为后面的比较做准备
    elif hand_tip.x > arm.x + 0.05:
        cv2.putText(frame, f"{R}", (10, 400), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        value = 3
    elif hand_tip.y < arm.y - 0.05:
        cv2.putText(frame, f"{U}", (10, 400), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        value = 0
    elif hand_tip.y > arm.y + 0.05:
        cv2.putText(frame, f"{D}", (10, 400), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        value = 1

    return value 

shared_data = {"hand_style":None}
lock= asyncio.Lock()#锁对象
#前端的按钮点击返回参数1/2
# global data
async def recive_data(websocket,path):
    global data
    data = await websocket.recv()
    print("接收参数：",data)
    # hand_style= data
    async with lock:
        shared_data["hand_style"]=data
    print("hand_style-r=",shared_data["hand_style"])

# 初始化语音引擎
# engines = [pyttsx3.init() for _ in range(4)]  # 创建4个语音引擎实例

# 创建四个线程池
# executor = ThreadPoolExecutor(max_workers=4)

# def speak(text):
#     """使用语音引擎朗读文本"""
#     # 选择一个语音引擎实例
#     engine = engines[experience_img]
#     engine.say(text)
#     engine.runAndWait()

# # 加载动图
# with open("./templates/picture-css/speak.gif", "rb") as image_file:
#     animated_gif = image_file.read()


#初始化人脸识别模块
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

experience_img=0
#初始化人脸识别模块
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# 初始化Holistic模型
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#初始化一些变量
# value = None
R="Right"
L='Left'
U="Up"
D="Down"
a=b=c=d=e=f=g=h=i=j=k=l=m=n=x=y= 0
level=46

correct_count = 0
wrong_count = 0
count = [x,a,b,c,d,e,f,g,h,i,j,k,l,m,n,y]

# 初始化 Mediapipe Hands 模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
flag = ['Right','Left','Up','Down']


font = cv2.FONT_HERSHEY_SIMPLEX#这里定义了文字的字体类型

#现用time()函数获取现在的时间，赋值给变量last_change_time（上一次改变的时间）
last_change_time = time.time()
last_change_time_e = time.time()


async def websocket_handler(websocket,path):
    global value
    try:
        while True:
            # print("send")
            print("send:",str(value))
            # # 将值发送给 JavaScript 客户端
            await websocket.send(str(value))
            await asyncio.sleep(4.5)  # 等待 4.5 秒再发送下一次数据
    except:
        print("Error！")            


# 读取视频流
async def video_stream(websocket, path):
    global last_change_time, random_img,flag,last_image,images_to_insert,resized_image,width,current_size_index,font,size,hands,mp_hands,count,correct_count,wrong_count,holistic,value,hand_tip,arm,R,D,L,U
    global experience_img,hand_tip,should_stop
    is_streaming = True  # 新增变量：表示当前是否正在传输视频流
    camera = cv2.VideoCapture(0)
    global data
    value = None
    R="Right"
    L='Left'
    U="Up"
    D="Down"

    
    while True:
        success, frame = camera.read()
        if not success:
            break
        # 镜像画面，镜像后，左右相反
        frame = cv2.flip(frame, 1)
        async with lock:
            #不是空的时候才显示识别
            if shared_data["hand_style"] is not None:
                # print("hand_style-v=",shared_data["hand_style"])
                # print(type(int(shared_data["hand_style"])))

                
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 获取人脸关键点和姿势信息（降低外界干扰）
                results = hands.process(image)
                results = holistic.process(image)

                # print("hand_style-v=",hand_style)

                if results.pose_landmarks and results.face_landmarks and results.left_hand_landmarks and results.right_hand_landmarks:
                    # 在图像中绘制身体关键点和连接线
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

                #手部节点
                #右手（镜像后）
                #!!(websocket传输的参数都是String类型的，要类型对应，才可以判断)!!
                if (results.left_hand_landmarks and (int(shared_data["hand_style"])==2 or int(shared_data["hand_style"])==4)):
                    for landmark in results.left_hand_landmarks.landmark:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 6, (255, 0, 255), -1)
                #左手（镜像后）
                if (results.right_hand_landmarks and int(shared_data["hand_style"]) == 1):
                    for landmark in results.right_hand_landmarks.landmark:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 6, (255, 255, 0), -1)

                # 在帧上显示文字信息
                # cv2.putText(frame, f"Want:{random_img}", (10, 400), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

                if (int(shared_data["hand_style"]) == 1 and results.right_hand_landmarks):
                    # print(1)
                    # 获取第一只右手的关键点信息
                    right_hand_landmarks = results.right_hand_landmarks.landmark
                    # 获取整只手臂的坐标
                    arm = right_hand_landmarks[mp_hands.HandLandmark.WRIST]
                    hand_tip = right_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
                    value = None
                    identity(frame)


                elif (int(shared_data["hand_style"]) == 2 and results.left_hand_landmarks):
                    # print(2)
                    # 获取第一只左手的关键点信息
                    left_hand_landmarks = results.left_hand_landmarks.landmark
                    # 获取整只手臂的坐标
                    arm = left_hand_landmarks[mp_hands.HandLandmark.WRIST]
                    hand_tip = left_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
                    value = None
                    identity(frame)

                #*******示教

                elif (int(shared_data["hand_style"]) == 4 and results.left_hand_landmarks):
                    left_hand_landmarks = results.left_hand_landmarks.landmark
                    # 获取整只手臂的坐标
                    arm = left_hand_landmarks[mp_hands.HandLandmark.WRIST]
                    hand_tip = left_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
                    value = None
                    if experience_img == 0:
                        # speak("请将你的右手向正上方向伸直。")
                        identity(frame)
                        if value==0:
                            experience_img+=1
                            print(experience_img)
                    elif experience_img == 1:
                        # speak("请将你的右手向正下方向伸直")
                        identity(frame)
                        if value==1:
                            experience_img+=1
                            print(experience_img)
                    elif experience_img == 2:
                        # speak("请将你的右手向正左方向伸直。")
                        identity(frame)
                        # has_played = False
                        if value==2:
                            experience_img+=1
                            print(experience_img)
                    elif experience_img == 3:
                        # speak("请将你的右手向正右方向伸直。")
                        identity(frame)
                        if value ==3:
                            experience_img+=1
                            print(experience_img)
                    else:
                        identity(frame)

                elif (int(shared_data["hand_style"]) == 3):
                    # 关闭摄像头
                    camera.release()

                    # 停止传输视频流
                    is_streaming = False
                    # #*******示教

            # 将帧转换为 Base64 编码的字符串
        _, buffer = cv2.imencode('.jpg', frame)
        frame_as_bytes = base64.b64encode(buffer)
        frame_as_text = frame_as_bytes.decode('utf-8')
        if is_streaming:
            # 发送帧到前端
            try:
                await websocket.send(frame_as_text)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed unexpectedly: {e}")
                # 这里可以考虑关闭摄像头、清理资源等操作
                camera.release()
                is_streaming = False
        

async def serial_communication(websocket, path):
    global value
    while True:
        async with lock:
            if int(shared_data["hand_style"]) == 3:
                # 串口设置
                port = 'COM3'
                baudrate = 9600
                timeout = 1

                ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

                while True:
                    try:
                        received_data = ser.readline().strip()
                    except serial.SerialTimeoutException:
                        print("串行读取超时，跳过此次数据接收")
                    except Exception as e:
                        print(f"串行读取时遇到未知错误：{e}")
                    # print(received_data)
                    if received_data:
                        if received_data == b'\x00':
                            value = "0"
                            break
                        elif received_data == b'\x01':
                            value = "1"
                            break
                        elif received_data == b'\x02':
                            value = "2"
                            break
                        elif received_data == b'\x03':
                            value = "3"
                            break

                        print("Received data:", value)  # 打印接收到的数据

                        print("speak-send:", str(value))

                    else:
                        print("Received nothings")

                ser.close()

                # 将值发送给 JavaScript 客户端
                await websocket.send(str(value))

                # 清除已发送的值，等待下一次通信
                value = None

            # 如果不是模式3，则休眠，避免频繁检查
            await asyncio.sleep(1)


# 启动 WebSocket 服务器

#接收前端按钮返回参数
start= websockets.serve(recive_data,"localhost",8767)
#发送手部值value
start_server = websockets.serve(
    websocket_handler, "localhost", 8765
)
#传输视频流
video_server = websockets.serve(
    video_stream, "localhost", 8766
)
#传输语音
speak_server = websockets.serve(
    serial_communication, "localhost", 8768
)

# 同时运行4个服务器
asyncio.get_event_loop().run_until_complete(start)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(video_server)
asyncio.get_event_loop().run_until_complete(speak_server)
asyncio.get_event_loop().run_forever()
