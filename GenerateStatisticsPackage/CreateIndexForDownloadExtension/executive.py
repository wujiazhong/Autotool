# -*- coding: utf-8 -*-  
from CreateIndexForDownloadExtension.GithubApiInfoObj import GithubApiInfoObj
from CreateIndexForDownloadExtension.InfoJSONObj import InfoJSONObj
from CreateIndexForDownloadExtension.MetaObj import MetaObj
from common.Logger import Logger
from optparse import OptionParser 

import urllib.request
import zipfile
import os
import re
import time 
import shutil

#"https://github.com/IBMPredictiveAnalytics/repos_name/blob/master/repos_name.spe?raw=true"
SPE_DOWNLOAD_URL = "https://github.com/IBMPredictiveAnalytics/repos_name/raw/master/repos_name.spe"
IMG_DOWNLOAD_URL = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/repos_name/master/default.png"
FILE_NAME= "MANIFEST.MF"
INDEX_FILE = 'index.json'
INDENT = '\t'
LOG_INFO = "logExtensionIndex.txt"
META_DIR = 'META-INF'      

class CreateIndexForDownloadExtension():
    @staticmethod
    def createIndex(*args):
        indexdir = args[0]
        product = args[1]
        START_WORDS = "{\n\"productname_extension_index\":[\n"    
        cur_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))  
        root_spe_dir = os.path.join(indexdir,"spe"+cur_time)        
        try:
            os.mkdir(root_spe_dir)
            logger = Logger(os.path.join(indexdir,LOG_INFO))
            logger.info("Script start ...")
        except IOError as e:  
            raise IOError("IOError: Need permission to write in "+indexdir)
        
        index_for_extension = re.sub('productname', product, START_WORDS)
        whole_product_name = getWholeProductName(product) 
        print("start to get repo data from github ...")
        logger.info("start to get repo data from github ...")
        
        i=0
        ok_repo_num = 0
        try:        
            githubApiInfo_obj = GithubApiInfoObj()
            for item in githubApiInfo_obj.item_list:
                i+=1
                print(i) 
                
                index_for_extension_item = INDENT+"{\n"
                index_for_extension_item += generateJSONStr(item)
                
                repo_name = item[githubApiInfo_obj.__class__.REPOSITORY].val
                logger.info(str(i)+"th repo: "+repo_name)
                print(repo_name)
    
                try:
                    info_json = InfoJSONObj(repo_name)
                except ValueError as e:
                    raise e
                except Exception as e:
                    print(str(e))
                    logger.warning(str(e))
                    continue
                    
                index_for_extension_item += generateJSONStr(info_json.item_list)
                repo_software = info_json.item_list[info_json.__class__.SOFTWARE].val
                index_for_extension_item += INDENT*2 + "\"download_link\":" +"\"" + re.sub('repos_name', repo_name, SPE_DOWNLOAD_URL) +"\",\n"
                index_for_extension_item += INDENT*2 + "\"image_link\":" +"\"" + re.sub('repos_name', repo_name, IMG_DOWNLOAD_URL) +"\",\n"
                
                if repo_software != whole_product_name:
                    print("This is not a " + whole_product_name + " repo.\nSwitch to next repo.\n\n\n")
                    logger.info("This is not a " + whole_product_name + " repo.\nSwitch to next repo.")
                    continue
                
                repo_spe_url = re.sub('repos_name', repo_name, SPE_DOWNLOAD_URL)
                spe_name = repo_name+".spe"
                
                spe_saving_path = os.path.join(root_spe_dir,repo_name)
                os.mkdir(spe_saving_path)
                
                try:
                    urllib.request.urlretrieve(repo_spe_url, os.path.join(spe_saving_path,spe_name))
                    srcZip = zipfile.ZipFile(os.path.join(spe_saving_path,spe_name), "r", zipfile.ZIP_DEFLATED)
                except:
                    print("This repo '"+repo_name+"' does not have spe package. Please check!"+"\nSwitch to next repo.\n\n\n")
                    logger.warning("This repo '"+repo_name+"' does not have spe package. Please check!"+"\nSwitch to next repo.")
                    continue
                
                for file in srcZip.namelist():
                    if not os.path.isdir(spe_saving_path):     
                        os.mkdir(spe_saving_path)
                    if FILE_NAME in file:
                        srcZip.extract(file, spe_saving_path)
                srcZip.close()
                
                meta_path = os.path.join(spe_saving_path, META_DIR, FILE_NAME)
                metaObj = MetaObj(meta_path)
                index_for_extension_item += metaObj.generateExtensionJSON()
                index_for_extension_item += INDENT + "},\n" 
                index_for_extension += index_for_extension_item
                print("Successfully get data!\n\n")
                ok_repo_num += 1
                logger.info("Successfully get data!\n")
    
            index_for_extension = index_for_extension[0:-2]
            index_for_extension += '\n]\n}'
            index_for_extension_fp = open(os.path.join(indexdir, INDEX_FILE),'w')
            index_for_extension_fp.write(index_for_extension)  
            index_for_extension_fp.close()   
                
        except Exception as e:        
            print(str(e))
            logger.error(str(e))
        finally:
            print("Totally get "+str(ok_repo_num)+" repo data successfully!\n\n")
            logger.info("Totally get "+str(ok_repo_num)+" repo data successfully!")
            clear(root_spe_dir)
            
def getWholeProductName(product_name):
    if(product_name == "stats"):
        return "SPSS Statistics"
    else:
        return "SPSS Modeler"

def generateJSONStr(json_obj_list):
    json_item_str =''
    for item in json_obj_list:            
        json_item_str += INDENT*2 + item.getJSONStr() 
    return json_item_str

def clear(spedir):
    if os.path.isdir(spedir):
        os.system(r"C:\Windows\System32\attrib -r "+ spedir+"\*.* " + " /s /d")
        shutil.rmtree(spedir, ignore_errors = True)

if __name__ == '__main__':    
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index file.")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose index for which product: 1. SPSS Modeler 2. SPSS Statistics.")
    (options, args) = parser.parse_args() 

    if not os.path.isdir():
        parser.error("Please input a valid directory to create index file.")   
    if options.productName != "modeler" and options.productName != "stats":  
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try:
        CreateIndexForDownloadExtension.createIndex(options.outdir, options.productName)
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e))
    