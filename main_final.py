#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
识别人类 - 最终稳定版
修复：正确的窗口关闭处理
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import threading
import time
from face_recognizer import FaceRecognizer

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类 - 人脸识别系统")
        self.root.geometry("1000x750")
        self.root.configure(bg='#1a1a2e')
        
        self.running = False
        self.cap = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # 初始化人脸识别器
        print("正在初始化人脸识别器...")
        self.recognizer = FaceRecognizer()
        stats = self.recognizer.get_stats()
        print(f"已加载 {stats['users']} 个用户，{stats['features']} 个特征")
        
        # 用于跟踪新用户
        self.last_unknown_time = 0
        self.last_unknown_face = None
        
        # 创建界面
        self.create_widgets()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="识别人类 - 人脸识别系统",
            font=('Microsoft YaHei', 20, 'bold'),
            bg='#1a1a2e',
            fg='#00ff00'
        )
        title_label.pack()
        
        # 控制按钮区域
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # 启动按钮
        self.start_btn = tk.Button(
            control_frame,
            text="▶ 启动摄像头",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#00aa00',
            fg='white',
            width=15,
            height=2,
            cursor='hand2',
            command=self.start_camera
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # 停止按钮
        self.stop_btn = tk.Button(
            control_frame,
            text="■ 停止摄像头",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#aa0000',
            fg='white',
            width=15,
            height=2,
            cursor='hand2',
            command=self.stop_camera,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # 统计信息
        self.stats_label = tk.Label(
            control_frame,
            text=f"用户数: {self.recognizer.get_stats()['users']} | 特征数: {self.recognizer.get_stats()['features']}",
            font=('Microsoft YaHei', 10),
            bg='#1a1a2e',
            fg='#00ffff'
        )
        self.stats_label.pack(side=tk.RIGHT, padx=10)
        
        # 视频显示区域
        self.video_frame = tk.Frame(self.root, bg='#000000', relief=tk.SUNKEN, bd=2)
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 视频标签
        self.video_label = tk.Label(self.video_frame, bg='#000000')
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # 提示信息
        tip_frame = tk.Frame(self.root, bg='#1a1a2e')
        tip_frame.pack(fill=tk.X, pady=5)
        
        tip_label = tk.Label(
            tip_frame,
            text="提示：点击启动摄像头开始识别 | 点击停止摄像头结束 | 点击窗口右上角关闭程序",
            font=('Microsoft YaHei', 9),
            bg='#1a1a2e',
            fg='#888888'
        )
        tip_label.pack()
        
    def on_closing(self):
        """处理窗口关闭事件"""
        print("\n正在关闭程序...")
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        self.root.destroy()
        
    def start_camera(self):
        """启动摄像头"""
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开摄像头！")
            return
        
        print("✅ 摄像头已启动")
        self.running = True
        
        self.start_btn.config(state=tk.DISABLED, bg='#666666')
        self.stop_btn.config(state=tk.NORMAL, bg='#aa0000')
        
        # 在新线程中处理视频
        thread = threading.Thread(target=self.video_loop, daemon=True)
        thread.start()
        
    def stop_camera(self):
        """停止摄像头"""
        print("正在停止摄像头...")
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        print("✅ 摄像头已停止")
        
        self.start_btn.config(state=tk.NORMAL, bg='#00aa00')
        self.stop_btn.config(state=tk.DISABLED, bg='#666666')
        
    def draw_chinese_text(self, img, text, position, font_size=24, color=(255, 255, 255)):
        """在图像上绘制中文文本"""
        # 尝试加载微软雅黑字体
        font_path = "C:/Windows/Fonts/msyh.ttc"
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            # 备用字体
            font_path = "C:/Windows/Fonts/simsun.ttc"
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                # 最后使用默认字体
                font = ImageFont.load_default()
        
        # 转换为PIL图像
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        draw.text(position, text, font=font, fill=color)
        
        # 转换回OpenCV格式
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def video_loop(self):
        """视频处理循环"""
        print("🎥 视频处理线程已启动")
        
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("⚠️  无法读取摄像头画面")
                    time.sleep(0.1)
                    continue
                
                # 缩小图像以加快处理速度
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
                
                # 检测人脸
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                # 处理每个人脸
                for (x, y, w, h) in faces:
                    # 还原到原始尺寸
                    x, y, w, h = x * 2, y * 2, w * 2, h * 2
                    
                    # 提取人脸区域
                    face_roi = frame[y:y+h, x:x+w]
                    
                    if face_roi.size == 0:
                        continue
                    
                    # 预处理
                    face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
                    face_resized = cv2.resize(face_gray, (200, 200))
                    face_equalized = cv2.equalizeHist(face_resized)
                    
                    # 识别人脸
                    name, confidence = self.recognizer.recognize_face(face_equalized)
                    
                    # 计算相似度
                    similarity = max(0, 100 - confidence)
                    
                    # 根据识别结果显示不同颜色
                    if name == "？？？":
                        color = (0, 0, 255)  # 红色 - 未知
                    else:
                        color = (0, 255, 0)  # 绿色 - 已知
                    
                    # 绘制矩形框
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                    
                    # 显示姓名和相似度
                    label = f"{name} ({similarity:.0f}%)"
                    
                    # 使用PIL绘制中文
                    frame = self.draw_chinese_text(
                        frame,
                        label,
                        (x, y - 10 if y > 30 else y + 10),
                        font_size=20,
                        color=color
                    )
                    
                    # 如果是陌生人，且距离上次提示超过10秒
                    if name == "？？？":
                        current_time = time.time()
                        if current_time - self.last_unknown_time > 10:
                            self.last_unknown_time = current_time
                            self.last_unknown_face = face_equalized.copy()
                            
                            # 提示用户录入（在控制台）
                            print(f"\n{'='*60}")
                            print(f"检测到新用户！")
                            print(f"请在控制台按 'n' 键录入新用户，或按 'i' 键忽略")
                            print(f"{'='*60}\n")
                
                # 显示用户数
                stats = self.recognizer.get_stats()
                frame = self.draw_chinese_text(
                    frame,
                    f"Users: {stats['users']}",
                    (10, 30),
                    font_size=24,
                    color=(0, 255, 0)
                )
                
                # 转换为tkinter可用的格式
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(image=img)
                
                # 在主线程中更新显示
                self.root.after(0, self.update_display, img_tk)
                
                # 控制帧率
                time.sleep(0.03)
                
            except Exception as e:
                print(f"⚠️  视频处理错误: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(0.1)
        
        print("🎥 视频处理线程已停止")
    
    def update_display(self, img_tk):
        """在主线程中更新显示"""
        self.video_label.imgtk = img_tk
        self.video_label.configure(image=img_tk)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FaceRecognitionApp(root)
        print("\n" + "="*60)
        print("✅ 程序已启动！")
        print("📌 点击'启动摄像头'开始识别人脸")
        print("📌 点击'停止摄像头'停止识别")
        print("📌 点击右上角关闭按钮退出程序")
        print("="*60 + "\n")
        root.mainloop()
    except Exception as e:
        print(f"\n❌ 程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
