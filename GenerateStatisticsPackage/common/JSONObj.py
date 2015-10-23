'''
Created on Oct 22, 2015

@author: wujz
'''

class JSONObj:
    def __init__(self, key, val):
        self.key, self.val = key, val
    
    def getJSONStr(self):
        return "\""+self.key+"\":\""+ self.val +"\",\n"
    
    @staticmethod
    def createJSONStr(key, value):
        return "\""+key+"\":\""+ value +"\",\n"