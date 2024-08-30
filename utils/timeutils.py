#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-07-24 10:38
# describe：
from datetime import datetime
import pytz
import time

# 计算函数耗时
def monitor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录结束时间
        duration = end_time - start_time  # 计算耗时
        print_log(f"Function '{func.__name__}' took {duration:.2f} seconds to execute.")
        return result
    return wrapper


def get_today_str():
    # 获取上海时区时间
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    shanghai_time = datetime.now(shanghai_tz)
    date_str = shanghai_time.strftime("%Y-%m-%d %H:%M:%S")
    return date_str


def print_log(*values: object):
    
    date_str = get_today_str()

    # 打印带当前年月日 时分秒 的日志
    if values and isinstance(values[0], str):
        # Check for leading newlines in the first value
        first_value = values[0]
        leading_newlines = ""
        while first_value.startswith('\n'):
            leading_newlines += "\n"
            first_value = first_value[1:]

        # Print with the leading newlines before the date if any
        print(leading_newlines + date_str, first_value, *values[1:])
    else:
        # Print normally if no special case is needed
        print(date_str, *values)