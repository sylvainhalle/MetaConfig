#-------------------------------------------------------------------------------
# Name:        Device
# Purpose:     Device
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from DeviceCommand import *

def printLog(text):
    print "* [Device]   "+str(text)


class Device:
    def __init__(self, xmldoc):
        self.deviceCommandList = []
        self.name = ""
        self.loadAllXML(xmldoc)



    def loadAllXML(self, xmldoc):
        printLog("Starting XML parsing")

        iosRef = xmldoc.getElementsByTagName('Device')[0]
        self.name = iosRef.attributes['name'].value

        alldeviceCommands = iosRef.getElementsByTagName('DeviceCommand')
        for node in alldeviceCommands:
            deviceCommand = DeviceCommand(node)
            self.addDeviceCommand(deviceCommand)

        printLog("Successfully loaded "+self.toString())


    def addDeviceCommand(self, deviceCommand):
        if (isinstance(deviceCommand, DeviceCommand)):
            self.deviceCommandList.append(deviceCommand)

    def toString(self):
        return "Device [name="+str(self.name)+", number_of_device_commands="+str(self.deviceCommandList.__len__())+"]"

