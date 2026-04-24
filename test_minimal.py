#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最小化摄像头测试 - 使用root.after()而非线程
"""

import cv2
import tkinter as tk
from PIL import Image, ImageTk

print("启动最小化测试程序...")

root = tk.Tk()
root.title("摄像头测试")
root.geometry("640x520")

video_label = tk.Label(root, bg="black")
video_label.pack(fill=tk.BOTH, expand=True)

cap = None
running = False

def start_cam():
    global cap, running
    print("点击了启动按钮")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    print("摄像头已打开")
    running = True
    process_frame()

def process_frame():
    global running, cap
    
    if not running or cap is None:
        return
    
    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        running = False
        return
    
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((640, 480))
    img_tk = ImageTk.PhotoImage(image=img)
    
    video_label.config(image=img_tk)
    video_label.image = img_tk
    
    # 使用after方法，每33ms调用一次（约30fps）
    root.after(33, process_frame)

def stop_cam():
    global running, cap
    print("点击了停止按钮")
    running = False
    if cap:
        cap.release()
        cap = None

btn_start = tk.Button(root, text="启动", command=start_cam, bg="green", fg="white")
btn_start.pack(side=tk.LEFT, padx=10, pady=10)

btn_stop = tk.Button(root, text="停止", command=stop_cam, bg="red", fg="white")
btn_stop.pack(side=tk.LEFT, padx=10, pady=10)

print("窗口已创建，请点击按钮测试")
root.mainloop()
print("程序退出")
