@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║                                                  ║
echo ║       识别人类 - Python环境一键安装脚本           ║
echo ║          （使用国内清华镜像源）                    ║
echo ║                                                  ║
echo ══════════════════════════════════════════════════╝
echo.
echo 本脚本将帮你安装Python和所需依赖
echo 使用清华镜像源加速下载
echo.

REM 检查Python是否已安装
echo [1/4] 检查Python是否已安装...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Python已安装
    python --version
    goto :install_deps
) else (
    echo ✗ Python未安装，需要下载安装
)

echo.
echo ========================================
echo 请选择安装方式：
echo ========================================
echo.
echo 方式1：手动下载安装（推荐）
echo   1. 使用国内镜像下载Python：
echo      https://mirrors.tuna.tsinghua.edu.cn/python/downloads/
echo   2. 或使用官网：https://www.python.org/downloads/
echo   3. 下载 Python 3.10 或更高版本
echo   4. 运行安装程序
echo   5. **重要：勾选 "Add Python to PATH"**
echo   6. 点击 "Install Now"
echo   7. 安装完成后重新运行此脚本
echo.
echo 方式2：使用Winget自动安装（Windows 11/10）
echo   如果系统支持Winget，可以自动安装
echo.
echo ========================================
echo.

REM 检查是否支持winget
where winget >nul 2>&1
if %errorlevel%==0 (
    echo 检测到Winget，是否使用自动安装？
    set /p choice=输入 Y 自动安装，或输入 N 手动安装 (Y/N): 
    if /i "%choice%"=="Y" (
        echo.
        echo 正在使用Winget安装Python...
        winget install Python.Python.3.11
        echo.
        echo Python安装完成！请关闭此窗口，重新打开命令行后再运行 install_deps.bat
        pause
        exit
    )
)

echo.
echo 请按照"方式1"手动安装Python
echo.
pause
exit

:install_deps
echo.
echo [2/4] 配置国内镜像源（清华源）...
echo 正在配置pip使用清华镜像源...
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

echo.
echo [3/4] 升级pip（使用国内源）...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [4/4] 安装项目依赖（使用清华镜像源）...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 安装核心依赖（使用国内镜像源）
echo 正在安装 OpenCV...
python -m pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装 Pillow...
python -m pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装 NumPy...
python -m pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装 matplotlib...
python -m pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装 PyTorch（CPU版本，较小）...
python -m pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║                                                  ║
echo ║              安装完成！                           ║
echo ║                                                  ║
echo ══════════════════════════════════════════════════╝
echo.
echo 现在可以运行主程序了：
echo   python main_gui.py
echo.
echo 或者运行测试脚本检查环境：
echo   python test_environment.py
echo.
pause
