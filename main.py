import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time

# 导入模型和工具函数
from model import GenderAgeNet
from utils import load_model, preprocess_frame, draw_results

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类 - 性别年龄识别系统")
        self.root.geometry("800x600")
        
        # 控制变量
        self.running = False
        self.cap = None
        self.model = None
        self.device = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化模型
        self.init_model()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(self.root, text="识别人类 - 性别年龄识别系统", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 摄像头显示区域
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack(pady=10)
        
        # 结果显示区域
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)
        
        self.result_label = tk.Label(self.result_frame, text="等待启动...", font=("Arial", 12))
        self.result_label.pack()
        
        # 控制按钮
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=20)
        
        self.start_button = tk.Button(self.control_frame, text="启动摄像头", command=self.start_camera, bg="green", fg="white", font=("Arial", 12))
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(self.control_frame, text="关闭摄像头", command=self.stop_camera, bg="red", fg="white", font=("Arial", 12))
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.config(state=tk.DISABLED)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="状态: 未启动", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
    def init_model(self):
        """初始化模型"""
        try:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            print(f"使用设备: {self.device}")
            
            self.model = load_model(self.device)
            print("模型加载成功！")
        except Exception as e:
            print(f"模型加载失败: {e}")
            messagebox.showerror("错误", f"模型加载失败: {e}")
            
    def start_camera(self):
        """启动摄像头"""
        if self.running:
            return
            
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开摄像头")
            return
            
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="状态: 运行中")
        
        # 在单独线程中处理视频
        self.video_thread = threading.Thread(target=self.process_video, daemon=True)
        self.video_thread.start()
        
    def stop_camera(self):
        """停止摄像头"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止")
        self.result_label.config(text="摄像头已关闭")
        
    def process_video(self):
        """处理视频流"""
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            # 处理帧并获取结果
            processed_frame, results = self.process_frame(frame)
            
            # 转换为PIL图像并显示
            img = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
            img = img.resize((640, 480))
            img_tk = ImageTk.PhotoImage(image=img)
            
            # 更新UI
            self.video_frame.config(image=img_tk)
            self.video_frame.image = img_tk
            
            # 更新结果
            if results:
                result_text = f"检测到 {len(results)} 个人\n"
                for i, result in enumerate(results):
                    result_text += f"人员{i+1}: {result['gender']} (置信度:{result['gender_conf']:.1f}%), 年龄:{result['age']}岁\n"
                self.result_label.config(text=result_text)
            else:
                self.result_label.config(text="未检测到人脸")
            
            time.sleep(0.03)  # 约30fps
            
    def process_frame(self, frame):
        """处理单帧图像"""
        # 预处理帧
        processed_frame, face_boxes = preprocess_frame(frame)
        
        results = []
        
        # 如果检测到人脸，进行预测
        if len(face_boxes) > 0 and self.model:
            for face_box in face_boxes:
                x, y, w, h = face_box
                
                # 提取人脸区域
                face_img = frame[y:y+h, x:x+w]
                
                if face_img.size == 0:
                    continue
                
                # 转换颜色空间并调整大小
                face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                face_pil = Image.fromarray(face_rgb)
                
                # 应用变换
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                       std=[0.229, 0.224, 0.225])
                ])
                
                face_tensor = transform(face_pil).unsqueeze(0).to(self.device)
                
                # 进行预测
                with torch.no_grad():
                    gender_pred, age_pred = self.model(face_tensor)
                    
                    # 处理性别预测
                    gender_probs = torch.softmax(gender_pred, dim=1)
                    gender_conf, gender_class = torch.max(gender_probs, 1)
                    gender_label = "男性" if gender_class.item() == 0 else "女性"
                    gender_confidence = gender_conf.item() * 100
                    
                    # 处理年龄预测
                    age = age_pred.item()
                    
                    results.append({
                        'box': (x, y, w, h),
                        'gender': gender_label,
                        'gender_conf': gender_confidence,
                        'age': int(age)
                    })
            
            # 在画面上绘制结果
            processed_frame = draw_results(processed_frame, results)
        
        return processed_frame, results

def main():
    """主函数"""
    root = tk.Tk()
    app = CameraApp(root)
    
    # 处理窗口关闭事件
    def on_closing():
        app.stop_camera()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
