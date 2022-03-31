@echo off

start cmd /c "python -m venv venv && venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install pillow opencv-python windows-curses"
