# -*- coding: utf-8 -*-  
from optparse import OptionParser 
import urllib.request
import json
import os

RAW_REPOS_SET_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/master/resbundles/{0}/index_for_{1}.json"
RAW_INDEX_KEY = "{0}_extension_index"
RAW_LICENSE_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/{0}/master/LICENSE"
INDENT = '\t'
LICENSE_FILE_NAME = 0
REPOS_NAME_LIST = 1
KEY_LIST = ["license_file_name","repository_names"]

class JSONObj:
    def __init__(self, key, val):
        self.key, self.val = key, val
    
    def getJSONStr(self):
        return "\""+self.key+"\":\""+ self.val +"\",\n"

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
                    
def addObj(repo_name, repo_license_content,license_obj_list):
    license_obj = LicenseItemObj()
    license_obj_list.append(license_obj)
    license_obj.addRepoName(repo_name)
    license_obj.setLicenseContent(repo_license_content)
    license_obj.setLicenseName("license{0}.txt".format(len(license_obj_list)))
    
def convertListToString(list):
    string = "["
    for item in list:
        if isinstance(item, str):
            string += "\""+item+"\",";
    string = string[0:-1]
    string += "]"
    return string
    
if __name__ == "__main__":    
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-s", "--spedir", dest="spedir", action='store', help="Directory to license_index.")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    if options.productName == "modeler":
        repos_set_uri = RAW_REPOS_SET_URI.format('modeler','modeler')
        index_key = RAW_INDEX_KEY.format('modeler')
    elif options.productName == 'stats':
        # wrong spell of statistics
        repos_set_uri = RAW_REPOS_SET_URI.format('statisitcs','stats') 
        index_key = RAW_INDEX_KEY.format('stats')
    else:  
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
        
    if not os.path.isdir(options.spedir):
        parser.error("Please input a valid directory to save license_index.json.") 
    try:   
        print("Script start...") 
        try:     
            repos_set_json = json.loads(urllib.request.urlopen(repos_set_uri).read().decode('utf-8'))[index_key]
        except urllib.error.HTTPError:
            raise Exception("HTTPError: Cannot get connection to site of index on github.com. Please check the internet!\n\n")           
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError: The index file has non-unicode character. Please check!\n\n")
        except ValueError:
            raise Exception("ValueError: The index file has an illegal format. Please check!\n\n") 
        except Exception:
            raise Exception("Exception: The index file has an unknown error. Please check!\n\n")
        
        license_obj_list = []
        j=0
        for repo in repos_set_json:
            j+=1
            try:
                repo_name = repo["repository"]
            except Exception:
                raise Exception("At least one repository in index file does not have repo name. Please check!\n\n")    
            
            repo_license_uri = RAW_LICENSE_URI.format(repo_name)
            try:     
                repo_license_content = urllib.request.urlopen(repo_license_uri).read().decode('utf-8')
            except urllib.error.HTTPError:
                raise Exception("HTTPError: Cannot get connection to site of license on github.com. Please check the internet!\n\n")          
            except UnicodeDecodeError:
                raise Exception("UnicodeDecodeError: The license has non-unicode character. Please check!\n\n")
            except ValueError:
                raise Exception("ValueError: The license has an illegal format. Please check!\n\n") 
            except Exception:
                raise Exception("Exception: The license has an unknown error. Please check!\n\n")
    
            isExistedLicense = False
            for item in license_obj_list:
                if repo_license_content == item.getLicenseContent():
                    isExistedLicense = True
                    item.addRepoName(repo_name)
                    break   
            if not isExistedLicense:
                print(j)
                addObj(repo_name, repo_license_content,license_obj_list)
        print("Start to read license...") 
        index_content = "{\n"+INDENT+"\"license_index\": [\n";
        i=0
        for obj in license_obj_list:
            print("in obj "+str(i))
            i+=1
            index_content += INDENT*2+"{\n"+INDENT*3+"\""+KEY_LIST[LICENSE_FILE_NAME]+"\":"+"\""+obj.getLicenseName()+"\",\n"
            index_content += INDENT*3+"\""+KEY_LIST[REPOS_NAME_LIST]+"\":"+convertListToString(obj.getRepoNameList())+"\n"+INDENT*2+"},\n"
            license_fp = open(os.path.join(options.spedir,obj.getLicenseName()),'w')
            license_fp.write(obj.getLicenseContent())
            license_fp.close()
        print("last")
        index_content = index_content[0:-2]
        index_content += INDENT + "]\n}"
        print("Start to write license to text...") 
        index_fp = open(os.path.join(options.spedir,'license_index.json'),'w')
        index_fp.write(index_content)
    except Exception as e:
        print(str(e))
            
        
                    
            
        
        
        
        
        
        
        
        
        
        
        
        