#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新用户录入对话框
"""

import tkinter as tk
from tkinter import messagebox

class NewUserDialog:
    def __init__(self, parent, callback):
        self.callback = callback
        self.result = None
        
        # 创建顶层窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("录入新用户")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # 居中显示
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 创建界面
        frame = tk.Frame(self.dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            frame, 
            text="检测到新人物", 
            font=("微软雅黑", 14, "bold"),
            fg="blue"
        )
        title_label.pack(pady=(0, 10))
        
        # 提示
        hint_label = tk.Label(
            frame, 
            text="请输入此人姓名：",
            font=("微软雅黑", 10)
        )
        hint_label.pack(pady=(0, 5))
        
        # 姓名输入框
        self.name_entry = tk.Entry(
            frame, 
            font=("微软雅黑", 12),
            width=20,
            justify=tk.CENTER
        )
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()
        
        # 按钮框架
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        
        # 确定按钮
        ok_btn = tk.Button(
            btn_frame,
            text="确定",
            command=self.on_ok,
            bg="green",
            fg="white",
            font=("微软雅黑", 10),
            width=8
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        # 取消按钮
        cancel_btn = tk.Button(
            btn_frame,
            text="跳过",
            command=self.on_cancel,
            bg="gray",
            fg="white",
            font=("微软雅黑", 10),
            width=8
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入姓名！")
            return
        
        self.result = name
        self.callback(name)
        self.dialog.destroy()
    
    def on_cancel(self):
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """显示对话框并等待用户输入"""
        self.dialog.wait_window()
        return self.result


if __name__ == "__main__":
    # 测试
    root = tk.Tk()
    root.withdraw()
    
    def callback(name):
        print(f"录入的用户名: {name}")
    
    dialog = NewUserDialog(root, callback)
    result = dialog.show()
    print(f"结果: {result}")
    
    root.destroy()
