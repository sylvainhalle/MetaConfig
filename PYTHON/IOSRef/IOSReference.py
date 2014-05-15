from GenericCommand import GenericCommand

def printLog(text):
    print "* [IOSReference]   "+str(text)


class IOSReference:
    def __init__(self, xmldoc):
        self.genericCommandList = []
        self.lastUpdate = None
        self.loadAllXML(xmldoc)


    def loadAllXML(self, xmldoc):
        iosRef = xmldoc.getElementsByTagName('IOSReference')[0]
        self.lastUpdate = iosRef.attributes['lastUpdate'].value

        allGenericCommands = iosRef.getElementsByTagName('GenericCommand')
        for node in allGenericCommands:
            genericCommand = GenericCommand(node)
            self.addGenericCommand(genericCommand)
        printLog("Successfully loaded "+self.__str__())


    def addGenericCommand(self, genericCommand):
        if (isinstance(genericCommand, GenericCommand)):
            self.genericCommandList.append(genericCommand)

    def __str__(self):
        result = "IOSReference [lastUpdate="+str(self.lastUpdate)+", number_of_generic_commands="+str(self.genericCommandList.__len__())+"]"
        for gc in self.genericCommandList:
            result += "   "+gc.__str__()+"\n"
        return result

