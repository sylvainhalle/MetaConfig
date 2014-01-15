#-------------------------------------------------------------------------------
# Name:        AtomicTerm
# Classes:     SyntaxTerm, AtomicTerm, CiscoParameter, CiscoKeyword, TermOrTerm, ListOptionItem
# Purpose:     IOSReference
#
# Author:      Sylvain
#
# Created:     09/12/2013
# Copyright:   (c) Sylvain 2013
# Licence:     UQAC
#-------------------------------------------------------------------------------

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

        from IOSReference import printLog
        printLog("Created "+self.toString())

    def addAtomicTerm(self, atomicTerm):
        if (isinstance(atomicTerm, AtomicTerm)):
            self.atomicTermList.append(atomicTerm)

    def toString(self):
        return "SyntaxTerm [cardinalityMin="+str(self.cardinalityMin)+", cardinalityMax="+str(self.cardinalityMax)+", number_of_atomic_terms="+str(self.atomicTermList.__len__())+"]"



class ListOptionItem:
    def __init__(self, xmlNode, value=None):
        self.value = value



class CiscoParameter(AtomicTerm):
    def __init__(self, xmlNode, name=None, cardinalityMin=None, cardinalityMax=None, description=None, typeParameter=None, genericParameter=None):
        self.name = name
        self.cardinalityMin = cardinalityMin
        self.cardinalityMax = cardinalityMax
        self.description = description
        self.typeParameter = typeParameter
        self.genericParameter = genericParameter
        self.listOptionItemList = []

    def addListOptionItem(self, listOptionItem):
        if (isinstance(listOptionItem, ListOptionItem)):
            self.listOptionItemList.append(listOptionItem)




class CiscoKeyword(AtomicTerm):
    def __init__(self, xmlNode, word=None):
        self.word = word




class TermOrTerm(AtomicTerm):
    def __init__(self, xmlNode):
        self.syntaxTermList = []

    def addSyntaxTerm(self, syntaxTerm):
        if (isinstance(syntaxTerm, SyntaxTerm)):
            self.syntaxTermList.append(syntaxTerm)