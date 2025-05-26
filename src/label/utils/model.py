from __future__ import annotations

from pathlib import Path

from funasr import AutoModel

from label._dataclass import RunnerSettings
from label._typing import ASRResponse
from label.utils.config import load_settings_file


class FunASRModel:
    def __init__(self):
        self.settings = load_settings_file("config.toml", RunnerSettings)
        self.base_model: str = str(self.settings.base_model)
        self.vad_model: str = str(self.settings.vad_model)
        self.punc_model: str = str(self.settings.punc_model)
        self.device: str = self.settings.device

    def vad_and_asr(self):
        model = AutoModel(
            model=self.base_model,  # base
            vad_model=self.vad_model,  # 检测语音活动，自动分隔
            device=self.device,
            disable_update=True,  # 添加在这里，禁用更新检查
        )
        return model

    def only_txt(self):
        model = AutoModel(
            model=self.base_model, device=self.device, disable_update=True
        )  # 也可以添加在这里
        return model

    def only_puc(self):
        model = AutoModel(
            model=self.punc_model, device=self.device, disable_update=True
        )  # 也可以添加在这里
        return model


def generate_asr_results(model: AutoModel, input_path: Path) -> ASRResponse:
    # asr_and_vad 使用
    # input: Path("./bug/bug_0_30.opus")
    # return:
    # [{'key': 'bug_0_30',
    # 'text': '嗯 嗯  well come to the hollywood reporter actress round',
    # 'timestamp': [[12590, 12830], [16460, 16700], [27950, 28170], [28170, 28290], [28290, 28390], [28390, 28470], [28470, 28890], [28890, 29290], [29290, 29690], [29690, 30000]]}]

    settings: RunnerSettings = load_settings_file("config.toml", RunnerSettings)
    batch_size_s = settings.batch_size_s
    hot_word_path = settings.hot_words_path
    # 原本 AutoModel 支持 input_path 是 list 的情况，但这里我忽略了它，我只需要写一个BasicRunner，多任务自己处理。
    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} not found.")
    else:
        res: list[dict[str, Any]] = model.generate(  # type: ignore
            input=str(input_path),
            batch_size_s=batch_size_s,
            hot_word=str(hot_word_path),
        )
    if not res:
        raise ValueError("The res from automodel is empty.")
    res: dict[str, Any] = res[0]  # type: ignore
    response: ASRResponse = {
        "key": res.get("key", ""),
        "text": res.get("text", ""),
        "timestamp": res.get("timestamp", []),
    }
    return response


def generate_punc_results(model: AutoModel, input_text: str) -> str:
    # punc_model 使用
    # 参考: https://modelscope.cn/models/iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch/summary
    # input_text: 那今天的会就到这里吧 happy new year 明年见
    # return: 那今天的会就到这里吧，happy new year明年见。
    res = model.generate(input=input_text)  # type:ignore
    return res[0]["text"]  # type:ignore
