# utils.py - 工具函数模块
# 注意：此文件需要torch和torchvision，如果不使用PyTorch模型可以忽略
try:
    import torch
    import cv2
    import numpy as np
    from PIL import Image
    from torchvision import transforms
    from model import create_model
    import os
except ImportError:
    # 如果没有安装torch，只提供基础功能
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

def load_model(device, model_path=None):
    """加载预训练模型"""
    model = create_model()
    model.to(device)
    model.eval()
    
    # 如果有预训练权重则加载
    if model_path and os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        print(f"从 {model_path} 加载模型权重")
    else:
        print("使用随机初始化的模型（实际应用中应加载预训练权重）")
    
    return model

def detect_faces(frame, min_size=(30, 30)):
    """检测人脸"""
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 使用Haar Cascade检测人脸
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=min_size
    )
    
    return faces

def preprocess_frame(frame):
    """预处理视频帧"""
    # 检测人脸
    faces = detect_faces(frame)
    
    return frame, faces

# 全局字体缓存
_chinese_font_large = None
_chinese_font_small = None

def _load_chinese_fonts():
    """加载中文字体（仅一次）"""
    global _chinese_font_large, _chinese_font_small
    if _chinese_font_large is not None:
        return _chinese_font_large, _chinese_font_small
    
    try:
        from PIL import ImageFont
        # Windows系统字体
        font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
        _chinese_font_large = ImageFont.truetype(font_path, 20)
        _chinese_font_small = ImageFont.truetype(font_path, 16)
    except:
        try:
            from PIL import ImageFont
            # 备选字体
            font_path = "C:/Windows/Fonts/simsun.ttc"  # 宋体
            _chinese_font_large = ImageFont.truetype(font_path, 20)
            _chinese_font_small = ImageFont.truetype(font_path, 16)
        except:
            from PIL import ImageFont
            # 如果都失败，使用默认字体
            _chinese_font_large = ImageFont.load_default()
            _chinese_font_small = ImageFont.load_default()
    
    return _chinese_font_large, _chinese_font_small

def draw_results(frame, results):
    """在帧上绘制识别结果（支持中文）"""
    from PIL import Image, ImageDraw
    import numpy as np
    
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
