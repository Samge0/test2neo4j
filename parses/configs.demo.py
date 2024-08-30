#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-23 16:49
# describe：

API_URL = 'http://localhost:80/v1'                      # dify的api地址，请替换为实际的服务器地址
AUTHORIZATION = 'xxx'                                   # dify的api鉴权token
USER_NAME = 'xxx'                                       # dify的api请求用户名

NEO4J_URL = 'neo4j://localhost:7687'                    # neo4j的地址
NEO4J_USER = 'neo4j'                                    # neo4j的用户名
NEO4J_PASSWORD = 'neo4j'                                # neo4j的密码

# 待处理的文档目录
DOC_DIR = "xxx"  
# 指定文档后缀，暂时只支持文本类型                            
DOC_SUFFIX = 'md,txt'    
# 文档最少行数，低于该值的文档则被忽略，该参数仅作用于 txt,md,html 后缀文件
DOC_MIN_LINES = 6