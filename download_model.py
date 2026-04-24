import os
import urllib.request
import zipfile
import hashlib

def download_model(url, save_path, expected_hash=None):
    """下载模型文件"""
    print(f"正在下载模型: {url}")
    
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"模型下载成功: {save_path}")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False

def check_model_exists(model_path):
    """检查模型文件是否存在"""
    return os.path.exists(model_path)

if __name__ == "__main__":
    print("模型下载脚本")
    print("请确保网络连接正常")
