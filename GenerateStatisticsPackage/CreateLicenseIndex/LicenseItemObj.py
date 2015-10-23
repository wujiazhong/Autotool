'''
Created on Oct 23, 2015

@author: wujz
'''
'''
Created on Oct 22, 2015

@author: wujz
'''
class LicenseItemObj:
    def __init__(self):
        self.license_name, self.repo_name_list, self.license_content = "", [], ""
    
    def addRepoName(self, repo_name):   
        self.repo_name_list.append(repo_name) 
        
    def getRepoNameList(self):
        return self.repo_name_list 
    
    def setLicenseContent(self, license_content):
        self.license_content = license_content
        
    def getLicenseContent(self):
        return self.license_content
        
    def setLicenseName(self, license_name):
        self.license_name = license_name
        
    def getLicenseName(self):
        return self.license_name