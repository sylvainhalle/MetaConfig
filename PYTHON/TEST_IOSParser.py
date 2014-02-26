#-------------------------------------------------------------------------------
# Name:        TestsParserXML
# Purpose:
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from xml.dom import minidom
from IOSRef import *
from Device import *


def main():
    print "*** Loading IOSReference Tests ***"

    xmldoc1 = minidom.parse('IOSReference.xml')
    ios = IOSReference(xmldoc1)


    """print "*** Loading Test Device (Device1) ***"

    xmldoc2 = minidom.parse('Device1.xml')
    device = Device(xmldoc2)

    for cmd in device.deviceCommandList:
        print cmd.name
        for prm in cmd.deviceParameterList:
            print "\t"+prm.name+":"
            for value in prm.values:
                print "\t\t%s" % value
            print "-----"
        print "====="
        """

    print "***           END              ***"



if __name__ == '__main__':
    main()



















'''def tests():
    itemlist = xmldoc.getElementsByTagName('CiscoKeyword')
    alltags = xmldoc.getElementsByTagName('IOSReference')[0]
    for node in alltags.childNodes:
        print node.nodeValue
    print "Nombre d'elements CiscoKeyWord:"+str(len(itemlist))
    #print itemlist[0].attributes['word'].value
    for s in itemlist:
        print s.attributes['word'].value
'''

