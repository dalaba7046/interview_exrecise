# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 23:11:10 2023

@author: Johnny.Liu
"""

from seleniumwire import webdriver
#import undetected_chromedriver as uc
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import gzip
import json
from jsonpath import jsonpath
from random import uniform
from time import sleep
from datetime import datetime
from utils.util import create_folder,write_json_file
import traceback
import sys

#車型
def get_mdl(driver):

    mdl_list=[]
    for m in driver.find_elements(By.CSS_SELECTOR,'#wid-modelTable > div > div > div.p5_table_data > div.p5_table_rec.datarow.unavailable.link'):
        m=m.get_attribute('id').split('_')[1]
        if m != "":
            if "'" in m:
                mdl_list.append(m.replace("'","%27"))
            else:
                mdl_list.append(m)
    return mdl_list



def get_model_type_path(m,driver,output_folder_path):
    #技術信息
    api_url = f'{base_url}/p5bmw/extern/vehicle/modeltypes?lang=zh-TW&mdl={m}&serviceName=bmw_parts&upds=2023-07-13--12-55&_=1692241038548'
    model_type_list = get_data(api_url, driver, output_folder_path)
    
    for model in model_type_list:
        #限制1
        res1_list = get_data(model, driver, output_folder_path)
        for r1 in res1_list:
            #限制2
            res2_list = get_data(r1, driver, output_folder_path)
            for r2 in res2_list:
                #限制3
                res3_list = get_data(r2,driver,output_folder_path)
                for r3 in res3_list:
                    #總組
                    bntr_list = get_data(r3, driver, output_folder_path)
                    for bntr in bntr_list:
                        #功能組
                        graph_nav_list = get_data(bntr, driver, output_folder_path)
                        for graph in graph_nav_list:
                            #評論
                           review_list = get_data(graph, driver, output_folder_path)





def get_data(res,driver,output_folder_path):
    driver.get(res)
    sleep(uniform(2,5))
    res_data,file_name = get_api_data(driver)
    #儲存API內容
    try:
        for re in res_data['data']['records']:
            try:
                file_path = f"{output_folder_path}/{re['values']['restriction']}.json"
            except:
                file_path = f"{output_folder_path}/{file_name}.json"
            write_json_file(file_path, res_data)
    except:
        file_path = res_data['data']['topRightButton']['hint']
        write_json_file(file_path, res_data)
    #回傳下一階url
    data_list=[f"{base_url}{jsonpath(res_data['data'],'$..path')[i]}" for i in range(len(jsonpath(res_data['data'],'$..path')))]

    return data_list


#API內容擷取
def get_api_data(driver):
    for request in driver.requests:
        if request.url == driver.current_url:
            res=request.response.body
            res_data = gzip.decompress(res)
            file_name = json.loads(res_data)['crumbs'][0]['link']['id']
            res_data=json.loads(res_data)
            break

    return res_data,file_name

def main():
    global base_url
    base_url='https://www.partslink24.com'
    host_url='https://www.partslink24.com/p5/latest/p5.html#%2Fp5bmw~bmw_parts~zh-TW~~~~~eyJwIjoidmVoaWNsZXMiLCJiIjoiL3A1Ym13L2V4dGVybi92ZWhpY2xlL21vZGVsIiwiZXAiOlsibGFuZz16aC1UVyIsInNlcnZpY2VOYW1lPWJtd19wYXJ0cyIsIm1kbD1YNSIsInVwZHM9MjAyMy0wNy0xMy0tMTItNTUiXSwid3MiOlt7IndpZCI6Im1vZGVsVGFibGUiLCJwYXRoIjoicyIsImlkIjoiWDUiLCJlcCI6WzAsMV19LHsid2lkIjoibW9kZWxUeXBlVGFibGUiLCJwYXRoIjoidHlwZXMiLCJlcCI6WzAsMiwxLDNdfV19'
    chrome_options=webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(host_url)
    output_folder_path = f'output/{datetime.now().strftime("%y%m%d_%H%M%S")}'
    
    create_folder(output_folder_path)
    
    """
    從車型開始取得技術訊息>限制1>限制2>限制3>總組>功能組>評論 API內容並儲存json
    """
    mdl_list = get_mdl(driver)
    for m in mdl_list:
        get_model_type_path(m,driver,output_folder_path)
        
        
if __name__ == '__main__':
    main()