## 这是一个针对Bert-VITS2的一个音频预处理项目.

该项目大部分建立于阿里的Funasr上.<br>
---
### 严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。

---

说人话是：请尊重别人的隐私，如果有需要公开使用别人的声音作为数据集，请征求别人的同意，至少，是让对方知情。



### 思路：<br>

利用带FunASR上面的带time_stamp的语音识别，获取每句话中第一个字的start_time和最后一个字的end_time.<br>
利用这个start-end把无语音的背景部分排除掉。并且获取每句话的开始和结束<br>

### 项目另一半本身是另一个up做的：@领航员未鸟
项目建立在她的切片语音识别上面。<br>
虽然我写得比她多 <br>
### 注意:

处理完的所有生成文件会放在./tmp下.<br>
待处理的文件需要放在./raw_audio/下<br>

## 如何安装环境:

#### 本身就是funasr的环境适配见：https://alibaba-damo-academy.github.io/FunASR/en/installation/installation.html
## 项目的说明:
适用场景一：给游戏主播录屏(单人音频，大量空白)制作BERT-VITS制作数据集<br>
适用场景二:多人音频，如动漫人物配音提取（兴奋）。以及电台，连麦，视频电话。<br>
适用场景三: 给已经切片好的galgame character wavs 制作BERT-VITS数据集<br>

## 用法:

场景一：<br>
Step 1. single_person_step1.py/bat .会识别字幕并且按照时间线来裁剪掉没有说话的片段，每个音频片段之间保留1.5s空白。<br>
Step 2. single_person_step2.py/bat  会将音频片段按照字幕切片，每个片段是一个完整断句或者长句，可以根据一些参数来控制断句，长句比例和长度。<br>
参数讲解：https://www.bilibili.com/opus/885554048063766563?spm_id_from=333.999.0.0<br>
如果连接丢了，可能是我更新了一下。可以在我的主页专栏里找：https://space.bilibili.com/556737824<br>
## 场景一已经基本成熟可以进入测试阶段。<br>
---

场景二:<br>

我打算更改策略.<br>

step1.根据说话人活动检测。并且切片，得到不带说话单人标签的短音频。<br>

目前借助3d-speaker生成的rttm文件进行片段分割，因为模型原因,暂时只支持中文，日文效果很差。<br>
如果在windows下运行，可以参照/speaker-diaration/combine.sh来写一个.bat然后运行，后续我也会补档一下windows.<br>
待处理的音频放在/speaker-diaration/examples/下，需要自行新建。具体可以参阅/speaker-diaration/local和/speaker-diaration/utils下的代码。<br>

参考原项目:(https://github.com/alibaba-damo-academy/3D-speaker)<br>
---

场景三:<br>

暂时需要使用Whisper WebUI来获取txt.

Step 1. 初步清洗，删除过短的音频<br>
Step 2. Whisper WebUI来获取*.txt,不需要Time_stamp<br>
step 3. 合成txts成esd.list,txt中可能有几行，这里会把它们合并到同一行，然后在进行写入.<br>
Step 4. 检查一下Whisper 错误生成的文本（乱码，重复单字).这里也可以选择清洗掉过短文本.<br>
Step 5. 已经可以用了<br>

后续会使用Funasr的日文模型。

你可以在b站上联系我：https://space.bilibili.com/556737824?spm_id_from=333.788.0.0
