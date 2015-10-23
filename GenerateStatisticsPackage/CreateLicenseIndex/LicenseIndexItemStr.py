'''
Created on Oct 23, 2015

@author: wujz
'''
'''
Created on Oct 22, 2015

@author: wujz
'''
from common.JSONObj import JSONObj

INDENT = '\t'
LICENSE_FILE_NAME = 0
REPOS_NAME_LIST = 1
KEY_LIST = ["license_file_name","repository_names"]

class LicenseIndexItemStr:
    @staticmethod
    def convertListToString(list):
        string = "["
        for item in list:
            if isinstance(item, str):
                string += "\""+item+"\",";
        string = string[0:-1]
        string += "]"
        return string  
    
    @staticmethod
    def getItemStr(LicenseItemObj):
        item_str = INDENT*2 + "{\n"
        item_str += INDENT*3 + JSONObj.createJSONStr(KEY_LIST[LICENSE_FILE_NAME], LicenseItemObj.getLicenseName())
        item_str += INDENT*3 + JSONObj.createJSONStr(KEY_LIST[REPOS_NAME_LIST], LicenseIndexItemStr.convertListToString(LicenseItemObj.getRepoNameList()))[1:-2]\
                             + '\n' + INDENT*2 + '},\n'
        return item_str  