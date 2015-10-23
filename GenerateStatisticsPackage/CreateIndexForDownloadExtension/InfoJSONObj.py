'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import re
import json
import urllib.request
from common.JSONObj import JSONObj

class InfoJSONObj:
    KEY_LIST = ['type', 'provider', 'software', 'language', 'category', 'promotion']
    TYPE, PROVIDER, SOFTWARE, LANGUAGE, CATEGORY, PROMOTION = 0,1,2,3,4,5
    RAW_INFO_JSON_URL = 'https://raw.githubusercontent.com/IBMPredictiveAnalytics/repos_name/master/info.json'

    def __init__(self, repo_name):       
        repo_info_json_url = re.sub('repos_name', repo_name, InfoJSONObj.RAW_INFO_JSON_URL)
        try:
            self.repo_info_json = json.loads(urllib.request.urlopen(repo_info_json_url).read().decode('utf-8'))
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError: "+repo_name+"'s info.json has non-unicode character. Please check!"+"\nSwitch to next repo.\n\n")
        except urllib.error.HTTPError:
            raise Exception("HTTPError: "+repo_name+"'s info.json does not have info.json, but this may not be a problem. Please check!"+"\nSwitch to next repo.\n\n") 
        except ValueError:
            raise Exception("ValueError: "+repo_name+"'s info.json has an illegal format. Please check!"+"\nSwitch to next repo.\n\n") 
        except Exception:
            raise Exception("Exception: "+repo_name+"'s info.json has an unknown error. Please check!"+"\nSwitch to next repo.\n\n")
        
        self.item_list = []
        for key in InfoJSONObj.KEY_LIST:
            try:
                if type(self.repo_info_json[key]) == list:
                    val = self.repo_info_json[key][0]
                else:
                    val = self.repo_info_json[key]
                self.item_list.append(JSONObj(key,val.strip()))
            except:
                raise ValueError("info.json missed some of the items below:\n"
                                "type, provider, software, language, category, promotion.")  
