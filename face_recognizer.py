#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
人脸识别模块
使用OpenCV LBPH进行人脸识别（轻量级，无需额外依赖）
"""

import cv2
import numpy as np
import os
import pickle
from face_db import FaceDatabase

class FaceRecognizer:
    def __init__(self):
        self.db = FaceDatabase()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map = {}  # ID到姓名的映射
        self.reverse_label_map = {}  # 姓名到ID的映射
        self.next_id = 0
        self.load_known_faces()
        # 加载后立即训练模型
        if len(self.label_map) > 0:
            self.retrain_model()
    
    def load_known_faces(self):
        """从数据库加载已知人脸"""
        users = self.db.get_all_users()
        self.label_map = {}
        self.reverse_label_map = {}
        
        for user in users:
            user_id = user['id']
            name = user['name']
            self.label_map[user_id] = name
            self.reverse_label_map[name] = user_id
            if user_id >= self.next_id:
                self.next_id = user_id + 1
        
        print(f"已加载 {len(self.label_map)} 个用户")
    
    def detect_faces(self, frame):
        """检测人脸位置（使用Haar Cascade）"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces
    
    def get_face_image(self, frame, x, y, w, h):
        """提取并预处理人脸图像"""
        # 增加边距
        margin = 10
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(frame.shape[1], x + w + margin)
        y2 = min(frame.shape[0], y + h + margin)
        
        face_img = frame[y1:y2, x1:x2]
        
        # 转换为灰度图
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 调整大小为统一尺寸
        gray = cv2.resize(gray, (200, 200))
        
        # 直方图均衡化
        gray = cv2.equalizeHist(gray)
        
        return gray
    
    def recognize_face(self, face_img):
        """识别人脸，返回姓名和置信度"""
        if len(self.label_map) == 0:
            return "？？？", 0
        
        try:
            # 检查模型是否已训练
            # 尝试获取模型状态，如果未训练会抛出异常
            try:
                # LBPH模型有一个空预测的技巧来检查是否已训练
                test_img = np.zeros((200, 200), dtype=np.uint8)
                self.recognizer.predict(test_img)
            except cv2.error:
                # 模型未训练，返回未知
                print("[识别器] 模型尚未训练，跳过识别")
                return "？？？", 0
            
            # 尝试识别
            label, confidence = self.recognizer.predict(face_img)
            
            # LBPH算法：置信度越低表示越相似
            # 阈值设为100，更宽松，允许多角度识别
            threshold = 100
            
            print(f"[识别器] label={label}, confidence={confidence:.2f}, threshold={threshold}")
            
            if confidence < threshold and label in self.label_map:
                return self.label_map[label], confidence
            else:
                return "？？？", confidence
        except Exception as e:
            print(f"识别错误: {e}")
            import traceback
            traceback.print_exc()
            return "？？？", 0
    
    def train_with_new_face(self, name, face_img):
        """用新人脸训练或更新模型"""
        # 获取或创建用户ID
        if name in self.reverse_label_map:
            user_id = self.reverse_label_map[name]
            print(f"更新用户 {name} (ID: {user_id})")
        else:
            # 先添加到数据库，获取真实的数据库ID
            db_user_id = self.db.add_user(name)
            
            # 使用数据库返回的ID
            user_id = db_user_id
            self.label_map[user_id] = name
            self.reverse_label_map[name] = user_id
            
            # 更新next_id
            if user_id >= self.next_id:
                self.next_id = user_id + 1
            
            print(f"添加新用户 {name} (数据库ID: {user_id})")
        
        # 保存人脸图像到数据库
        # 注意：face_img已经是灰度图，需要转换为3通道以便imencode正确处理
        if len(face_img.shape) == 2:
            # 灰度图转3通道
            face_img_3ch = cv2.cvtColor(face_img, cv2.COLOR_GRAY2BGR)
        else:
            face_img_3ch = face_img
        
        _, img_encoded = cv2.imencode('.png', face_img_3ch)
        
        if img_encoded is not None:
            img_bytes = img_encoded.tobytes()
            print(f"[保存] 人脸特征数据大小: {len(img_bytes)} bytes")
            self.db.add_face_feature(user_id, img_bytes)
        else:
            print("[保存] 错误: 无法编码图像")
            raise Exception("图像编码失败")
        
        # 重新训练模型
        self.retrain_model()
    
    def retrain_model(self):
        """重新训练识别模型"""
        features = self.db.get_all_face_features()
        
        print(f"[训练] 从数据库读取到 {len(features)} 个特征")
        
        if len(features) == 0:
            print("没有数据可训练")
            return
        
        images = []
        labels = []
        
        for idx, feature in enumerate(features):
            user_id = feature['user_id']
            img_bytes = feature['encoding']
            
            if img_bytes is None or len(img_bytes) == 0:
                print(f"[训练] 特征 {idx+1} 数据为空，跳过")
                continue
            
            try:
                # 方式1: 尝试用pickle反序列化
                img = pickle.loads(img_bytes)
                if isinstance(img, np.ndarray):
                    # 确保是灰度图
                    if len(img.shape) == 3:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # 确保尺寸正确
                    if img.shape != (200, 200):
                        img = cv2.resize(img, (200, 200))
                    images.append(img)
                    labels.append(user_id)
                    print(f"[训练] 特征 {idx+1} 使用pickle解码成功 (用户ID: {user_id})")
                    continue
            except Exception as e:
                pass
            
            # 方式2: 尝试作为图像bytes解码
            try:
                img_array = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
                
                if img is not None and img.size > 0:
                    # 确保尺寸正确
                    if img.shape != (200, 200):
                        img = cv2.resize(img, (200, 200))
                    images.append(img)
                    labels.append(user_id)
                    print(f"[训练] 特征 {idx+1} 使用imdecode解码成功 (用户ID: {user_id})")
                    continue
            except Exception as e:
                pass
            
            # 方式3: 尝试作为RGB图像解码
            try:
                img_array = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                
                if img is not None and img.size > 0:
                    # 转换为灰度图
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # 确保尺寸正确
                    if img.shape != (200, 200):
                        img = cv2.resize(img, (200, 200))
                    images.append(img)
                    labels.append(user_id)
                    print(f"[训练] 特征 {idx+1} 使用RGB解码成功 (用户ID: {user_id})")
                    continue
            except Exception as e:
                pass
            
            print(f"[训练] 警告: 无法解码特征 {idx+1} (用户ID: {user_id}, 数据长度: {len(img_bytes)})")
        
        print(f"[训练] 成功解码 {len(images)} 张图像")
        
        if len(images) > 0:
            # 训练模型
            self.recognizer.train(images, np.array(labels))
            print(f"✓ 模型训练完成，共{len(images)}张图像")
        else:
            print("⚠️  警告: 没有有效的图像数据可训练")
            print("提示: 可能是数据库中的特征数据格式不正确")
            print("建议: 删除旧的数据库文件 faces.db，重新开始录入")
        
        # 更新映射
        self.load_known_faces()
    
    def get_stats(self):
        """获取统计信息"""
        return self.db.get_stats()


if __name__ == "__main__":
    recognizer = FaceRecognizer()
    print("人脸识别器初始化成功")
    print(f"统计: {recognizer.get_stats()}")
