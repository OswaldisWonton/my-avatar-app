import os
import cv2
import time

from utils.face_utils import face_detection
from utils.controller import ThresholdController

def get_video_list(path):
    ans = dict()
    for root, dirs, files in os.walk(path):
        for file in files:
            key = file.split("_")[0]
            if key in ans:
                ans[key].append(os.path.join(root, file))
            else:
                ans[key] = [os.path.join(root, file)]
    return ans

def normalize_window(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # cv2.resizeWindow('Screen', width, height)
    cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def camera_and_detection(T=20, threshold=0.9, lower_bound=True, display=False, output=None):

    if lower_bound:
        threshold_controller = ThresholdController(T, threshold_low=threshold)
    else:
        threshold_controller = ThresholdController(T, threshold_high=threshold)
        threshold_controller._set()

    cap = cv2.VideoCapture(1)

    normalize_window(cap)

    if not cap.isOpened():
        exit("Error: Could not open video device.")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    flag = 0
    frame = None
    while True:
        ret, frame = cap.read()
        if ret:
            if threshold_controller(face_detection(frame)):
                flag = 1
                break
            if display:
                cv2.imshow('Screen', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): # 按'q'键退出循环
                print("[INFO] Interrupt by keyboard.")
                break
        else:
            print("[INFO] Error: No frame received.")
            break

    # 释放摄像头资源
    cap.release()
    result = frame if flag else None
    if output is not None:
        output.append(result)
    return result

# def video_display(video_path, cycle=False):

#     cap = cv2.VideoCapture(video_path)
    
#     normalize_window(cap)

#     if not cap.isOpened():
#         print("Error: Could not open video.")
    
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_interval = 1 / fps

#     while True:
#         start_time = time.time()

#         ret, frame = cap.read()

#         if ret:
#             cv2.imshow('Video', frame)

#             elapsed_time = time.time() - start_time
#             wait_time = max(int((frame_interval - elapsed_time) * 1000), 1)
#             if cv2.waitKey(wait_time) & 0xFF == ord('q'):
#                 break
#         elif cycle:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         else:
#             break

#     # 释放视频资源
#     cap.release()
#     cv2.destroyAllWindows()

def video_display(video_path, cycle=0, flag=[]):

    cap = cv2.VideoCapture(video_path)
    
    normalize_window(cap)

    if not cap.isOpened():
        print("Error: Could not open video.")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 / fps

    quit_ = False

    cycle_count = 0
    while True:

        start_time = time.time()

        ret, frame = cap.read()

        if ret:
            cv2.imshow('Screen', frame)
            if flag:
                break
            elapsed_time = time.time() - start_time
            wait_time = max(int((frame_interval - elapsed_time) * 1000), 1)
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                quit_ = True
                break
        elif cycle:
            if cycle > 0:
                cycle_count += 1
                if cycle_count >= cycle:
                    break
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            break

    # 释放视频资源
    cap.release()

    return quit_
