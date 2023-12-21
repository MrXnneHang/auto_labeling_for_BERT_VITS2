## 这是一个针对Bert-VITS2的一个音频预处理项目.

该项目大部分建立于阿里的Funasr上.<br>
---
### 思路：<br>
利用带FunASR上面的带time_stamp的语音识别，获取每句话中第一个字的start_time和最后一个字的end_time.<br>
利用这个start-end把无语音的背景部分排除掉。并且获取每句话的开始和结束<br>

### 项目另一半本身是另一个up做的：@领航员未鸟
项目建立在她的切片语音识别上面。<br>
虽然我写得比她多 <br>
### 注意:

最终处理出来一条一条完整的句子后可以再利用带符号的标注来写esd.list<br>
处理完的所有生成文件会放在./tmp下.<br>
Model需要自己下,我这里打算放到网盘.<br>
待处理的文件需要放在./raw_audio/下<br>

## 如何安装环境:

本身就是funasr的环境适配见：https://alibaba-damo-academy.github.io/FunASR/en/installation/installation.html
---
## 项目的说明:
适用场景一：给游戏主播录屏(单人音频，大量空白)制作BERT-VITS制作数据集<br>
适用场景二: 给已经切片好的galgame character wavs 制作BERT-VITS数据集<br>

场景一：<br>
Step 1. Run_clip.py 会按照Funasr的Time_stamp逐句squeeze掉没有说话的音频 <br>
step 2. 用MDX算法给process后变短的wav降噪,请参考领航员未鸟的一键包。
Step 3. Run_cut.py  ./raw_audio/降噪后的wavs -> ./tmp/cut/*.wav，根据字幕切割后的音频,每个音频是一个完整断句(长句一般由逗号隔开有多个部分，而这里把这些部分separated,稍微修改也可以选择按照长句分割)<br>
Step 4. 用未鸟的auto_labeling来给短音频写esd.list<br>

场景二:<br>
Step 1. 初步清洗，删除过短的音频<br>
Step 2. Whisper WebUI来获取*.txt,不需要Time_stamp<br>
step 3. 合成txts成esd.list,txt中可能有几行，这里会把它们合并到同一行，然后在进行写入.<br>
Step 4. 手动清理一下Whisper 错误生成的文本（不正常显示，重复).这里也可以选择清洗掉过短文本.<br>
Step 5. 已经可以用了<br>


你可以在b站上联系我：https://space.bilibili.com/556737824?spm_id_from=333.788.0.0
