#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试摄像头是否正常"""

import cv2

print("正在测试摄像头...")
print("="*60)

# 尝试打开摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ 无法打开摄像头！")
    print("\n可能的原因：")
    print("1. 摄像头被其他程序占用")
    print("2. 摄像头驱动问题")
    print("3. 摄像头硬件故障")
    print("\n建议操作：")
    print("1. 关闭所有可能使用摄像头的程序（微信、QQ、浏览器等）")
    print("2. 重新插拔USB摄像头（如果是外接的）")
    print("3. 重启电脑")
else:
    print("✅ 摄像头打开成功！")
    
    # 尝试读取一帧
    ret, frame = cap.read()
    if ret:
        print("✅ 摄像头读取正常！")
        print(f"📷 分辨率: {frame.shape[1]}x{frame.shape[0]}")
    else:
        print("⚠️  摄像头无法读取画面")
    
    cap.release()
    print("\n✅ 摄像头测试完成，资源已释放")

print("="*60)
input("\n按Enter键退出...")
