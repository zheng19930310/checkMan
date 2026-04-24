# 快速开始指南

## 🚀 5分钟快速上手

### 第一步：安装依赖

打开命令行，进入项目目录：

```bash
cd d:\aiwork\checkMan
pip install -r requirements.txt
```

### 第二步：运行GUI版本（推荐）

```bash
python main_gui.py
```

### 第三步：使用界面

1. 点击 **"▶ 启动摄像头"** 按钮
2. 等待摄像头开启
3. 面对摄像头，系统会自动识别
4. 右侧面板显示识别结果（性别、年龄）
5. 点击 **"⏹ 关闭摄像头"** 按钮暂停
6. 点击窗口 **X** 按钮退出程序

## 📸 界面说明

```
┌─────────────────────────────────────────────────┐
│         识别人类 - 性别年龄识别系统               │
├─────────────────────┬───────────────────────────┤
│                     │  系统状态                  │
│                     │  状态: 运行中              │
│   摄像头画面         │  FPS: 25.3                │
│   (实时显示)         │                           │
│                     │  识别结果                  │
│                     │  👤 人员 1:                │
│                     │    性别: 男性 (65.0%)      │
│                     │    年龄: 28 岁             │
│                     │                           │
├─────────────────────┴───────────────────────────┤
│  [▶ 启动摄像头]  [⏹ 关闭摄像头]                  │
└─────────────────────────────────────────────────┘
```

## ⚙️ 配置说明

### 摄像头选择

如果系统有多个摄像头，可以修改代码：

```python
# 在 main_gui.py 中找到这行：
self.cap = cv2.VideoCapture(0)

# 修改数字来选择不同的摄像头：
# 0 - 默认摄像头
# 1 - 第二个摄像头
# 2 - 第三个摄像头
```

### 调整识别区域

```python
# 在 process_frame 方法中调整：
faces = face_cascade.detectMultiScale(
    gray, 
    scaleFactor=1.1,      # 缩放比例（越小越精确但越慢）
    minNeighbors=5,       # 最小邻居数（越大越严格）
    minSize=(30, 30)      # 最小检测区域
)
```

## 🎯 使用技巧

### 提高识别准确率

1. **光线充足**：确保面部光线均匀
2. **正对摄像头**：面部尽量正对摄像头
3. **距离适中**：保持30-50厘米距离
4. **避免遮挡**：不要戴墨镜或口罩

### 性能优化

1. **降低分辨率**：减小摄像头分辨率可提高FPS
2. **调整检测频率**：不必每帧都检测
3. **关闭其他程序**：释放系统资源

## 🔧 故障排除

### 问题1：摄像头无法打开

**解决方法：**
```python
# 检查摄像头是否被其他程序占用
# 尝试更换摄像头编号
self.cap = cv2.VideoCapture(1)  # 改为1或2
```

### 问题2：识别结果不准确

**原因：**
- 当前使用简化算法（适合开发测试）
- 光线不足或角度不佳

**解决方法：**
- 改善光线条件
- 使用预训练的深度学习模型（需要训练）

### 问题3：界面卡顿

**解决方法：**
```python
# 在 process_video 方法中调整：
time.sleep(0.03)  # 增加这个值可以降低CPU占用
```

### 问题4：无法检测到人脸

**检查项：**
- 面部是否在画面中
- 光线是否充足
- 是否有遮挡物

## 📝 开发说明

### 项目架构

```
main_gui.py
├── CameraApp (主应用类)
│   ├── create_widgets()     # 创建UI
│   ├── init_models()        # 初始化模型
│   ├── start_camera()       # 启动摄像头
│   ├── stop_camera()        # 停止摄像头
│   ├── process_video()      # 处理视频流（线程）
│   ├── process_frame()      # 处理单帧
│   ├── estimate_gender()    # 性别估计
│   └── estimate_age()       # 年龄估计
```

### 自定义功能

#### 添加新的识别属性

```python
def estimate_emotion(self, face_roi):
    """估计情绪"""
    # 实现情绪识别逻辑
    return emotion, confidence
```

#### 保存识别结果

```python
def save_results(self, results):
    """保存识别结果到文件"""
    with open('results.txt', 'a') as f:
        f.write(str(results) + '\n')
```

## 🌐 集成预训练模型

如果需要更高的准确率，可以集成预训练模型：

### 方案1：使用OpenCV DNN

```python
# 加载预训练的性别年龄模型
gender_net = cv2.dnn.readNetFromCaffe(
    'gender_deploy.prototxt',
    'gender_net.caffemodel'
)

age_net = cv2.dnn.readNetFromCaffe(
    'age_deploy.prototxt',
    'age_net.caffemodel'
)
```

### 方案2：使用深度学习框架

```python
# 使用PyTorch加载预训练模型
model = torch.hub.load('pytorch/vision', 'resnet18', pretrained=True)
```

## 📞 获取帮助

如果遇到问题：

1. 查看 README.md 文档
2. 检查 Python 版本（需要 3.8+）
3. 确保所有依赖已正确安装
4. 查看控制台输出的错误信息

## 🎉 开始使用

现在你可以：

```bash
# 启动GUI版本
python main_gui.py

# 或者启动命令行版本
python main.py
```

祝你使用愉快！🚀
