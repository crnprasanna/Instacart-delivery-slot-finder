#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Logger helper module
'''

import logging
import os
from datetime import datetime
LOG_DIR_DEFAULT = 'logs/'


class Logger:

    def __init__(self, log_path=LOG_DIR_DEFAULT):
        LOG_DEST = log_path
        if not os.path.exists(LOG_DEST):
            os.makedirs(LOG_DEST)
        self.LOG_DEST = LOG_DEST + '{}.log'
        curr_date = datetime.now().strftime('%Y%m%d')
        self.log_name = self.LOG_DEST.format(curr_date)

    def _update_config(self):

        logging.basicConfig(filename=self.log_name, filemode='a',
                            format='(%(asctime)s) %(name)s | %(message)s'
                            , datefmt='%H:%M:%S', level=logging.INFO)

    def log(self, msg='\n'):
        self._update_config()
        print(msg)
        logging.info(msg)
