#-------------------------------------------------------------------------------
# Name:        CentralValidation
# Purpose:
#
# Author:      Sylvain
#
# Created:     26/02/2014
# Copyright:   (c) Sylvain 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import copy


class CentralValidation(object):
    '''
    Central de validation des regles
    '''
    def __init__(self):
        self.devices = []
        self.logicFormulaTrees = []

    def addDevice(self, device):
        self.devices.append(device)

    def submitFormula(self, formulaTree):
        if (self.devices.__len__()>0):
            self.logicFormulaTrees = []
            formulaTree.setCentral(self)
            formulaTree.setDevice(self.devices[0])
            self.logicFormulaTrees.append(formulaTree)
            #copy n times the formula, where n = number of devices - 1
            for i in range(1, self.devices.__len__()):
                formulaTreeCopy = formulaTree.getCopy()
                formulaTreeCopy.setCentral(self)
                formulaTreeCopy.setDevice(self.devices[i])
                self.logicFormulaTrees.append(formulaTreeCopy)

    def compute(self):
        result = True
        for logicFormulaTree in self.logicFormulaTrees:
            result &= logicFormulaTree.compute()
        return result

    def valuate(self):
        for logicFormulaTree in self.logicFormulaTrees:
            logicFormulaTree.valuate()

    def __str__(self):
        affichage = "Central:\nFormulaTrees:\n"
        for logicFormulaTree in self.logicFormulaTrees:
            affichage += str(logicFormulaTree) +"\n"
        affichage +="\nDevices:\n"
        for device in self.devices:
            affichage += str(device)+"\n"
        return affichage




class LogicFormulaTree(object):
    def __init__(self, nodes = [], interdependancies = []):
        self.central = None
        self.nodes = []
        for node in nodes:
            self.addChild(node)
        self.interdependancies = []
        for interdep in interdependancies:
            self.interdependancies.append(interdep)
        self.device = None

    def setCentral(self, central):
        self.central = central

    def setDevice(self, device):
        self.device = device

    def getCopy(self):
        #TODO: Return a custom copy of the tree, do not use "deepcopy" !
        return copy.deepcopy(self)

    def addInterdependancy(self, interdependancy):
        self.interdependancies.append(interdependancy)

    def addChild(self, node):
        self.nodes.append(node)

    def valuate(self):
        for node in self.nodes:
            node.valuate(self, self.device)

    def compute(self):
        result = True
        for node in self.nodes:
            result &= node.compute()
        #TODO: compute interdependancies!!
        return result