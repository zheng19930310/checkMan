#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试版本 - 用于诊断GUI问题
"""

import sys
import traceback

try:
    print("开始导入tkinter...")
    import tkinter as tk
    print("✓ tkinter导入成功")
    
    print("创建主窗口...")
    root = tk.Tk()
    print("✓ 主窗口创建成功")
    
    root.title("调试窗口 - 识别人类")
    root.geometry("600x400")
    
    print("添加标签...")
    label = tk.Label(root, 
                    text="如果你看到这个窗口\n说明GUI系统正常工作！",
                    font=("Microsoft YaHei", 16),
                    fg="blue")
    label.pack(expand=True, pady=50)
    
    info = tk.Label(root,
                   text="这个窗口会保持打开\n关闭此窗口将退出程序",
                   font=("Microsoft YaHei", 12),
                   fg="gray")
    info.pack(pady=20)
    
    print("启动主循环...")
    print("=" * 50)
    print("窗口应该已经显示，请查看屏幕")
    print("=" * 50)
    
    root.mainloop()
    
    print("程序正常退出")
    
except Exception as e:
    print("\n" + "=" * 50)
    print("错误信息：")
    print("=" * 50)
    print(f"错误类型: {type(e).__name__}")
    print(f"错误描述: {e}")
    print("\n详细堆栈：")
    traceback.print_exc()
    print("=" * 50)
    input("\n按回车键退出...")
