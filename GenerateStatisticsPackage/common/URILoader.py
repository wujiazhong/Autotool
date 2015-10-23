'''
Created on Oct 22, 2015

@author: wujz
'''
import urllib.request


class URILoader:
    HTTP_ERROR_MSG = "HTTPError: Cannot get connection to {0} on github.com. Please check the internet!\n\n"
    UNIDEC_ERROR_MSG = "UnicodeDecodeError: The {0} has non-unicode character. Please check!\n\n"
    
    UNKNOWN_ERROR_MSG = "Exception: The {0} has an unknown error. Please check!\n\n"
        
    @staticmethod
    def loadURI(uri, file_name):
        try:     
            repos_set_json = urllib.request.urlopen(uri).read().decode('utf-8')
        except urllib.error.HTTPError:
            raise Exception(URILoader.HTTP_ERROR_MSG.format(file_name))           
        except UnicodeDecodeError:
            raise Exception(URILoader.UNIDEC_ERROR_MSG.format(file_name))
        except Exception:
            raise Exception(URILoader.UNKNOWN_ERROR_MSG.format(file_name))      
        return repos_set_json
        