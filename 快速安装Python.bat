@echo off
chcp 65001 >nul
color 0A

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║                                                  ║
echo ║     识别人类 - Python 3.11 快速安装脚本          ║
echo ║         （使用国内清华镜像源）                    ║
echo ║                                                  ║
echo ══════════════════════════════════════════════════╝
echo.

REM 检查Python是否已安装
echo [检查] 正在检测Python环境...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo [成功] Python已安装！
    python --version
    echo.
    goto :install_deps
)

echo.
echo ══════════════════════════════════════════════════
echo  Python 未安装，开始安装...
echo ══════════════════════════════════════════════════
echo.

REM 从清华镜像下载Python 3.11.9
echo [下载] 正在从清华镜像下载Python 3.11.9...
echo 下载地址: https://mirrors.tuna.tsinghua.edu.cn/python/downloads/3.11.9/python-3.11.9-amd64.exe
echo.
echo 如果下载失败，请手动下载：
echo 1. 打开浏览器
echo 2. 访问: https://mirrors.tuna.tsinghua.edu.cn/python/downloads/3.11.9/
echo 3. 下载: python-3.11.9-amd64.exe
echo 4. 运行安装程序，务必勾选 "Add Python to PATH"
echo 5. 安装完成后重新运行此脚本
echo.

echo 正在开始下载（约50MB，请耐心等待）...
echo.

REM 使用PowerShell下载
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://mirrors.tuna.tsinghua.edu.cn/python/downloads/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-3.11.9-amd64.exe'}"

if exist "%TEMP%\python-3.11.9-amd64.exe" (
    echo [成功] 下载完成！
    echo.
    echo ══════════════════════════════════════════════════
    echo  开始安装Python
    echo ══════════════════════════════════════════════════
    echo.
    echo 安装程序即将启动...
    echo 请在安装界面勾选 "Add Python to PATH"
    echo 然后点击 "Install Now"
    echo.
    pause
    
    REM 静默安装Python（自动添加到PATH）
    "%TEMP%\python-3.11.9-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    
    echo.
    echo 等待安装完成...
    timeout /t 60 /nobreak >nul
    
    REM 清理安装文件
    del "%TEMP%\python-3.11.9-amd64.exe"
    
    echo.
    echo [成功] Python安装完成！
    echo.
    echo ⚠️  重要提示：
    echo 请关闭此窗口，重新打开一个新的命令行窗口
    echo 然后再次运行此脚本以安装依赖包
    echo.
    pause
    exit
) else (
    echo.
    echo [失败] 下载失败！
    echo.
    echo 请手动安装Python：
    echo 1. 访问: https://www.python.org/downloads/
    echo 2. 下载 Python 3.11.x
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo 4. 安装完成后重新运行此脚本
    echo.
    pause
    exit
)

:install_deps
echo.
echo ══════════════════════════════════════════════════
echo  配置国内镜像源并安装依赖包
echo ══════════════════════════════════════════════════
echo.

echo [1/5] 配置清华镜像源...
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
echo [完成] 镜像源配置完成
echo.

echo [2/5] 升级pip...
python -m pip install --upgrade pip
echo.

echo [3/5] 安装 OpenCV...
python -m pip install opencv-python
echo.

echo [4/5] 安装 Pillow...
python -m pip install Pillow
echo.

echo [5/5] 安装 NumPy...
python -m pip install numpy
echo.

echo ╔══════════════════════════════════════════════════╗
echo ║                                                  ║
echo ║          🎉 所有依赖安装完成！                    ║
echo ║                                                  ║
echo ══════════════════════════════════════════════════╝
echo.
echo 现在可以运行测试程序：
echo   python test_environment.py
echo.
echo 或运行主程序：
echo   python main_gui.py
echo.
pause
