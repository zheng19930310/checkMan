#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
人脸数据库管理模块
使用SQLite存储用户信息和人脸特征
"""

import sqlite3
import numpy as np
import pickle
import os
from datetime import datetime

class FaceDatabase:
    def __init__(self, db_path="faces.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建人脸特征表（一个人可以有多个特征）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                encoding BLOB NOT NULL,
                angle TEXT DEFAULT 'unknown',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, name):
        """添加新用户"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            # 用户已存在
            return self.get_user_by_name(name)['id']
    
    def get_user_by_name(self, name):
        """根据姓名查找用户"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def get_all_users(self):
        """获取所有用户"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def add_face_feature(self, user_id, encoding, angle='unknown'):
        """添加人脸特征（支持多角度）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # encoding已经是bytes了，直接保存
        cursor.execute(
            'INSERT INTO face_features (user_id, encoding, angle) VALUES (?, ?, ?)',
            (user_id, encoding, angle)
        )
        conn.commit()
        conn.close()
    
    def get_all_face_features(self):
        """获取所有人脸特征"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ff.*, u.name 
            FROM face_features ff 
            JOIN users u ON ff.user_id = u.id
        ''')
        features = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return features
    
    def get_user_features(self, user_id):
        """获取指定用户的所有特征"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM face_features WHERE user_id = ?', (user_id,))
        features = []
        for row in cursor.fetchall():
            feature = dict(row)
            feature['encoding'] = pickle.loads(feature['encoding'])
            features.append(feature)
        conn.close()
        return features
    
    def delete_user(self, user_id):
        """删除用户及其所有特征"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM face_features')
        feature_count = cursor.fetchone()[0]
        conn.close()
        return {'users': user_count, 'features': feature_count}


if __name__ == "__main__":
    # 测试
    db = FaceDatabase()
    print("数据库初始化成功")
    print(f"统计: {db.get_stats()}")
