#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-30 17:31
# describe：遍历目录-》读取文本-》对文本进行关系提取-》写入neo4j数据库

import os
from parses import configs, neo4js, relations
from utils import fileutils, timeutils

# 本地记录的失败日志文件
faild_log_path = f"{fileutils.cache_dir}/logs/faild.log"
# 本地记录的成功日志文件
success_log_path = f"{fileutils.cache_dir}/logs/success.log"


def is_success(file_path):
    """
    Check if the given file has been successfully processed.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file has been successfully processed, False otherwise.
    """
    if not file_path or not os.path.exists(file_path):
        return False
    _log_text = fileutils.read(success_log_path) or ''
    return file_path in _log_text


if __name__ == '__main__':
    # 遍历md目录文档 -》 读取文本 -》 对文本进行关系提取 -》写入neo4j数据库
     
    # 使用 glob 模块获取所有 .md 文件
    doc_files = fileutils.get_docs_files(configs.DOC_DIR, configs.DOC_SUFFIX) or []

    file_total = len(doc_files)
    if file_total == 0:
        raise ValueError(f"在 {configs.DOC_DIR} 目录下没有找到符合要求文档文件") 
    
    # 打印找到的所有 .md 文件
    for i in range(file_total):
        
        file_path = doc_files[i]
        file_path = file_path.replace(os.sep, '/')
        filename = os.path.basename(file_path)
        
        timeutils.print_log(f"【{i+1}/{file_total}】正在处理：{file_path}")
        
        # 判断文件行数是否小于 目标值
        if fileutils.need_calculate_lines(file_path):
            file_lines = fileutils.get_file_lines(file_path)
            if file_lines < configs.DOC_MIN_LINES:
                timeutils.print_log(f"行数低于{configs.DOC_MIN_LINES}，跳过：{file_path}")
                continue
        
        # 判断是否已处理过
        if is_success(file_path):
            timeutils.print_log(f"该文件已处理过，跳过：{file_path}")
            continue
        
        # 读取文本
        text = fileutils.read(file_path)
        
        # 提取关系
        try:
            relation_data = relations.extract(text)
        except Exception as e:
            msg = f"提取关系失败，跳过：，跳过：{file_path}, text={text[:100]}...\n"
            fileutils.save(faild_log_path, f"{timeutils.get_today_str()} {msg}", 'a+')
            timeutils.print_log(msg)
            continue
        
        # 上传到neo4j数据库
        try:
            neo4js.import_to_neo4j(relation_data)
        except Exception as e:
            msg = f"上传到neo4j数据库失败，跳过：{file_path}, relation_data={relation_data}\n"
            fileutils.save(faild_log_path, f"{timeutils.get_today_str()} {msg}", 'a+')
            timeutils.print_log(msg)
            continue
        
        fileutils.save(success_log_path, f"{file_path}\n", 'a+')
        timeutils.print_log(f"【{i+1}/{file_total}】处理完毕：{file_path}")
        
    # 关闭数据库连接
    neo4js.close_driver()
    timeutils.print_log('all done')
    