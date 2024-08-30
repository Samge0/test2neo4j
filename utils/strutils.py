#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-30 11:58
# describe：


import re


def sanitize_filename(filename):
    # Replace invalid characters with an underscore or any other preferred character
    return re.sub(r'[\/:*?"<>|]', '_', filename)