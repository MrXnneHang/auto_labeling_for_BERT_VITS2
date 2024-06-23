from utils.util import load_config
from funasr import AutoModel


class FunASRModel:

    def __init__(self):
        """
        """
        self.config = load_config()
        self.base_model = self.config["base_model"]
        self.vad_model = self.config["vad_model"]
        self.punc_model = self.config["punc_model"]

    def full_version(self):
        funasr_model = AutoModel(
            model=self.base_model,  # base
            vad_model=self.vad_model,  # 支持长音频，自动分隔
            punc_model=self.punc_model,  # 检测语音活动，给出标点。
            # model_revision="v2.0.4",
            device="cuda:0"
        )
        return funasr_model

    def only_base(self):
        funasr_model = AutoModel(
            model=self.base_model,  # base
            vad_model=self.vad_model,  # 支持长音频，自动分隔
            # punc_model=self.punc_model,  # 检测语音活动，给出标点。
            # model_revision="v2.0.4",
            device="cuda:0"
        )
        return funasr_model


def generate_results(model,wav_name, hot_word,debug=False):
    res = model.generate(
        input=f"./raw_audio/{wav_name}.wav",
        hotword=hot_word,
        batch_size_s=300,
    )
    return res
