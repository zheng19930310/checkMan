#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
摄像头深度诊断工具
"""

import sys
import traceback

print("=" * 60)
print("摄像头深度诊断工具")
print("=" * 60)
print()

try:
    print("[步骤1] 导入cv2...")
    import cv2
    print("✓ cv2导入成功")
    print(f"  OpenCV版本: {cv2.__version__}")
    print()
    
    print("[步骤2] 尝试打开摄像头索引0...")
    cap = cv2.VideoCapture(0)
    print(f"✓ VideoCapture对象创建成功")
    print()
    
    print("[步骤3] 检查摄像头是否打开...")
    if cap.isOpened():
        print("✓ 摄像头已打开")
    else:
        print("✗ 摄像头未打开")
        print("  可能原因：")
        print("  - 摄像头被其他程序占用")
        print("  - 摄像头驱动问题")
        print("  - 权限问题")
        cap.release()
        sys.exit(1)
    
    print()
    print("[步骤4] 读取摄像头参数...")
    try:
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"✓ 分辨率: {width}x{height}")
        print(f"✓ FPS: {fps}")
    except Exception as e:
        print(f"⚠ 读取参数失败: {e}")
    
    print()
    print("[步骤5] 尝试读取一帧...")
    ret, frame = cap.read()
    if ret:
        print(f"✓ 成功读取一帧")
        print(f"  帧尺寸: {frame.shape}")
        print(f"  帧类型: {type(frame)}")
    else:
        print("✗ 无法读取帧")
        cap.release()
        sys.exit(1)
    
    print()
    print("[步骤6] 尝试读取10帧（测试稳定性）...")
    success_count = 0
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            success_count += 1
    print(f"✓ 成功读取 {success_count}/10 帧")
    
    cap.release()
    
    print()
    print("=" * 60)
    print("诊断结果: 摄像头工作正常！")
    print("=" * 60)
    
except Exception as e:
    print()
    print("=" * 60)
    print("诊断结果: 摄像头测试失败！")
    print("=" * 60)
    print(f"\n错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n详细堆栈:")
    traceback.print_exc()
    print("=" * 60)

print()
input("按回车键退出...")
