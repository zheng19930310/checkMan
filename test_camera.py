#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
摄像头测试工具
"""

import cv2
import sys

print("=" * 50)
print("摄像头诊断工具")
print("=" * 50)
print()

# 测试摄像头0
print("[测试] 正在尝试打开摄像头 0...")
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("✓ 摄像头 0 打开成功！")
    
    # 获取摄像头属性
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"  分辨率: {int(width)}x{int(height)}")
    print(f"  FPS: {fps}")
    
    # 尝试读取一帧
    ret, frame = cap.read()
    if ret:
        print(f"✓ 成功读取帧，尺寸: {frame.shape}")
        print()
        print("=" * 50)
        print("摄像头工作正常！")
        print("=" * 50)
    else:
        print("✗ 无法读取摄像头画面")
        
    cap.release()
else:
    print("✗ 摄像头 0 打开失败！")
    print()
    print("可能的原因：")
    print("1. 摄像头被其他程序占用（如Zoom、Teams等）")
    print("2. 摄像头驱动未安装")
    print("3. 摄像头权限未授予")
    print("4. 硬件摄像头不存在或损坏")
    print()
    print("请尝试：")
    print("- 关闭其他可能使用摄像头的程序")
    print("- 检查设备管理器中摄像头是否正常")
    print("- 尝试使用外部USB摄像头")

print()
input("按回车键退出...")
