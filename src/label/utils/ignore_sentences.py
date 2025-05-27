from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from label._typing import Sentence


def ignore_short_sentences(
    sentences: list[Sentence], min_length: int = 2000
) -> list[Sentence]:
    """
    忽略长度小于 min_length 的句子。
    """
    ignored_sentences = [
        sentence
        for sentence in sentences
        if sentence["end"] - sentence["start"] >= min_length
    ]
    return ignored_sentences


def ignore_long_sentences(
    sentences: list[Sentence], max_length: int = 10000
) -> list[Sentence]:
    """
    忽略长度大于 max_length 的句子。
    """
    ignored_sentences = [
        sentence
        for sentence in sentences
        if sentence["end"] - sentence["start"] <= max_length
    ]
    return ignored_sentences
