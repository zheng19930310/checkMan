# Python环境安装指南

## 🚀 快速安装步骤

### 方法一：使用安装脚本（推荐）

1. **双击运行** `安装Python环境.bat`
2. 脚本会自动检测是否已安装Python
3. 如果未安装，按照提示操作

### 方法二：手动安装（如果脚本不可用）

#### 步骤1：下载Python

1. 打开浏览器，访问：**https://www.python.org/downloads/**
2. 点击黄色按钮 **"Download Python 3.11.x"**（或最新版本）
3. 等待下载完成

#### 步骤2：安装Python

1. **双击** 下载的安装程序（例如：`python-3.11.9-amd64.exe`）

2. **⚠️ 重要：在安装界面勾选 "Add Python to PATH"**
   ```
   ☑ Add Python to PATH  ← 一定要勾选这个！
   ```

3. 点击 **"Install Now"**

4. 等待安装完成（大约2-3分钟）

5. 看到 "Setup was successful" 后，点击 **"Close"**

#### 步骤3：验证安装

1. **关闭当前所有命令行窗口**
2. **重新打开** 一个新的命令行（PowerShell或CMD）
3. 输入以下命令验证：
   ```bash
   python --version
   ```
   应该显示类似：`Python 3.11.9`

4. 检查pip：
   ```bash
   pip --version
   ```
   应该显示pip版本信息

#### 步骤4：安装项目依赖

在命令行中进入项目目录：
```bash
cd d:\aiwork\checkMan
```

安装依赖包：
```bash
pip install opencv-python pillow numpy matplotlib
```

或者使用requirements.txt：
```bash
pip install -r requirements.txt
```

#### 步骤5：测试环境

运行测试脚本：
```bash
python test_environment.py
```

如果所有测试通过，就可以运行主程序了！

#### 步骤6：运行主程序

```bash
python main_gui.py
```

## 🔧 常见问题

### Q1: 安装时忘记勾选"Add Python to PATH"怎么办？

**解决方法：**
1. 重新运行Python安装程序
2. 选择 "Modify"
3. 确保勾选 "Add Python to environment variables"
4. 点击 "Next" 完成

或者手动添加环境变量：
1. 右键"此电脑" → "属性" → "高级系统设置"
2. 点击"环境变量"
3. 在"系统变量"中找到"Path"，点击"编辑"
4. 添加Python安装路径（例如：`C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\`）
5. 添加Scripts路径（例如：`C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\Scripts\`）
6. 点击"确定"保存
7. **重新打开命令行窗口**

### Q2: 提示"python不是内部或外部命令"？

**原因：** Python未添加到PATH环境变量

**解决方法：** 参考Q1的方法

### Q3: pip安装依赖很慢或失败？

**解决方法：** 使用国内镜像源
```bash
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: 安装后还是无法运行？

**检查步骤：**
1. 确认Python版本：`python --version`（应该是3.8或更高）
2. 确认pip可用：`pip --version`
3. 重新打开命令行（环境变量需要重启才能生效）
4. 检查是否在正确的目录：`cd d:\aiwork\checkMan`

## 📝 安装清单

安装完成后，应该具备：

- ✅ Python 3.8+ （推荐3.10或3.11）
- ✅ pip 包管理器
- ✅ opencv-python （OpenCV）
- ✅ Pillow （图像处理）
- ✅ numpy （数值计算）
- ✅ matplotlib （绘图，可选）

## 🎯 快速验证

运行以下命令快速验证环境：

```bash
python -c "import cv2; import PIL; import numpy; print('环境正常！')"
```

如果显示"环境正常！"，说明安装成功！

## 📞 需要帮助？

如果遇到问题：
1. 查看本指南的"常见问题"部分
2. 运行 `python test_environment.py` 查看详细信息
3. 检查命令行输出的错误信息

祝你安装顺利！🎉
