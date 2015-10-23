'''
Created on Oct 22, 2015

@author: wujz
'''
from CreateLicenseStatsZIP.executive
from optparse import OptionParser 

if __name__ == "__main__":    
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--outdir", dest="outdir", action='store', help="Directory to save license index.")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    CreateLicenseIndex.CreateIndex((options.outdir, options.productName))