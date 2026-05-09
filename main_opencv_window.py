#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
识别人类 - OpenCV窗口版
使用OpenCV原生窗口，避免tkinter兼容性问题
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
from face_recognizer import FaceRecognizer

class OpenCVFaceRecognitionApp:
    def __init__(self):
        # 初始化人脸识别器
        print("正在初始化人脸识别器...")
        self.recognizer = FaceRecognizer()
        stats = self.recognizer.get_stats()
        print(f"已加载 {stats['users']} 个用户，{stats['features']} 个特征")
        
        self.cap = None
        self.running = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # 用于跟踪新用户（避免重复提示）
        self.last_unknown_time = 0
        self.last_unknown_face = None
        
    def start_camera(self):
        """启动摄像头"""
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print(" 无法打开摄像头")
            return False
        
        print("✅ 摄像头已启动")
        self.running = True
        return True
    
    def stop_camera(self):
        """停止摄像头"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        print("✅ 摄像头已停止")
    
    def draw_chinese_text(self, img, text, position, font_size=24, color=(255, 255, 255)):
        """在图像上绘制中文文本"""
        # 尝试加载字体
        font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            # 如果加载失败，使用默认字体
            font = ImageFont.load_default()
        
        # 转换为PIL图像
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        draw.text(position, text, font=font, fill=color)
        
        # 转换回OpenCV格式
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def recognize_and_display(self):
        """识别并显示"""
        if not self.cap or not self.cap.isOpened():
            print("❌ 摄像头未启动")
            return
        
        # 获取统计信息
        stats = self.recognizer.get_stats()
        
        print("\n" + "="*60)
        print("开始识别，按 'q' 键退出")
        print("="*60 + "\n")
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ 无法读取摄像头画面")
                break
            
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
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
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
                        print(f"请按 'n' 键录入新用户，或按 'i' 键忽略")
                        print(f"{'='*60}\n")
            
            # 显示帧数
            cv2.putText(frame, f"Users: {stats['users']}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # 显示画面
            cv2.imshow('识别人类 - 人脸识别系统', frame)
            
            # 处理键盘输入
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n退出程序...")
                break
            elif key == ord('n') and self.last_unknown_face is not None:
                # 录入新用户
                self.add_new_user(self.last_unknown_face)
            elif key == ord('i'):
                # 忽略当前提示
                print("已忽略")
                self.last_unknown_time = time.time()
        
        self.stop_camera()
    
    def add_new_user(self, face_img):
        """添加新用户"""
        print("\n" + "="*60)
        print("录入新用户")
        print("="*60)
        
        name = input("请输入用户姓名: ").strip()
        
        if not name:
            print("❌ 姓名不能为空")
            return
        
        try:
            # 添加用户和人脸特征
            self.recognizer.add_user_and_face(name, face_img)
            print(f"✅ 成功录入用户: {name}")
            
            # 更新统计
            stats = self.recognizer.get_stats()
            print(f"当前用户数: {stats['users']}, 特征数: {stats['features']}")
        except Exception as e:
            print(f"❌ 录入失败: {e}")
        
        print("="*60 + "\n")
    
    def run(self):
        """运行程序"""
        print("\n" + "="*60)
        print("识别人类 - OpenCV版")
        print("="*60 + "\n")
        
        if not self.start_camera():
            return
        
        try:
            self.recognize_and_display()
        except KeyboardInterrupt:
            print("\n用户中断")
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop_camera()

if __name__ == "__main__":
    try:
        app = OpenCVFaceRecognitionApp()
        app.run()
    except Exception as e:
        print(f"\n❌ 程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
