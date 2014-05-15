from DeviceParameter import DeviceParameter

class DeviceCommand:
    def __init__(self, xmlNode, ref_cmd=None, name=None, negated=False):
        self.deviceParametersAndCommandsList = []

        if xmlNode==None:
            self.ref_cmd = ref_cmd
            self.name = name
            self.negated = negated
        else:
            self.ref_cmd = xmlNode.attributes['ref_cmd'].value
            self.name = xmlNode.attributes['name'].value
            self.negated = xmlNode.attributes['negated'].value
            #load device parameters
            alldeviceParameters = xmlNode.getElementsByTagName('DeviceParameter')
            for node in alldeviceParameters:
                deviceParameter = DeviceParameter(node)
                self.addDeviceParameterOrCommand(deviceParameter)
            #load device commands
            alldeviceCommands = xmlNode.getElementsByTagName('DeviceCommand')
            for node in alldeviceCommands:
                deviceCommand = DeviceCommand(node)
                self.addDeviceParameterOrCommand(deviceCommand)

        """from IOSReference import printLog
        printLog("Created "+self.toString())"""

    def addDeviceParameterOrCommand(self, deviceParameterOrCommand):
        if (isinstance(deviceParameterOrCommand, DeviceParameter) | isinstance(deviceParameterOrCommand, DeviceCommand)):
            self.deviceParametersAndCommandsList.append(deviceParameterOrCommand)

    def __str__(self):
        result = "DeviceCommand [ref_cmd="+str(self.ref_cmd)+", name='"+str(self.name)+", negated="+self.negated+"]\n"
        for dpc in self.deviceParametersAndCommandsList:
            result += "   "+dpc.__str__()+"\n"
        return result
