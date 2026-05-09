#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
识别人类 - 完整版
功能：人脸识别 + 用户管理 + 多角度特征强化
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import time
from face_recognizer import FaceRecognizer
from new_user_dialog import NewUserDialog

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类 - 人脸识别系统")
        self.root.geometry("900x650")
        
        self.running = False
        self.cap = None
        
        # 初始化人脸识别器
        print("正在初始化人脸识别器...")
        self.recognizer = FaceRecognizer()
        print(f"数据库统计: {self.recognizer.get_stats()}")
        
        # 用于跟踪已处理的人脸（避免重复弹窗）
        self.processed_faces = {}
        self.last_popup_time = {}
        
        # 添加用户时的锁定标志（避免并发问题）
        self.is_adding_user = False
        self.adding_face_id = None
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部控制栏
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 启动按钮
        self.start_btn = tk.Button(
            control_frame, 
            text="▶ 启动摄像头", 
            command=self.start_camera,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 10, "bold"),
            padx=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # 停止按钮
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ 停止",
            command=self.stop_camera,
            state=tk.DISABLED,
            bg="#f44336",
            fg="white",
            font=("微软雅黑", 10, "bold"),
            padx=10
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 统计信息
        stats = self.recognizer.get_stats()
        self.stats_label = tk.Label(
            control_frame,
            text=f"用户数: {stats['users']} | 特征数: {stats['features']}",
            font=("微软雅黑", 9),
            bg="#f0f0f0",
            fg="#666"
        )
        self.stats_label.pack(side=tk.RIGHT, padx=10)
        
        # 状态标签
        self.status_label = tk.Label(
            control_frame,
            text="状态: 未启动",
            font=("微软雅黑", 9),
            bg="#f0f0f0",
            fg="gray"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # 视频显示区域
        video_frame = tk.Frame(self.root, bg="black")
        video_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.video_label = tk.Label(video_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # 底部说明
        info_frame = tk.Frame(self.root, bg="#e8e8e8")
        info_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        info_text = (
            "💡 使用说明：\n"
            "• 检测到新人物时会自动弹出录入窗口\n"
            "• 同一人会从不同角度自动强化识别\n"
            "• 不认识的人会显示'？？？'"
        )
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("微软雅黑", 8),
            bg="#e8e8e8",
            fg="#666",
            justify=tk.LEFT
        )
        info_label.pack(padx=10, pady=5)
    
    def start_camera(self):
        """启动摄像头"""
        try:
            if self.running:
                return
            
            print("[尝试] 打开摄像头...")
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("[错误] 无法打开摄像头")
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", 
                    "无法打开摄像头\n\n请检查：\n1. 摄像头是否被其他程序占用\n2. Windows摄像头权限是否开启"
                ))
                return
            
            # 测试读取一帧
            ret, frame = self.cap.read()
            if not ret:
                print("[错误] 无法读取摄像头画面")
                self.cap.release()
                self.cap = None
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", 
                    "无法读取摄像头画面\n\n请检查摄像头连接"
                ))
                return
                
            print("[成功] 摄像头已启动")
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="状态: 运行中 ✓", fg="green")
            
            # 重置已处理人脸记录
            self.processed_faces = {}
            self.last_popup_time = {}
            
            # 在单独线程中处理视频
            self.video_thread = threading.Thread(target=self.process_video, daemon=True)
            self.video_thread.start()
            
        except Exception as e:
            print(f"[错误] 启动摄像头失败: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("错误", f"启动摄像头失败:\n{e}"))
    
    def stop_camera(self):
        """停止摄像头"""
        print("[停止] 关闭摄像头...")
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止", fg="gray")
        print("[完成] 摄像头已关闭")
    
    def process_video(self):
        """处理视频流"""
        frame_count = 0
        process_interval = 2  # 每2帧处理一次
        
        while self.running and self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("[警告] 无法读取帧，退出视频处理")
                break
            
            frame_count += 1
            
            # 跳帧处理
            if frame_count % process_interval == 0:
                processed_frame, results = self.process_frame(frame)
                
                # 更新结果
                self.root.after(0, self.update_results, results)
            else:
                processed_frame = frame.copy()
            
            # 转换为PIL图像并显示
            try:
                img = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
                display_width = min(800, self.video_label.winfo_width() - 10 if self.video_label.winfo_width() > 10 else 800)
                display_height = int(display_width * frame.shape[0] / frame.shape[1])
                img = img.resize((display_width, display_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(image=img)
                
                self.root.after(0, lambda: self.video_label.config(image=img_tk))
                self.video_label.image = img_tk
            except Exception as e:
                print(f"[错误] 显示帧失败: {e}")
            
            time.sleep(0.033)
        
        self.root.after(0, self.stop_camera)
    
    def process_frame(self, frame):
        """处理单帧图像"""
        results = []
        
        try:
            # 使用OpenCV检测人脸
            faces = self.recognizer.detect_faces(frame)
            
            for (x, y, w, h) in faces:
                # 提取并预处理人脸
                face_img = self.recognizer.get_face_image(frame, x, y, w, h)
                
                # 如果正在添加用户，跳过识别
                if self.is_adding_user:
                    results.append({
                        'box': (x, y, w, h),
                        'name': '录入中...',
                        'confidence': 0
                    })
                    continue
                
                # 识别人脸
                name, confidence = self.recognizer.recognize_face(face_img)
                
                # 打印识别信息用于调试
                print(f"[识别] 姓名: {name}, 置信度: {confidence:.2f} (越低越相似)")
                
                # 如果是陌生人，检查是否需要弹窗
                if name == "？？？":
                    # 使用时间戳毫秒值作为唯一ID
                    face_id = f"{int(time.time() * 1000)}"
                    current_time = time.time()
                    
                    # 如果这个人脸ID正在处理中，跳过
                    if face_id == self.adding_face_id:
                        continue
                    
                    # 如果这个位置的人脸超过10秒没有弹窗，则弹出（增加时间间隔）
                    if face_id not in self.last_popup_time or \
                       current_time - self.last_popup_time[face_id] > 10:
                        self.last_popup_time[face_id] = current_time
                        
                        print(f"[提示] 检测到新用户，准备弹出录入窗口")
                        # 在主线程中弹出对话框
                        self.root.after(0, self.show_new_user_dialog, face_img, face_id)
                
                results.append({
                    'box': (x, y, w, h),
                    'name': name,
                    'confidence': confidence
                })
                    
        except Exception as e:
            print(f"[错误] 处理帧失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 绘制结果
        if results:
            frame = self.draw_results(frame, results)
        
        return frame, results
    
    def show_new_user_dialog(self, face_img, face_id):
        """显示新用户录入对话框"""
        # 设置锁定标志，暂停识别
        self.is_adding_user = True
        self.adding_face_id = face_id
        print(f"[锁定] 开始录入用户，face_id: {face_id}")
        
        def on_user_added(name):
            if name:
                try:
                    # 训练模型
                    self.recognizer.train_with_new_face(name, face_img)
                    # 更新统计信息
                    stats = self.recognizer.get_stats()
                    self.stats_label.config(
                        text=f"用户数: {stats['users']} | 特征数: {stats['features']}"
                    )
                    messagebox.showinfo("成功", f"已成功录入用户: {name}\n\n多角度识别将自动强化！")
                finally:
                    # 解锁，恢复识别
                    self.is_adding_user = False
                    self.adding_face_id = None
                    # 清除该face_id的弹窗记录，允许下次检测
                    if face_id in self.last_popup_time:
                        del self.last_popup_time[face_id]
                    print(f"[解锁] 用户录入完成，恢复识别")
            else:
                # 用户取消，也要解锁
                self.is_adding_user = False
                self.adding_face_id = None
                print(f"[解锁] 用户取消录入，恢复识别")
        
        dialog = NewUserDialog(self.root, on_user_added)
        dialog.show()
    
    def draw_results(self, frame, results):
        """在帧上绘制识别结果（支持中文）"""
        # 将OpenCV的BGR图像转换为PIL的RGB图像
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)
        draw = ImageDraw.Draw(pil_image)
        
        # 加载中文字体
        try:
            font_large = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)
            font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        for result in results:
            x, y, w, h = result['box']
            name = result['name']
            confidence = result.get('confidence', 0)
            
            # 根据姓名选择颜色
            if name == "？？？":
                color = (255, 100, 100)  # 红色 - 未知
            elif name == '录入中...':
                color = (255, 255, 100)  # 黄色 - 录入中
            else:
                color = (100, 255, 100)  # 绿色 - 已知
            
            # 绘制矩形框
            draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
            
            # 准备文本 - 显示姓名和置信度
            if name == '录入中...':
                name_text = name
            else:
                # 置信度越低表示越相似，转换为相似度百分比
                similarity = max(0, 100 - confidence)
                name_text = f"{name} ({similarity:.0f}%)"
            
            # 绘制姓名文本（在矩形框上方）
            text_y = y - 5
            if text_y < 30:
                text_y = y + 30
            
            # 绘制背景矩形
            bbox = draw.textbbox((x, text_y - 22), name_text, font=font_large)
            draw.rectangle([x, text_y - 24, bbox[2] + 5, text_y + 2], fill=color)
            draw.text((x + 2, text_y - 22), name_text, fill=(0, 0, 0), font=font_large)
        
        # 将PIL图像转回OpenCV格式
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return frame
    
    def update_results(self, results):
        """更新结果显示（预留，可用于侧边栏显示）"""
        pass


def main():
    print("\n" + "="*60)
    print("正在启动识别人类系统...")
    print("="*60 + "\n")
    
    try:
        root = tk.Tk()
        print("✓ tkinter根窗口创建成功")
        
        # 居中显示
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 650) // 2
        root.geometry(f"900x650+{x}+{y}")
        print(f"✓ 窗口位置已设置: 900x650+{x}+{y}")
        
        app = FaceRecognitionApp(root)
        print("✓ 应用程序初始化完成")
        
        print("窗口已创建，准备显示...")
        
        # 处理窗口关闭事件
        def on_closing():
            print("正在关闭程序...")
            app.stop_camera()
            root.destroy()
            print("程序已退出")
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("显示窗口...")
        print("="*60)
        print("程序正在运行，请操作界面")
        print("="*60)
        root.mainloop()
        
        print("\n程序已正常退出")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"错误: {e}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"\n{'='*60}")
        input("\n按回车键退出...")


if __name__ == "__main__":
    main()
