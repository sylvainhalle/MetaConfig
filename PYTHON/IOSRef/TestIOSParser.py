from xml.dom import minidom
from IOSRef import IOSReference


def main():
    print "*** Loading IOSReference Tests ***"
    xmldoc = minidom.parse('../TestFiles/Real_Example_IOSReference.xml')
    ios = IOSReference(xmldoc)
    print ios.__str__()
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

