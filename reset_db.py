#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重置数据库"""

import os

db_path = "faces.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✓ 已删除旧数据库: {db_path}")
else:
    print(f"数据库文件不存在: {db_path}")

print("数据库已重置，下次运行程序会自动创建新数据库")
