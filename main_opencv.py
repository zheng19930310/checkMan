#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
识别人类 - OpenCV原生窗口版本（更稳定）
"""

import cv2
import numpy as np
import time

print("=" * 60)
print("识别人类 - OpenCV原生窗口版本")
print("=" * 60)
print()

# 打开摄像头
print("[1/3] 打开摄像头...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("✗ 无法打开摄像头")
    input("按回车键退出...")
    exit(1)

print("✓ 摄像头已打开")
print()

# 加载中文字体
print("[2/3] 加载中文字体...")
try:
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 尝试使用Pillow绘制中文
    from PIL import Image, ImageDraw, ImageFont
    chinese_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)
    print("✓ 中文字体加载成功")
except:
    print("⚠ 使用英文字体")
    chinese_font = None

print()
print("[3/3] 启动识别窗口...")
print("=" * 60)
print("提示：")
print("- 按 'q' 键退出程序")
print("- 按 's' 键保存当前帧")
print("=" * 60)
print()

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        break
    
    frame_count += 1
    
    # 每3帧处理一次人脸检测
    if frame_count % 3 == 0:
        # 人脸检测
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        # 绘制识别结果
        for (x, y, w, h) in faces:
            # 绘制绿色矩形框
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # 使用英文显示（避免中文乱码）
            cv2.putText(frame, "Person", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # 显示帧数
    cv2.putText(frame, f"FPS: {frame_count//3}", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    # 显示窗口
    cv2.imshow('识别人类 - 按q退出', frame)
    
    # 按键处理
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\n用户退出")
        break
    elif key == ord('s'):
        filename = f"screenshot_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✓ 已保存: {filename}")

# 释放资源
cap.release()
cv2.destroyAllWindows()

print()
print("=" * 60)
print("程序已退出")
print("=" * 60)
input("\n按回车键关闭窗口...")
