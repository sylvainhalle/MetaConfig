#-------------------------------------------------------------------------------
# Name:        GenericCommand
# Classes:     GenericCommand, AuxiliarCommand, deviceParameter
# Purpose:     IOSReference
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------


class DeviceParameter:
    def __init__(self, xmlNode, ref_param=None, name=None):
        if xmlNode==None:
            self.name = name
            self.ref_param = ref_param
            self.values = []
        else:
            self.ref_param = xmlNode.attributes['ref_param'].value
            self.name = xmlNode.attributes['name'].value
            self.values = []
            for value in xmlNode.getElementsByTagName("Value"):
                for v in value.childNodes:
                    self.values.append(v.data)

        """from IOSReference import printLog
        printLog("Created "+self.toString())"""


    def toString(self):
        return "DeviceParameter [name='"+str(self.name)+", ref_param="+str(self.ref_param)+"]"





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

    def toString(self):
        result = "DeviceCommand [ref_cmd="+str(self.ref_cmd)+", name='"+str(self.name)+", negated="+self.negated+"]\n"
        for dpc in self.deviceParametersAndCommandsList:
            result += "   "+dpc.toString()+"\n"
        return result
