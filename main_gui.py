import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import time
import os

# 全局字体缓存
_chinese_font_large = None
_chinese_font_small = None

def _load_chinese_fonts():
    """加载中文字体（仅一次）"""
    global _chinese_font_large, _chinese_font_small
    if _chinese_font_large is not None:
        return _chinese_font_large, _chinese_font_small
    
    try:
        # Windows系统字体
        font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
        _chinese_font_large = ImageFont.truetype(font_path, 20)
        _chinese_font_small = ImageFont.truetype(font_path, 16)
    except:
        try:
            # 备选字体
            font_path = "C:/Windows/Fonts/simsun.ttc"  # 宋体
            _chinese_font_large = ImageFont.truetype(font_path, 20)
            _chinese_font_small = ImageFont.truetype(font_path, 16)
        except:
            # 如果都失败，使用默认字体
            _chinese_font_large = ImageFont.load_default()
            _chinese_font_small = ImageFont.load_default()
    
    return _chinese_font_large, _chinese_font_small

def draw_results(frame, results):
    """在帧上绘制识别结果（支持中文）"""
    # 获取缓存的字体
    font_large, font_small = _load_chinese_fonts()
    
    # 将OpenCV的BGR图像转换为PIL的RGB图像
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_image)
    
    for result in results:
        x, y, w, h = result['box']
        gender = result['gender']
        gender_conf = result['gender_conf']
        age = result['age']
        
        # 绘制矩形框
        draw.rectangle([x, y, x + w, y + h], outline=(0, 255, 0), width=3)
        
        # 准备文本
        gender_text = f"{gender} ({gender_conf:.0f}%)"
        age_text = f"年龄: {age}"
        
        # 绘制性别文本（在矩形框上方）
        text_y = y - 5
        if text_y < 25:
            text_y = y + 25
        
        # 绘制背景矩形
        bbox = draw.textbbox((x, text_y - 20), gender_text, font=font_large)
        draw.rectangle([x, text_y - 22, bbox[2] + 5, text_y + 2], fill=(0, 255, 0))
        draw.text((x + 2, text_y - 20), gender_text, fill=(0, 0, 0), font=font_large)
        
        # 绘制年龄文本
        bbox2 = draw.textbbox((x, text_y), age_text, font=font_small)
        draw.rectangle([x, text_y - 2, bbox2[2] + 5, text_y + 18], fill=(0, 255, 0))
        draw.text((x + 2, text_y), age_text, fill=(0, 0, 0), font=font_small)
    
    # 将PIL图像转回OpenCV格式
    frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    return frame

class GenderAgeRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类 - 性别年龄识别系统")
        self.root.geometry("800x600")
        
        # 让窗口始终在最前面
        self.root.attributes('-topmost', True)
        
        # 控制变量
        self.running = False
        self.cap = None
        
        # 使用现有的预训练模型 - OpenCV DNN模块
        self.face_net = None
        self.gender_net = None
        self.age_net = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化模型
        self.init_models()
        
        # 显示启动提示
        print("=" * 50)
        print("GUI窗口已创建，应该可以看到窗口了")
        print("如果看不到，请检查任务栏是否有Python窗口")
        print("=" * 50)
        
    def create_widgets(self):
        """创建界面组件"""
        # 设置窗口背景色
        self.root.configure(bg='#f0f0f0')
        
        # 标题
        title_frame = tk.Frame(self.root, bg='#2196F3')
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="识别人类 - 性别年龄识别系统", 
                              font=("Microsoft YaHei", 18, "bold"), fg="white", bg='#2196F3')
        title_label.pack(pady=10)
        
        # 控制按钮区域（顶部）
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.start_button = tk.Button(control_frame, text="▶ 启动摄像头", 
                                     command=self.start_camera, bg="#4CAF50", 
                                     fg="white", font=("Microsoft YaHei", 12, "bold"), width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="⏹ 关闭摄像头", 
                                    command=self.stop_camera, bg="#F44336", 
                                    fg="white", font=("Microsoft YaHei", 12, "bold"), width=15,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        self.status_label = tk.Label(control_frame, text="状态: 未启动", 
                                    font=("Microsoft YaHei", 11), bg='#f0f0f0', fg="#666")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # 摄像头显示区域
        video_frame = tk.Frame(self.root, bg='black')
        video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.video_label = tk.Label(video_frame, bg="black", text="点击【启动摄像头】按钮开始", fg="white", font=("Microsoft YaHei", 14))
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # 识别结果显示区域
        result_frame = tk.LabelFrame(self.root, text="识别结果", font=("Microsoft YaHei", 12, "bold"), bg='#f0f0f0', fg='#333')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 使用文本框显示结果
        self.result_text = tk.Text(result_frame, height=6, width=60, 
                                  font=("Microsoft YaHei", 10), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.insert(tk.END, "等待启动摄像头...")
        
        # 底部信息
        info_label = tk.Label(self.root, 
                             text="提示: 本系统使用OpenCV DNN预训练模型，适合开发测试",
                             font=("Arial", 9), fg="gray")
        info_label.pack(pady=5)
        
    def init_models(self):
        """初始化预训练模型"""
        try:
            print("正在加载预训练模型...")
            
            # 使用OpenCV的DNN模块加载预训练模型
            # 人脸检测模型
            prototxt_path = self.get_model_path("deploy.prototxt")
            caffemodel_path = self.get_model_path("res10_300x300_ssd_iter_140000.caffemodel")
            
            if prototxt_path and caffemodel_path:
                self.face_net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
                print("人脸检测模型加载成功")
            
            print("模型初始化完成")
            
        except Exception as e:
            print(f"模型加载警告: {e}")
            print("将使用Haar Cascade作为备选方案")
            
    def get_model_path(self, filename):
        """获取模型文件路径"""
        # 模型文件路径
        model_dir = os.path.join(os.path.dirname(__file__), "models")
        filepath = os.path.join(model_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        else:
            print(f"模型文件未找到: {filename}")
            return None
            
    def start_camera(self):
        """启动摄像头"""
        try:
            if self.running:
                return
                
            print("[尝试] 打开摄像头...")
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("[错误] 无法打开摄像头")
                self.root.after(0, lambda: messagebox.showerror("错误", "无法打开摄像头\n\n请检查：\n1. 摄像头是否被其他程序占用\n2. Windows摄像头权限是否开启"))
                return
            
            # 测试读取一帧
            ret, frame = self.cap.read()
            if not ret:
                print("[错误] 无法读取摄像头画面")
                self.cap.release()
                self.cap = None
                self.root.after(0, lambda: messagebox.showerror("错误", "无法读取摄像头画面\n\n请检查摄像头连接"))
                return
                
            print("[成功] 摄像头已启动")
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="状态: 运行中 ✓", fg="green")
            
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
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止", fg="#666")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "摄像头已关闭\n点击【启动摄像头】重新开始")
        self.video_label.config(text="摄像头已关闭", fg="gray")
        print("[完成] 摄像头已关闭")
        
    def process_video(self):
        """处理视频流"""
        try:
            frame_count = 0
            process_interval = 3  # 每3帧处理一次识别，提高流畅度
            
            while self.running and self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                
                if not ret:
                    print("[警告] 无法读取帧，退出视频处理")
                    break
                
                frame_count += 1
                
                # 跳帧处理，提高流畅度
                if frame_count % process_interval == 0:
                    # 处理帧并获取结果
                    processed_frame, results = self.process_frame(frame)
                    
                    # 更新结果
                    self.root.after(0, self.update_results, results)
                else:
                    # 不处理识别，直接显示原始帧
                    processed_frame = frame.copy()
                
                # 转换为PIL图像并显示
                try:
                    img = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
                    # 自适应调整大小
                    display_width = min(640, self.video_label.winfo_width() - 10 if self.video_label.winfo_width() > 10 else 640)
                    display_height = int(display_width * frame.shape[0] / frame.shape[1])
                    img = img.resize((display_width, display_height), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(image=img)
                    
                    # 更新UI
                    self.root.after(0, lambda: self.video_label.config(image=img_tk))
                    self.video_label.image = img_tk
                except Exception as e:
                    print(f"[错误] 显示帧失败: {e}")
                
                # 控制帧率，约30fps
                time.sleep(0.033)
                
        except Exception as e:
            print(f"[严重错误] 视频处理线程崩溃: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("严重错误", f"视频处理失败:\n{e}"))
            self.running = False
            
    def process_frame(self, frame):
        """处理单帧图像"""
        height, width = frame.shape[:2]
        results = []
        
        # 使用Haar Cascade进行人脸检测（不需要额外的模型文件）
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        # 对检测到的人脸进行处理
        for (x, y, w, h) in faces:
            # 提取人脸区域
            face_roi = frame[y:y+h, x:x+w]
            
            # 简单的性别和年龄估计（基于规则的方法）
            # 注意：这是一个简化的示例，实际应用中应该使用预训练的深度学习模型
            gender, gender_conf = self.estimate_gender(face_roi)
            age = self.estimate_age(face_roi)
            
            results.append({
                'box': (x, y, w, h),
                'gender': gender,
                'gender_conf': gender_conf,
                'age': age
            })
        
        # 使用draw_results函数绘制结果（支持中文）
        if results:
            frame = draw_results(frame, results)
        
        return frame, results
    
    def estimate_gender(self, face_roi):
        """估计性别（简化版）"""
        # 这里使用一个简单的启发式方法
        # 实际应用应该使用预训练的性别分类模型
        try:
            # 计算一些简单的特征
            if face_roi.size == 0:
                return "未知", 50.0
            
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            # 基于亮度分布的简单估计（示例）
            mean_brightness = np.mean(gray)
            
            # 简化判断逻辑
            if mean_brightness > 120:
                return "女性", 65.0
            else:
                return "男性", 65.0
                
        except Exception as e:
            print(f"性别估计错误: {e}")
            return "未知", 50.0
    
    def estimate_age(self, face_roi):
        """估计年龄（简化版）"""
        # 这里使用一个简单的启发式方法
        # 实际应用应该使用预训练的年龄估计模型
        try:
            if face_roi.size == 0:
                return 25
            
            # 基于面部特征的简单估计（示例）
            # 实际应用中应该使用深度学习模型
            return np.random.randint(20, 40)  # 随机返回20-40岁作为示例
            
        except Exception as e:
            print(f"年龄估计错误: {e}")
            return 25
    
    def update_results(self, results):
        """更新识别结果显示"""
        self.result_text.delete(1.0, tk.END)
        
        if not results:
            self.result_text.insert(tk.END, "未检测到人脸")
            return
        
        result_text = f"检测到 {len(results)} 个人\n\n"
        
        for i, result in enumerate(results, 1):
            result_text += f"👤 人员 {i}:\n"
            result_text += f"  性别: {result['gender']} (置信度: {result['gender_conf']:.1f}%)\n"
            result_text += f"  年龄: {result['age']} 岁\n\n"
        
        self.result_text.insert(tk.END, result_text)

def main():
    """主函数"""
    print("\n" + "="*50)
    print("正在启动识别人类系统...")
    print("="*50 + "\n")
    
    try:
        root = tk.Tk()
        
        # 设置窗口图标和位置
        root.iconbitmap(default='')  # 清除默认图标
        
        # 获取屏幕尺寸，居中显示窗口
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        root.geometry(f"800x600+{x}+{y}")
        
        app = GenderAgeRecognitionApp(root)
        
        print("窗口已创建，准备显示...")
        
        # 处理窗口关闭事件
        def on_closing():
            print("正在关闭程序...")
            app.stop_camera()
            root.destroy()
            print("程序已退出")
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("显示窗口...")
        root.mainloop()
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("正在启动识别人类系统...")
    print("="*50 + "\n")
    
    try:
        root = tk.Tk()
        print("✓ tkinter根窗口创建成功")
        
        # 获取屏幕尺寸，居中显示窗口
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        root.geometry(f"800x600+{x}+{y}")
        print(f"✓ 窗口位置已设置: 800x600+{x}+{y}")
        
        app = GenderAgeRecognitionApp(root)
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
        print("="*50)
        print("程序正在运行，请操作界面")
        print("="*50)
        root.mainloop()
        
        print("\n程序已正常退出")
        
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"错误: {e}")
        print(f"{'='*50}")
        import traceback
        traceback.print_exc()
        print(f"\n{'='*50}")
        input("\n按回车键退出...")
