import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import time

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类")
        self.root.geometry("800x600")
        
        self.running = False
        self.cap = None
        
        # 创建界面
        frame_top = tk.Frame(root)
        frame_top.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_btn = tk.Button(frame_top, text="启动摄像头", command=self.start_camera, bg="green", fg="white")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(frame_top, text="停止", command=self.stop_camera, state=tk.DISABLED, bg="red", fg="white")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(frame_top, text="状态: 未启动", fg="gray")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        self.video_label = tk.Label(root, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def start_camera(self):
        if self.running:
            return
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开摄像头")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            messagebox.showerror("错误", "无法读取画面")
            return
        
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="状态: 运行中", fg="green")
        
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止", fg="gray")
    
    def process_video(self):
        while self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 简单的人脸检测
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            # 绘制结果（使用Pillow支持中文）
            if len(faces) > 0:
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                draw = ImageDraw.Draw(pil_img)
                
                try:
                    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
                except:
                    font = ImageFont.load_default()
                
                for (x, y, w, h) in faces:
                    draw.rectangle([x, y, x+w, y+h], outline=(0, 255, 0), width=2)
                    draw.text((x, y-25), "人", fill=(0, 255, 0), font=font)
                
                frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
            # 显示
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = img.resize((640, 480))
            img_tk = ImageTk.PhotoImage(image=img)
            
            self.root.after(0, lambda: self.video_label.config(image=img_tk))
            self.video_label.image = img_tk
            
            time.sleep(0.033)
        
        self.root.after(0, self.stop_camera)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
