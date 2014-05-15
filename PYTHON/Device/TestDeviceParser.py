from xml.dom import minidom
from Device import Device


def main():
    print "*** Loading Device Tests ***"
    xmldoc = minidom.parse('../TestFiles/Real_Example_Device.xml')
    device = Device(xmldoc)
    print device.__str__()
    print "***           END        ***"


if __name__ == '__main__':
    main()
