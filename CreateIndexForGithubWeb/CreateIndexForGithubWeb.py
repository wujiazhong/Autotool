# -*- coding: utf-8 -*-  
import urllib.request
import urllib.error
import json,re, math, os
from optparse import OptionParser 

UNICODE_ERROR_LIST = []
HTTP_ERROR_LIST = []
VALUE_ERROR_LIST = []
OTHER_ERROR_LIST = []
MAX_REPO_NUM = 1000
PER_PAGE = 100
INDENT_SPACE = '\t'
INDEX_NAME = 'index_for_web.json'


def createIndexForWeb(index_for_web_path):
    page_num = math.floor(MAX_REPO_NUM/PER_PAGE)
    #read name and desc info from api.github.com
    api_url = "https://api.github.com/orgs/ibmpredictiveanalytics/repos?page={0}&per_page={1}"
    raw_info_json_url = 'https://raw.githubusercontent.com/IBMPredictiveAnalytics/repos_name/master/info.json'

    #key_list for repository info.json
    key_list = ['type', 'provider', 'software', 'language', 'category', 'promotion']
       
    index_for_web_json = "{\n\"repository_index\":[\n"
    index_for_web = open(index_for_web_path,'w')
    
    for page_index in range(1, page_num+1):
        cur_api_url = api_url.format(str(page_index),str(PER_PAGE))
        api_json_data = json.loads(urllib.request.urlopen(cur_api_url).read().decode('utf-8'))
        
        if len(api_json_data) == 0:
            break

        for item in api_json_data:
            repo_name = item['name']
            #ignore .io repository
            if('IBMPredictiveAnalytics.github.io' == repo_name):
                continue
            
            repo_desc = item['description']
            repo_push_time = item['pushed_at']
            repo_info_json_url = re.sub('repos_name', repo_name, raw_info_json_url)
            
            try:
                repo_info_json = json.loads(urllib.request.urlopen(repo_info_json_url).read().decode('utf-8'))
            except UnicodeDecodeError:
                UNICODE_ERROR_LIST.append(repo_name+"  "+repo_push_time)
                continue
            except urllib.error.HTTPError:
                HTTP_ERROR_LIST.append(repo_name+"  "+repo_push_time)
                continue
            except ValueError:
                VALUE_ERROR_LIST.append(repo_name+"  "+repo_push_time)
                continue
            except Exception:
                OTHER_ERROR_LIST.append(repo_name+"  "+repo_push_time)
                continue
            
            json_item = INDENT_SPACE+'{\n'
            json_item += INDENT_SPACE + INDENT_SPACE + "\"repository\":" +"\"" + repo_name +"\",\n" 
            json_item += INDENT_SPACE + INDENT_SPACE + "\"description\":" +"\"" + repo_desc +"\",\n"
            json_item += INDENT_SPACE + INDENT_SPACE + "\"pushed_at\":" +"\"" + repo_push_time +"\",\n" 
            
            for key in key_list:
                if type(repo_info_json[key]) == list:
                    val = repo_info_json[key][0]
                else:
                    val = repo_info_json[key]
                json_item += INDENT_SPACE + INDENT_SPACE + "\"" + key + "\":" + "\"" + val + "\",\n"
            json_item = json_item[0:-2]+'\n'
            json_item += INDENT_SPACE + "},\n"  
            index_for_web_json += json_item
    index_for_web_json = index_for_web_json[0:-2]
    index_for_web_json += '\n]\n}'
    index_for_web.write(index_for_web_json)  
    index_for_web.close()

def printError(error_list, error_msg):
    for repo_name in error_list:
        print(error_msg+": "+repo_name)

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index_for_web file.")
    (options, args) = parser.parse_args() 
    
    if getattr(options, 'outdir') == None or not os.path.isdir(options.outdir):
        parser.error("Please input a valid directory to save index_for_web.json file\n\n")  
    else:
        index_for_web_path = os.path.join(options.outdir,INDEX_NAME)
    
    print("The index_for_web.json is saved in:"+index_for_web_path)         
    createIndexForWeb(index_for_web_path)
    print("Cannot get below repositories information. Please check!")
    printError(UNICODE_ERROR_LIST, "UnicodeDecodeError")
    printError(HTTP_ERROR_LIST, "HTTPError")
    printError(VALUE_ERROR_LIST, "ValueError")
    printError(OTHER_ERROR_LIST, "Other exception")