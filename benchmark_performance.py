#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
硬件性能快速测试脚本
测试你的电脑在人脸识别任务上的实际表现
"""

import time
import sys

def test_cpu_basic():
    """基础CPU性能测试"""
    print("=" * 60)
    print("1. CPU基础性能测试")
    print("=" * 60)
    
    import platform
    print(f"处理器: {platform.processor()}")
    print(f"架构: {'64位' if sys.maxsize > 2**32 else '32位'}")
    
    # 简单的计算测试
    start = time.time()
    result = sum([i**2 for i in range(1000000)])
    elapsed = time.time() - start
    
    print(f"百万级计算耗时: {elapsed:.3f}秒")
    
    if elapsed < 0.5:
        print("✓ CPU性能良好")
    elif elapsed < 1.0:
        print("⚠ CPU性能一般")
    else:
        print("⚠ CPU性能较弱")
    
    print()

def test_memory():
    """内存测试"""
    print("=" * 60)
    print("2. 内存检查")
    print("=" * 60)
    
    try:
        import psutil
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        
        print(f"总内存: {total_gb:.1f} GB")
        print(f"可用内存: {available_gb:.1f} GB")
        print(f"使用率: {memory.percent}%")
        
        if total_gb >= 16:
            print("✓ 内存非常充足")
        elif total_gb >= 8:
            print("✓ 内存充足")
        elif total_gb >= 4:
            print("⚠ 内存勉强够用")
        else:
            print("✗ 内存不足")
        
        print()
    except ImportError:
        print("ℹ️ 未安装psutil，跳过内存测试")
        print("   安装: pip install psutil")
        print()

def test_opencv_performance():
    """OpenCV性能测试"""
    print("=" * 60)
    print("3. OpenCV图像处理性能")
    print("=" * 60)
    
    try:
        import cv2
        import numpy as np
        
        print(f"OpenCV版本: {cv2.__version__}")
        
        # 测试图像加载和处理速度
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        start = time.time()
        for _ in range(100):
            gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (224, 224))
        elapsed = time.time() - start
        
        fps = 100 / elapsed
        print(f"图像处理速度: {fps:.1f} FPS (480p转224x224)")
        
        if fps > 200:
            print("✓ 图像处理性能优秀")
        elif fps > 100:
            print("✓ 图像处理性能良好")
        else:
            print("⚠ 图像处理性能一般")
        
        # 测试Haar人脸检测
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        start = time.time()
        for _ in range(50):
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        elapsed = time.time() - start
        
        detection_fps = 50 / elapsed
        print(f"Haar人脸检测速度: {detection_fps:.1f} FPS")
        
        if detection_fps > 20:
            print("✓ Haar检测速度快，适合实时应用")
        elif detection_fps > 10:
            print("⚠ Haar检测速度一般")
        else:
            print("⚠ Haar检测较慢")
        
        print()
        
    except ImportError:
        print("✗ OpenCV未安装")
        print("  安装: pip install opencv-python")
        print()
    except Exception as e:
        print(f"✗ OpenCV测试失败: {e}")
        print()

def test_numpy_performance():
    """NumPy性能测试"""
    print("=" * 60)
    print("4. NumPy数值计算性能")
    print("=" * 60)
    
    try:
        import numpy as np
        
        # 矩阵运算测试
        size = 1000
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)
        
        start = time.time()
        c = np.dot(a, b)
        elapsed = time.time() - start
        
        print(f"{size}x{size}矩阵乘法耗时: {elapsed:.3f}秒")
        
        if elapsed < 0.5:
            print("✓ 数值计算性能优秀")
        elif elapsed < 1.0:
            print("✓ 数值计算性能良好")
        else:
            print("⚠ 数值计算性能一般")
        
        print()
        
    except ImportError:
        print("✗ NumPy未安装")
        print("  安装: pip install numpy")
        print()
    except Exception as e:
        print(f"✗ NumPy测试失败: {e}")
        print()

def test_pytorch_availability():
    """PyTorch可用性测试"""
    print("=" * 60)
    print("5. PyTorch深度学习框架")
    print("=" * 60)
    
    try:
        import torch
        
        print(f"PyTorch版本: {torch.__version__}")
        print(f"CUDA可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"GPU设备: {torch.cuda.get_device_name(0)}")
            print("✓ 支持GPU加速")
        else:
            print("ℹ️ 仅支持CPU推理")
            print("  对于你的配置（集成显卡），这是正常的")
        
        # 测试CPU推理速度
        print("\n测试模型推理速度...")
        
        # 创建一个简单模型
        model = torch.nn.Sequential(
            torch.nn.Linear(1000, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 10)
        )
        
        # 模拟输入
        x = torch.randn(1, 1000)
        
        # 预热
        for _ in range(10):
            _ = model(x)
        
        # 测试推理时间
        start = time.time()
        iterations = 100
        for _ in range(iterations):
            _ = model(x)
        elapsed = time.time() - start
        
        avg_time = (elapsed / iterations) * 1000
        print(f"平均推理时间: {avg_time:.2f} ms/次")
        print(f"推理速度: {iterations/elapsed:.1f} 次/秒")
        
        if avg_time < 10:
            print("✓ 推理速度快")
        elif avg_time < 50:
            print("⚠ 推理速度中等")
        else:
            print("⚠ 推理速度较慢，建议使用轻量模型")
        
        print()
        
    except ImportError:
        print("✗ PyTorch未安装")
        print("  安装CPU版本: pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
        print()
    except Exception as e:
        print(f"✗ PyTorch测试失败: {e}")
        print()

def test_camera():
    """摄像头测试"""
    print("=" * 60)
    print("6. 摄像头检测")
    print("=" * 60)
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("⚠️  未检测到摄像头")
            print("  可以使用图片文件进行测试")
            print()
            return
        
        ret, frame = cap.read()
        if not ret:
            print("✗ 无法读取摄像头画面")
            cap.release()
            print()
            return
        
        h, w = frame.shape[:2]
        print(f"✓ 摄像头可用")
        print(f"  分辨率: {w}x{h}")
        
        # 测试摄像头FPS
        print("\n测试摄像头帧率...")
        frame_count = 0
        start = time.time()
        
        while frame_count < 30:
            ret, frame = cap.read()
            if ret:
                frame_count += 1
        
        elapsed = time.time() - start
        camera_fps = frame_count / elapsed
        
        print(f"摄像头帧率: {camera_fps:.1f} FPS")
        
        if camera_fps >= 25:
            print("✓ 摄像头性能良好")
        elif camera_fps >= 15:
            print("⚠ 摄像头性能一般")
        else:
            print("⚠ 摄像头性能较差")
        
        cap.release()
        print()
        
    except Exception as e:
        print(f"✗ 摄像头测试失败: {e}")
        print()

def show_recommendation():
    """显示建议"""
    print("=" * 60)
    print("📋 综合评估与建议")
    print("=" * 60)
    print()
    
    print("基于你的硬件配置 (i7-6600U + 16GB RAM + 集成显卡):")
    print()
    
    print("✅ 推荐方案:")
    print("  1. MediaPipe - 最轻量，20+ FPS")
    print("  2. OpenCV Haar - 基础功能，10-30 FPS")
    print("  3. MobileNetV2 - 平衡性能和准确度，5-8 FPS")
    print()
    
    print("⚠️  可用但较慢:")
    print("  1. ResNet18 - 当前项目使用，1-3 FPS")
    print("  2. face_recognition - 高精度，3-8 FPS")
    print()
    
    print("❌ 不推荐:")
    print("  1. 大型Transformer模型 - 太慢")
    print("  2. 高分辨率实时处理 - 会卡顿")
    print("  3. 多目标同时追踪 - CPU压力大")
    print()
    
    print("💡 优化技巧:")
    print("  • 降低输入分辨率 (160x160 而非 224x224)")
    print("  • 隔帧处理 (每3-5帧处理一次)")
    print("  • 使用轻量级模型 (MobileNet/ShuffleNet)")
    print("  • 关闭不必要的后台程序")
    print()

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "人脸识别硬件性能测试工具" + " " * 14 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    print("正在测试你的电脑性能...\n")
    
    test_cpu_basic()
    test_memory()
    test_opencv_performance()
    test_numpy_performance()
    test_pytorch_availability()
    test_camera()
    
    show_recommendation()
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)
    print()
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
