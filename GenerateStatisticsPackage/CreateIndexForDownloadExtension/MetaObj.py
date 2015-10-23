'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import re
from common.JSONObj import JSONObj

class MetaObj:        
    INDENT = '\t'
    EXTENSION_JSON_TITLE = "extension_detail_info"
    '''
    initialize a MeatObj to save manifest content 
    Input: raw content in MANIFEST.MF
    Output: none
    '''
    def __init__(self,meta_file):  
        self.key_list = []
        meta_content = '' 
        try:
            meta_content, self.key_list = self.parseMetaContent(meta_file)
        except IOError as e:
            print("Manifest file open error: "+str(e))
            raise e
        except Exception as e:
            print("Manifest file format error: "+str(e))
            raise e
        
        self.meta_list = []    
            
        for key in self.key_list:
            val = re.findall(key+"\s*:\s*(.+?)\n",meta_content,re.S)
            if len(val) == 0:
                continue
            self.meta_list.append(JSONObj(key,val[0]))
        
    
    '''
    parse content in manifest file, eliminate extra '\n' and space
    Input: manifest file path
    Output: A string eliminated space and \n in one item 
    '''
    def parseMetaContent(self,meta_file):
        try:
            fp = open(meta_file, 'r')
            meta_content = fp.read()
        except IOError as err:
            raise err
        
        if meta_content != '':
            line_list = meta_content.split('\n')
            modified_str, temp, key_list = '', '', []

            for item in line_list:  
                item = item.replace("\"", "\'")         
                if item[0:1] == ' ':
                    temp = temp+item[1:]            
                else:
                    if len(temp) != 0:
                        modified_str += temp+'\n'
                    temp = item
                    
                    key = re.findall("(.+?)\s*:",item)
                    if len(key) != 0:
                        key_list.append(key[0])
                    elif item != '':
                        raise Exception("Error format of MANIFEST file. One line must only have one ':'")
        return modified_str, key_list
    
    def generateExtensionJSON(self):
        try:
            if len(self.meta_list) == 0:
                raise Exception("Error format of MANIFEST file.")
        except Exception as e:
            raise e
        
        extension_json = MetaObj.INDENT*2+"\""+MetaObj.EXTENSION_JSON_TITLE+"\": {\n"    
        for item in  self.meta_list:
            extension_json += MetaObj.INDENT*3 + item.getJSONStr()
        
        extension_json = extension_json[0:-2]+'\n'
        extension_json += MetaObj.INDENT*2 + "}\n"  
        return extension_json    