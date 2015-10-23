'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import logging

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
class Logger:
    def __init__(self, filename):
        logging.basicConfig(level=logging.DEBUG, 
                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                         datefmt='%a, %d %b %Y %H:%M:%S',
                         filename=filename,
                         filemode='w')
        self.logger = logging.getLogger()       
        self.configConsole();
           
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warn(msg)
    def error(self, msg):
        self.error(msg)
    
    def configConsole(self):
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')  
        ch = logging.StreamHandler()  
        ch.setFormatter(formatter) 
        self.logger.addHandler(ch)
        
        
        