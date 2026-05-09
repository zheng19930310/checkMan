#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查数据库内容"""

from face_db import FaceDatabase

db = FaceDatabase()
print("数据库统计:", db.get_stats())

features = db.get_all_face_features()
print(f"\n特征数量: {len(features)}")

for i, f in enumerate(features):
    print(f"\n特征 {i+1}:")
    print(f"  user_id: {f['user_id']}")
    print(f"  encoding类型: {type(f['encoding']).__name__}")
    print(f"  encoding大小: {len(f['encoding'])} bytes")
    print(f"  angle: {f['angle']}")
    
    # 尝试解码
    import pickle
    import numpy as np
    import cv2
    
    try:
        img = pickle.loads(f['encoding'])
        print(f"  ✓ pickle解码成功，形状: {img.shape if hasattr(img, 'shape') else 'N/A'}")
    except Exception as e:
        print(f"  ✗ pickle解码失败: {e}")
        
        try:
            img_array = np.frombuffer(f['encoding'], np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                print(f"  ✓ 图像解码成功，形状: {img.shape}")
            else:
                print(f"  ✗ 图像解码失败")
        except Exception as e2:
            print(f"  ✗ 图像解码也失败: {e2}")
