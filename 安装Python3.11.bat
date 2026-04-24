@echo off
chcp 65001 >nul
echo ============================================================
echo 安装 Python 3.11（更稳定，兼容性好）
echo ============================================================
echo.
echo 当前Python版本:
python --version
echo.
echo 正在下载 Python 3.11.9...
echo.

:: 下载 Python 3.11.9
curl -L -o python-3.11.9-amd64.exe "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"

if %ERRORLEVEL% NEQ 0 (
    echo 下载失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo 正在安装 Python 3.11.9...
echo 请等待安装完成...
echo.

:: 静默安装
start /wait python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo.
echo Python 3.11.9 安装完成！
echo.
echo 请关闭此窗口，重新打开一个新的PowerShell窗口
echo 然后运行以下命令验证安装:
echo   python --version
echo.
echo 之后运行:
echo   pip install opencv-python pillow numpy matplotlib
echo.
pause
