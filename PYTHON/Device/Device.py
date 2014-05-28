from DeviceCommand import DeviceCommand
from DeviceParameter import DeviceParameter

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
            
    def countParams(self):
        count = 0
        for cmd in self.deviceCommandList:
            count += self.countParam(cmd)
        return count
            
    def countParam(self, node):
        count = 0
        if isinstance(node, DeviceParameter):
            count+= node.nbParam()
        elif isinstance(node, DeviceCommand):
            count+= node.nbParam()
            for paramOrCmd in node.deviceParametersAndCommandsList:
                count += self.countParam(paramOrCmd)
        return count

    def __str__(self):
        result = "Device [name="+str(self.name)+", number_of_device_commands="+str(self.deviceCommandList.__len__())+"]\n"
        for dc in self.deviceCommandList:
            result += "   "+dc.__str__()+"\n"
        return result

