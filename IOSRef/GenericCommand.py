#-------------------------------------------------------------------------------
# Name:        GenericCommand
# Classes:     GenericCommand, AuxiliarCommand, GenericParameter
# Purpose:     IOSReference
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from CiscoCommandsVersion import *


class AuxiliarCommand:
    def __init__(self, xmlNode, versionMin=None, versionMax=None, genericCommandNeeded=None):
        if xmlNode==None:
            self.versionMin = versionMin
            self.versionMax = versionMax
            self.genericCommandNeeded = genericCommandNeeded
        else:
            self.versionMin = xmlNode.attributes['versionMin'].value
            self.versionMax = xmlNode.attributes['versionMax'].value
            self.genericCommandNeeded = xmlNode.attributes['guid'].value

        from IOSReference import printLog
        printLog("Created "+self.__str__())


    def __str__(self):
        return "AuxiliarCommand [versionMin="+str(self.versionMin)+", versionMax="+str(self.versionMax)+", uid_genericCommandNeeded="+str(self.genericCommandNeeded)+"]"







class GenericParameter:
    def __init__(self, xmlNode, uid=None, name=None):
        if xmlNode==None:
            self.name = name
            self.uid = uid
        else:
            self.uid = xmlNode.attributes['uid'].value
            self.name = xmlNode.attributes['name'].value

        from IOSReference import printLog
        printLog("Created "+self.__str__())


    def __str__(self):
        return "GenericParameter [uid="+str(self.uid)+", name='"+str(self.name)+"']"





class GenericCommand:
    def __init__(self, xmlNode, uid=None, genericName=None):
        self.ciscoCommandsVersionList = []
        self.genericParameterList = []
        self.auxiliarCommandList = []

        if xmlNode==None:
            self.uid = uid
            self.genericName = genericName
        else:
            self.uid = xmlNode.attributes['uid'].value
            self.genericName = xmlNode.attributes['genericName'].value
            #load generic parameters
            allGenericParameters = xmlNode.getElementsByTagName('GenericParameter')
            for node in allGenericParameters:
                genericParameter = GenericParameter(node)
                self.addGenericParameter(genericParameter)
            #load cisco commands version
            allCiscoCommandsVersion = xmlNode.getElementsByTagName('CiscoCommandsVersion')
            for node in allCiscoCommandsVersion:
                ciscoCommandsVersion = CiscoCommandsVersion(node)
                self.addCiscoCommandsVersion(ciscoCommandsVersion)
            #load auxiliar commands
            allAuxiliarCommands = xmlNode.getElementsByTagName('AuxiliarCommand')
            for node in allAuxiliarCommands:
                auxiliarCommand = AuxiliarCommand(node)
                self.addAuxiliarCommand(auxiliarCommand)

        from IOSReference import printLog
        printLog("Created "+self.__str__())


    def addCiscoCommandsVersion(self, ciscoCommandsVersion):
        if (isinstance(ciscoCommandsVersion, CiscoCommandsVersion)):
            self.ciscoCommandsVersionList.append(ciscoCommandsVersion)

    def addAuxiliarCommand(self, auxiliarCommand):
        if (isinstance(auxiliarCommand, AuxiliarCommand)):
            self.auxiliarCommandList.append(auxiliarCommand)

    def addGenericParameter(self, genericParameter):
        if (isinstance(genericParameter, GenericParameter)):
            self.genericParameterList.append(genericParameter)

    def __str__(self):
        return "GenericCommand [uid="+str(self.uid)+", name='"+str(self.genericName)+"', number_of_cisco_commands_versions="+str(self.ciscoCommandsVersionList.__len__())+", number_of_generic_parameters="+str(self.genericParameterList.__len__())+", number_of_auxiliar_commands="+str(self.auxiliarCommandList.__len__())+"]"
