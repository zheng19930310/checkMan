#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
环境测试脚本
用于检查是否具备运行主程序的条件
"""

import sys
import os

def test_python():
    """测试Python版本"""
    print("=" * 50)
    print("Python版本测试")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"当前目录: {os.getcwd()}")
    print()

def test_tkinter():
    """测试tkinter"""
    print("=" * 50)
    print("tkinter测试")
    print("=" * 50)
    try:
        import tkinter as tk
        print("✓ tkinter 导入成功")
        
        # 创建一个测试窗口
        root = tk.Tk()
        root.title("环境测试窗口")
        root.geometry("400x300")
        
        label = tk.Label(root, 
                        text="如果你看到这个窗口\n说明tkinter正常工作！",
                        font=("Microsoft YaHei", 14),
                        fg="blue")
        label.pack(expand=True)
        
        info = tk.Label(root,
                       text="这个窗口会在3秒后自动关闭\n然后继续测试其他组件",
                       font=("Microsoft YaHei", 10),
                       fg="gray")
        info.pack(pady=10)
        
        # 3秒后自动关闭
        root.after(3000, root.destroy)
        root.mainloop()
        
        print("✓ tkinter窗口显示成功")
        print()
        return True
        
    except Exception as e:
        print(f"✗ tkinter测试失败: {e}")
        print()
        return False

def test_opencv():
    """测试OpenCV"""
    print("=" * 50)
    print("OpenCV测试")
    print("=" * 50)
    try:
        import cv2
        print(f"✓ OpenCV导入成功，版本: {cv2.__version__}")
        
        # 测试摄像头
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ 摄像头打开成功，分辨率: {frame.shape[1]}x{frame.shape[0]}")
            else:
                print("✗ 无法读取摄像头画面")
            cap.release()
        else:
            print("✗ 无法打开摄像头（可能没有摄像头或被占用）")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ OpenCV测试失败: {e}")
        print("  请运行: pip install opencv-python")
        print()
        return False

def test_pil():
    """测试PIL"""
    print("=" * 50)
    print("PIL/Pillow测试")
    print("=" * 50)
    try:
        from PIL import Image, ImageTk
        print("✓ PIL/Pillow 导入成功")
        print()
        return True
        
    except Exception as e:
        print(f"✗ PIL测试失败: {e}")
        print("  请运行: pip install Pillow")
        print()
        return False

def test_numpy():
    """测试numpy"""
    print("=" * 50)
    print("NumPy测试")
    print("=" * 50)
    try:
        import numpy as np
        print(f"✓ NumPy导入成功，版本: {np.__version__}")
        print()
        return True
        
    except Exception as e:
        print(f"✗ NumPy测试失败: {e}")
        print("  请运行: pip install numpy")
        print()
        return False

def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "识别人类 - 环境测试工具" + " " * 12 + "║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    results = []
    
    # 测试Python
    test_python()
    
    # 测试各个库
    results.append(("tkinter", test_tkinter()))
    results.append(("OpenCV", test_opencv()))
    results.append(("PIL", test_pil()))
    results.append(("NumPy", test_numpy()))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name:10s}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有测试通过！可以运行主程序了")
        print("\n运行命令: python main_gui.py")
    else:
        print("⚠️  部分测试失败，请安装缺失的依赖")
        print("\n安装命令:")
        print("  pip install opencv-python pillow numpy")
    
    print()
    input("按回车键退出...")

if __name__ == "__main__":
    main()
