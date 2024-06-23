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
        self.spk_model = self.config["spk_model"]
        self.device = self.config["device"]

    def full_version(self):
        funasr_model = AutoModel(
            model=self.base_model,  # base
            vad_model=self.vad_model,  # 检测语音活动，自动分隔
            punc_model=self.punc_model,  # 给出标点。
            # model_revision="v2.0.4",
            device=self.device
        )
        return funasr_model

    def only_vad(self):
        model = AutoModel(model=self.vad_model,
                          device=self.device)
        return model

    def only_spk(self):
        model = AutoModel(model=self.spk_model,
                          device=self.device)
        return model


def generate_results(model,wav_name, hot_word="",debug=False):
    if type(wav_name) is list:
        if hot_word!="":
            res = model.generate(
                input=wav_name,
                hotword=hot_word,
                batch_size_s=300,
            )
        else:
            res = model.generate(
                input=wav_name,
                batch_size_s=300,
            )
    else:
        if hot_word!="":
            res = model.generate(
                input=f"./raw_audio/{wav_name}.wav",
                hotword=hot_word,
                batch_size_s=300,
            )
        else:
            res = model.generate(
                input=f"./raw_audio/{wav_name}.wav",
                batch_size_s=300,
            )

    return res
