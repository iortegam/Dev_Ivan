#! /usr/bin/python
#----------------------------------------------------------------------------------------
# Name:
#        pltHDF.py
#
# Purpose:
#
#
#----------------------------------------------------------------------------------------


#---------------
# Import modules
#---------------
import sys
import os
import getopt
import HDFClassRead as dc
import time


def usage():
    ''' Prints to screen standard program usage'''
    print 'pltSet.py -i <inputfile> -?'
    print '  -i <file> : Run pltSet.py with specified input file'
    print '  -?        : Show all flags'

def ckDir(dirName,logFlg=False,exit=False):
    ''' '''
    if not os.path.exists( dirName ):
        print 'Input Directory %s does not exist' % (dirName)
        if logFlg: logFlg.error('Directory %s does not exist' % dirName)
        if exit: sys.exit()
        return False
    else:
        return True    

def ckFile(fName,logFlg=False,exit=False):
    '''Check if a file exists'''
    if not os.path.isfile(fName):
        print 'File %s does not exist' % (fName)
        if logFlg: logFlg.error('Unable to find file: %s' % fName)
        if exit: sys.exit()
        return False
    else:
        return True    

def main(argv):

    #--------------------------------
    # Retrieve command line arguments
    #--------------------------------
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:?')

    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit()

    #-----------------------------
    # Parse command line arguments
    #-----------------------------
    for opt, arg in opts:
        # Check input file flag and path
        if opt == '-i':

            pltInputs = {}

            ckFile(arg,exit=True)

            try:
                execfile(arg, pltInputs)
            except IOError as errmsg:
                print errmsg + ' : ' + arg
                sys.exit()

            if '__builtins__' in pltInputs:
                del pltInputs['__builtins__']               


        # Show all command line flags
        elif opt == '-?':
            usage()
            sys.exit()

        else:
            print 'Unhandled option: ' + opt
            sys.exit()


    #---------------------------------
    # Check for the existance of files 
    # directories from input file
    #---------------------------------
    ckDir(pltInputs['dataDir'], exit=True)
   
    if pltInputs['saveFlg']:  ckDir(os.path.dirname(os.path.realpath(pltInputs['pltFile'])),exit=True)

    #-------------------------
    # Create Instance of Class
    #-------------------------
    gas = dc.PlotHDF(pltInputs['dataDir'], pltInputs['locID'], pltInputs['gasName'],saveFlg= pltInputs['saveFlg'], outFname=pltInputs['pltFile'])

    #----------------------
    # Call to plot profiles
    #----------------------
    gas.PltHDFSet(fltr=pltInputs['fltrFlg'],  iyear=pltInputs['iyear'], imonth=pltInputs['imonth'], iday=pltInputs['iday'], fyear=pltInputs['fyear'], fmonth=pltInputs['fmonth'], fday=pltInputs['fday'],
            sclfct=pltInputs['sclfct'],sclname=pltInputs['sclfctName'], errFlg=pltInputs['errorFlg'],minSZA=pltInputs['minSZA'],maxSZA=pltInputs['maxSZA'],minTC=pltInputs['minTC'],maxTC=pltInputs['maxTC'], 
            tcFlg=pltInputs['tcNegFlg'], pcFlg=pltInputs['pcNegFlg'], szaFlg=pltInputs['szaFlg'],tcMMFlg=pltInputs['tcMMFlg'], dateFlg=pltInputs['dateFlg'])



    ##----
    if pltInputs['saveFlg']: gas.closeFig()

    print('\nFinished Plots.......\n')

    #--------------------------------
    # Pause so user can look at plots
    #--------------------------------
    if not pltInputs['saveFlg']:
        user_input = raw_input('Press any key to exit >>> ')
        sys.exit()           # Exit program        


if __name__ == "__main__":
    main(sys.argv[1:])
