class AtomicTerm:
    def __init__(self):
        pass


class SyntaxTerm:
    def __init__(self, xmlNode, cardinalityMin=None, cardinalityMax=None):
        self.atomicTermList = []

        if xmlNode==None:
            self.cardinalityMin = cardinalityMin
            self.cardinalityMax = cardinalityMax
        else:
            self.cardinalityMin = xmlNode.attributes['cardinalityMin'].value
            self.cardinalityMax = xmlNode.attributes['cardinalityMax'].value
            #load atomic terms
            allAtomicTerms = xmlNode.childNodes
            for node in allAtomicTerms:
                if node.nodeType != node.ELEMENT_NODE:
                    continue
                atomicTerm = None
                if node.tagName=="CiscoKeyword":
                    atomicTerm = CiscoKeyword(node)
                if node.tagName=="CiscoParameter":
                    atomicTerm = CiscoParameter(node)
                if node.tagName=="TermOrTerm":
                    atomicTerm = TermOrTerm(node)
                if atomicTerm!=None:
                    self.addAtomicTerm(atomicTerm)

        #from IOSReference import printLog
        #printLog("Created "+self.__str__())

    def addAtomicTerm(self, atomicTerm):
        if (isinstance(atomicTerm, AtomicTerm)):
            self.atomicTermList.append(atomicTerm)

    def __str__(self):
        return "SyntaxTerm [cardinalityMin="+str(self.cardinalityMin)+", cardinalityMax="+str(self.cardinalityMax)+", number_of_atomic_terms="+str(self.atomicTermList.__len__())+"]"





class ListOptionItem:
    def __init__(self, xmlNode, value=None):
        if xmlNode==None:
            self.value = value
        else:
            self.value = xmlNode.nodeValue

        #from IOSReference import printLog
        #printLog("Created "+self.__str__())


    def __str__(self):
        return "ListOptionItem [value="+str(self.value)+"]"





class CiscoParameter(AtomicTerm):
    def __init__(self, xmlNode, name=None, cardinalityMin=None, cardinalityMax=None, description=None, typeParameter=None, genericParameter=None):
        self.listOptionItemList = []

        if xmlNode==None:
            self.name = name
            self.cardinalityMin = cardinalityMin
            self.cardinalityMax = cardinalityMax
            self.description = description
            self.typeParameter = typeParameter
            self.genericParameter = genericParameter
        else:
            self.name = xmlNode.attributes['name'].value
            self.cardinalityMin = xmlNode.attributes['cardinalityMin'].value
            self.cardinalityMax = xmlNode.attributes['cardinalityMax'].value
            self.genericParameter = xmlNode.attributes['guid'].value
            try:
                self.description = xmlNode.attributes['description'].value
                self.typeParameter = xmlNode.attributes['typeParameter'].value
            except:
                self.description = ""
                self.typeParameter = ""

            #load list option items
            allListOptionItems = xmlNode.getElementsByTagName('ListOptionItem')
            for node in allListOptionItems:
                listOptionItem = ListOptionItem(node)
                self.addListOptionItem(listOptionItem)

        #from IOSReference import printLog
        #printLog("Created "+self.__str__())



    def addListOptionItem(self, listOptionItem):
        if (isinstance(listOptionItem, ListOptionItem)):
            self.listOptionItemList.append(listOptionItem)


    def __str__(self):
        return "CiscoParameter [name='"+str(self.name)+"', cardinalityMin="+str(self.cardinalityMin)+", cardinalityMax="+str(self.cardinalityMax)+", description='"+str(self.description)+"', typeParameter='"+str(self.typeParameter)+"', uid_genericParameter="+str(self.genericParameter)+", number_of_listOptionItem="+str(self.listOptionItemList.__len__())+"]"






class CiscoKeyword(AtomicTerm):
    def __init__(self, xmlNode, word=None):
        if xmlNode==None:
            self.word = word
        else:
            self.word = xmlNode.attributes['word'].value

        #from IOSReference import printLog
        #printLog("Created "+self.__str__())

    def __str__(self):
        return "CiscoKeyword [word="+str(self.word)+"]"






class TermOrTerm(AtomicTerm):
    def __init__(self, xmlNode):
        self.syntaxTermList = []

        if xmlNode!=None:
            #load syntax terms (separated by a "or")
            allSsyntaxTerm = xmlNode.getElementsByTagName('SyntaxTerm')
            for node in allSsyntaxTerm:
                syntaxTerm = SyntaxTerm(node)
                self.addSyntaxTerm(syntaxTerm)

        #from IOSReference import printLog
        #printLog("Created "+self.__str__())



    def addSyntaxTerm(self, syntaxTerm):
        if (isinstance(syntaxTerm, SyntaxTerm)):
            self.syntaxTermList.append(syntaxTerm)

    def __str__(self):
        return "TermOrTerm [number_of_syntax_terms="+str(self.syntaxTermList.__len__())+"]"