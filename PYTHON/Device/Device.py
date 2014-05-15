from DeviceCommand import DeviceCommand

def printLog(text):
    print "* [Device]   "+str(text)


class Device:
    def __init__(self, xmldoc, iosRef = None):
        self.iosRef = iosRef
        self.deviceCommandList = []
        self.name = ""
        self.loadAllXML(xmldoc)



    def loadAllXML(self, xmldoc):
        iosRef = xmldoc.getElementsByTagName('Device')[0]
        self.name = iosRef.attributes['name'].value

        alldeviceCommands = iosRef.getElementsByTagName('DeviceCommand')
        for node in alldeviceCommands:
            deviceCommand = DeviceCommand(node)
            self.addDeviceCommand(deviceCommand)

        printLog("Successfully loaded Device '"+self.name+"'")


    def addDeviceCommand(self, deviceCommand):
        if (isinstance(deviceCommand, DeviceCommand)):
            self.deviceCommandList.append(deviceCommand)

    def __str__(self):
        result = "Device [name="+str(self.name)+", number_of_device_commands="+str(self.deviceCommandList.__len__())+"]\n"
        for dc in self.deviceCommandList:
            result += "   "+dc.__str__()+"\n"
        return result

