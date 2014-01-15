#-------------------------------------------------------------------------------
# Name:        TestsParserXML
# Purpose:
#
# Author:      Sylvain
#
# Created:     08/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from xml.dom import minidom
from IOSRef import *

def main():
    print "*** Loading IOSReference Tests ***"
    xmldoc = minidom.parse('IOSReference.xml')
    ios = IOSReference(xmldoc)
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

