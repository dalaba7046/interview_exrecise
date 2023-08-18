# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 00:20:10 2023

@author: Johnny.Liu
"""
import os
import logging as logger
import json

def create_folder(path):

    if os.path.exists(path) == True:
        logger.info('Folder {} already exists.'.format(path))
        return

    try:
        os.makedirs(path)
        logger.info('Create folder {} done'.format(path))
    except Exception as e:
        logger.info(e)
        
        
def write_json_file(path,res_data):
    with open(f'{path}','w',encoding='utf-8') as f:
        json.dump(res_data, f)