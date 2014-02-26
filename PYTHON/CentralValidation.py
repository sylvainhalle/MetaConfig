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

class CentralValidation(object):
    '''
    Central de validation des regles
    '''
    def __init__(self, interdependancies = [], logicFormulaTrees = []):
        self.interdependancies = []
        for interdependance in interdependancies:
            self.interdependancies.append(interdependance)
        self.logicFormulaTrees = []
        for logicFormulaTree in logicFormulaTrees:
            self.addFormulaTree(logicFormulaTree)

    def addFormulaTree(self, formulaTree):
        self.logicFormulaTrees.append(formulaTree)
        formulaTree.setCentral(self)

    def addInterdependancy(self, interdependancy):
        self.interdependancies.append(interdependancy)

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
        affichage +="\nInterdependance:\n"
        for interdependance in self.interdependancies:
            affichage += str(interdependance)+"\n"
        return affichage




class LogicFormulaTree(object):
    def __init__(self, device, nodes = []):
        self.central = None
        self.nodes = []
        for node in nodes:
            self.addChild(node)
        self.device = device

    def setCentral(self, central):
        self.central = central

    def getCopy(self):
        #TODO: Return copy of the tree
        return copy.deepcopy(self)

    def addChild(self, node):
        self.nodes.append(node)

    def valuate(self):
        for node in self.nodes:
            node.valuate(self, self.device)

    def compute(self):
        result = True
        for node in self.nodes:
            result &= node.compute()
        return result