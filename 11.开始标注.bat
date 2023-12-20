@echo off
chcp 65001
@title VITS数据自动标注 by 未鸟
set path=.\env\Scripts;.\env;ffmpeg\bin;%path%
echo =====
echo 请确定所有的音频已经按标准处理完毕，否则必报错！
echo =====
echo.
.\env\python.exe auto_DataLabeling_re.py
pause
