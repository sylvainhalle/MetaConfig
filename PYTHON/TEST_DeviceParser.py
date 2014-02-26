#-------------------------------------------------------------------------------
# Name:        TestsParserXML_Device
# Purpose:
#
# Author:      Clement
#
# Created:     10/12/2013
# Copyright:   (c) Clement 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from Device import *
from xml.dom import minidom


def main():
    print "*** Loading Device Tests ***"
    xmldoc = minidom.parse('Device1.xml')
    device = Device(xmldoc)
    '''for cmd in device.deviceCommandList:
        print cmd.name
        for prm in cmd.deviceParameterList:
            print "\t"+prm.name+":"
            for value in prm.values:
                print "\t\t%s" % value
            print "-----"
        print "====="'''
    print device.toString()


    print "***           END              ***"

if __name__ == '__main__':
    main()
