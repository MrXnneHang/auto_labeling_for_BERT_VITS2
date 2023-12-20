## 这是一个针对Bert-VITS2的一个音频预处理项目.

该项目大部分建立于阿里的Funasr上.<br>
---
### 应用场景:<br>
从主播游戏的视频中提取人声,取出无人声的部分。<br>
把主播的每句话字幕的起始点和结束点记录下来。之后可以利用这个来切分出一句句完整的长短不一的话，而取代以往的归一化一样的切片切成10s。<br>
---
### 思路：<br>
利用带FunASR上面的带time_stamp的语音识别，获取每句话中第一个字的start_time和最后一个字的end_time.<br>
利用这个start-end把无语音的背景部分排除掉。并且获取每句话的开始和结束<br>

### 项目另一半本身是另一个up做的：@领航员未鸟
项目建立在她的切片语音识别上面。<br>
最终处理出来一条一条完整的句子后可以再利用带符号的标注来写esd.list<br>
Model需要自己下,我这里打算放到网盘.<br>
待处理的文件需要放在./raw_audio/下<br>
处理完的所有生成文件会放在./tmp下.
包括.带time_series的字幕txt.合成短句的processed.txt,和去空白后的processed.wav



## 如何安装环境:

本身就是funasr的环境适配见：https://alibaba-damo-academy.github.io/FunASR/en/installation/installation.html
