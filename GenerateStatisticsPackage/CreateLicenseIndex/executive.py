'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
from common.Logger import Logger
from common.URILoader import URILoader
from optparse import OptionParser 
from CreateLicenseIndex.LicenseItemObj import LicenseItemObj
from CreateLicenseIndex.LicenseIndexItemStr import LicenseIndexItemStr
import os,json

RAW_REPOS_SET_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/master/resbundles/{0}/index_for_{1}.json"
RAW_INDEX_KEY = "{0}_extension_index"
RAW_LICENSE_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/{0}/master/LICENSE"
RAW_LICENSE_NAME = "license{0}.txt"
INDENT = '\t'
LICENSE_FILE_NAME = 0
REPOS_NAME_LIST = 1
KEY_LIST = ["license_file_name","repository_names"]
LOG_INFO = "logLicenseIndex.txt"
LICENSE_DIR = 'license'

class CreateLicenseIndex():
    @staticmethod
    def CreateIndex(*args):
        print("size"+str(len(args)))
        outdir = args[0]
        product = args[1]
        
        if product == "modeler":
            repos_set_uri = RAW_REPOS_SET_URI.format('modeler','modeler')
            index_key = RAW_INDEX_KEY.format('modeler')
        elif product == 'stats':
            # wrong spell of statistics
            repos_set_uri = RAW_REPOS_SET_URI.format('statisitcs','stats') 
            index_key = RAW_INDEX_KEY.format('stats')
        
        try:
            lic_path = os.path.join(outdir,LICENSE_DIR)   
            os.mkdir(lic_path)
            logger = Logger(os.path.join(lic_path,LOG_INFO))
            logger.info("Script start ...")
        except IOError as e:  
            raise IOError("IOError: Need permission to write in "+outdir)
            
        try:   
            try:     
                repos_set_json = json.loads(URILoader.loadURI(repos_set_uri, "index file"))
            except ValueError as e:
                raise Exception("ValueError: The {0} has an illegal format. Please check!\n\n".format("index file"))
            except Exception as e:
                raise e
            
            try:
                repos_set_json_index = repos_set_json[index_key]
            except Exception as e:
                raise e
            license_obj_list = []
            for repo in repos_set_json_index:
                try:
                    repo_name = repo["repository"]
                except Exception:
                    raise Exception("At least one repository in index file does not have repo name. Please check!\n\n")    
                
                repo_license_uri = RAW_LICENSE_URI.format(repo_name)
                
                try:     
                    repo_license_content = URILoader.loadURI(repo_license_uri, "license file")
                except Exception as e:
                    raise e
        
                isExistedLicense = False
                for item in license_obj_list:
                    if repo_license_content == item.getLicenseContent():
                        isExistedLicense = True
                        item.addRepoName(repo_name)
                        break   
                if not isExistedLicense:
                    addObj(repo_name, repo_license_content,license_obj_list)
            
            print("Start to read license...") 
            index_content = "{\n"+INDENT+"\"license_index\": [\n";
            
            for obj in license_obj_list:
                index_item_str = LicenseIndexItemStr.getItemStr(obj)
                index_content += index_item_str
                license_fp = open(os.path.join(lic_path,obj.getLicenseName()),'w')
                license_fp.write(obj.getLicenseContent())
                license_fp.close()

            index_content = index_content[0:-2]
            index_content += '\n' + INDENT + "]\n}"
            print("Start to write license to text...") 
            index_fp = open(os.path.join(lic_path,'license_index.json'),'w')
            index_fp.write(index_content)
        except Exception as e:
            logger.error(str(e))
                    
def addObj(repo_name, repo_license_content,license_obj_list):
    license_obj = LicenseItemObj()
    license_obj_list.append(license_obj)
    license_obj.addRepoName(repo_name)
    license_obj.setLicenseContent(repo_license_content)
    license_obj.setLicenseName(RAW_LICENSE_NAME.format(len(license_obj_list)))
    
if __name__ == "__main__":    
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--outdir", dest="outdir", action='store', help="Directory to save license index.")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    if options.productName != "modeler" and options.productName != "stats":   
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
        
    if not os.path.isdir(options.outdir):
        parser.error("Please input a valid directory to save license_index.json.")
    
    try:
        CreateLicenseIndex.CreateIndex(options.outdir, options.productName)
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e))
        
    
            
        
                    
            
        
        
        
        
        
        
        
        
        
        
        
        