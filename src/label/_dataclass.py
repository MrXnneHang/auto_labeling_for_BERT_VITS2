from __future__ import annotations

from typing import Annotated, Literal, get_args

from pydantic import BaseModel, Field


class RunnerSettings(BaseModel):
    batch_size_s: Annotated[
        int, Field(300, title="批处理大小(默认300,只要能吃满显卡或者CPU即可)")
    ]
    device: Annotated[Literal["cpu", "cuda"], Field("cpu", title="设备选择")]
    punctuation_list: Annotated[str, Field("，。；、？！,.;?!")]
    custom_output_dir: Annotated[bool, Field(False, title="自定义输出目录")]

    cache_dir: Annotated[str, Field("./cache", title="缓存路径")]
    output_dir: Annotated[str, Field("./output", title="输出路径")]
    hot_words_path: Annotated[str, Field("./hot_words.txt", title="热词路径")]
    FFMPEG_PATH: Annotated[str, Field("ffmpeg", title="FFMPEG路径,默认用系统环境变量")]
    base_model: Annotated[
        str,
        Field(
            "./models/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
            title="base 模型",
        ),
    ]
    vad_model: Annotated[
        str,
        Field("./models/speech_fsmn_vad_zh-cn-16k-common-pytorch", title="vad 模型"),
    ]
    punc_model: Annotated[
        str,
        Field(
            "./models/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
            title="punc 模型",
        ),
    ]
    sense_voice_model: Annotated[
        str,
        Field(
            "./models/SenseVoiceSmall",
            title="sense_voice 模型",
        ),
    ]

    cut: Annotated[bool, Field(False)]
    cut_line: Annotated[int, Field(400, title="分割间隔(毫秒)")]
    combine: Annotated[bool, Field(False)]
    combine_line: Annotated[int, Field(400, title="合并间隔(毫秒)")]
    max_sentence_length: Annotated[int, Field(20, title="最大单句长度")]
