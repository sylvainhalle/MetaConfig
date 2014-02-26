#-------------------------------------------------------------------------------
# Name:        CiscoCommandsVersion
# Classes:     CiscoCommandsVersion, CiscoSyntax
# Purpose:     IOSReference
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------
from Term import *

class CiscoCommandsVersion:
    def __init__(self, xmlNode, versionMin=None, versionMax=None, deviceType=None):
        self.ciscoSyntaxList = []

        if xmlNode==None:
            self.versionMin = versionMin
            self.versionMax = versionMax
            self.deviceType = deviceType
        else:
            self.versionMin = xmlNode.attributes['versionMin'].value
            self.versionMax = xmlNode.attributes['versionMax'].value
            self.deviceType = xmlNode.attributes['deviceType'].value
            #load cisco syntaxes
            allCiscoSyntaxes = xmlNode.getElementsByTagName('CiscoSyntax')
            for node in allCiscoSyntaxes:
                ciscoSyntax = CiscoSyntax(node)
                self.addCiscoSyntax(ciscoSyntax)

        from IOSReference import printLog
        printLog("Created "+self.__str__())


    def addCiscoSyntax(self, ciscoSyntax):
        if (isinstance(ciscoSyntax, CiscoSyntax)):
            self.ciscoSyntaxList.append(ciscoSyntax)

    def __str__(self):
        return "CiscoCommandsVersion [versionMin="+str(self.versionMin)+", versionMax="+str(self.versionMax)+", deviceType="+str(self.deviceType)+", number_of_cisco_syntaxes="+str(self.ciscoSyntaxList.__len__())+"]"



class CiscoSyntax:
    def __init__(self, xmlNode, negatable=None):
        self.syntaxTermList = []
        if xmlNode==None:
            self.negatable = negatable
        else:
            self.negatable = xmlNode.attributes['negatable'].value
            #load syntax terms
            allSyntaxTerms = xmlNode.getElementsByTagName('SyntaxTerm')
            for node in allSyntaxTerms:
                syntaxTerm = SyntaxTerm(node)
                self.addSyntaxTerm(syntaxTerm)

        from IOSReference import printLog
        printLog("Created "+self.__str__())

    def addSyntaxTerm(self, syntaxTerm):
        if (isinstance(syntaxTerm, SyntaxTerm)):
            self.syntaxTermList.append(syntaxTerm)

    def __str__(self):
        return "CiscoSyntax [negatable="+str(self.negatable)+", number_of_syntax_terms="+str(self.syntaxTermList.__len__())+"]"