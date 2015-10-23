'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import math
import json
import urllib.request
from common.JSONObj import JSONObj

class GithubApiInfoObj:
    GITHUB_API_URL = "https://api.github.com/orgs/ibmpredictiveanalytics/repos?page={0}&per_page={1}"
    MAX_REPO_NUM = 1000
    PER_PAGE = 100 
    KEY_LIST = ['repository','description','pushed_at']
    REPOSITORY, DESCRIPTION, PUSHED_AT = 0,1,2
    
    def __init__(self):
        self.item_list = []
        for page_index in range(1, math.floor(GithubApiInfoObj.MAX_REPO_NUM/GithubApiInfoObj.PER_PAGE)+1):  
            try:
                pageName = GithubApiInfoObj.GITHUB_API_URL.format(page_index,GithubApiInfoObj.PER_PAGE)
                api_json_data = json.loads(urllib.request.urlopen(pageName).read().decode('utf-8'))
            except:
                raise Exception("Cannot request data from github api: '"+pageName+"'.\n")
            
            if len(api_json_data) == 0:
                break
                        
            for item in api_json_data:  
                temp_json_list = []
                #ignore .io repository
                if('IBMPredictiveAnalytics.github.io' == item['name']):
                    continue 
                  
                for key in GithubApiInfoObj.KEY_LIST:
                    if key == 'repository':
                        key_name_in_api = 'name'
                    else:
                        key_name_in_api= key
        
                    try:
                        temp_json_list.append(JSONObj(key,item[key_name_in_api].strip())) 
                    except:
                        raise Exception("Github api ("+GithubApiInfoObj.GITHUB_API_URL+") does not provide information of "+key+". Please check!\n")
                
                self.item_list.append(temp_json_list)   