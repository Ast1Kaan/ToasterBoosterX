@echo off
title TOASTER BOOSTER X - Setup
color 0A
echo.
echo  ====================================
echo   TOASTER BOOSTER X - Setup
echo  ====================================
echo.

echo [1/3] Pip updating...
python -m pip install --upgrade pip

echo.
echo [2/3] Libraries are loading...
pip install customtkinter==5.2.2
pip install psutil==5.9.8
pip install GPUtil==1.4.0
pip install Pillow==10.3.0
pip install pyinstaller==6.6.0

echo.
echo [3/3] Creating an EXE file....
pyinstaller --onefile --windowed --uac-admin --name "ToasterBoosterX" --collect-all customtkinter --hidden-import psutil --hidden-import GPUtil optimizer.py

echo.
echo  ====================================
echo   COMPLETE! Check the dist/ folder.
echo  ====================================
pause
