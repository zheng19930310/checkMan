#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查数据库内容"""

import sqlite3

db_path = "faces.db"

print("="*60)
print("检查数据库内容")
print("="*60)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查用户表
print("\n【用户表】")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print(f"用户数量: {len(users)}")
for user in users:
    print(f"  ID: {user[0]}, 姓名: {user[1]}, 创建时间: {user[2]}")

# 检查特征表
print("\n【人脸特征表】")
cursor.execute("SELECT * FROM face_features")
features = cursor.fetchall()
print(f"特征数量: {len(features)}")
for feature in features:
    print(f"  ID: {feature[0]}, 用户ID: {feature[1]}, 数据大小: {len(feature[2])} bytes, 角度: {feature[3]}, 创建时间: {feature[4]}")

# 测试JOIN查询
print("\n【JOIN查询结果】")
cursor.execute('''
    SELECT ff.*, u.name 
    FROM face_features ff 
    JOIN users u ON ff.user_id = u.id
''')
joined = cursor.fetchall()
print(f"JOIN查询结果数量: {len(joined)}")
for row in joined:
    print(f"  用户: {row[5]}, 特征ID: {row[0]}, 用户ID: {row[1]}, 数据大小: {len(row[2])} bytes")

conn.close()
print("\n" + "="*60)
input("按Enter键退出...")
