@echo off
@title Bert_VITS2标注清理 by 未鸟
set path=.\env\Scripts;.\env;ffmpeg\bin;%path%
echo =====
echo 请注意！你需要先完成标注，而继续执行将删除所有含英文字母及过短的标注数据
echo =====
echo.
pause
.\env\python.exe clean_list.py
pause
