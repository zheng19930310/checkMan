#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本 - 带完整错误日志
"""

import sys
import traceback
import os

# 重定向stderr到文件
log_file = "error_log.txt"
sys.stderr = open(log_file, 'w', encoding='utf-8')

print("="*60)
print("启动识别人类系统...")
print(f"错误日志将保存到: {os.path.abspath(log_file)}")
print("="*60)

try:
    from main_full import main
    main()
except Exception as e:
    print(f"\n严重错误: {e}")
    traceback.print_exc()
    input("\n按回车键退出...")
finally:
    sys.stderr.close()
