#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-30 15:30
# describe：对文本进行关系提取

from parses import configs, relation_models
from utils import timeutils


@timeutils.monitor
def extract(query):
    """
    使用dify的关系提取应用对文本进行关系提取

    :param query: 需要提取关系的文本
    :return: 提取的关系
    """
    result = relation_models.get_api_client().send_chat_message(
        query=query,
        user=configs.USER_NAME,
    )
    return result


if __name__ == "__main__":
    result = extract("2024年8月26日，公司A的陈总与公司B的刘总达成合作协议。陈总来自贵州，于2000年毕业于北京大学。刘总来自四川，于2005年毕业于深圳大学。")
    print(result)
    