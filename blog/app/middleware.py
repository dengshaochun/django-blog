#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 17:20
# @Author  : Dengsc
# @Site    : 
# @File    : middleware.py
# @Software: PyCharm


import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.db import connection

logger = logging.getLogger('dblog')


class ShowSqlMiddleware(MiddlewareMixin):
    """打印出每次的数据库操作"""
    
    def process_response(self, request, response):
        if settings.DEBUG:
            for query in connection.queries:
                logger.info("\033[1;31m[%s]\033[0m \033[1m%s\033[0m"
                            % (query['time'], " ".join(query['sql'].split())))
        return response
