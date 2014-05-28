import copy



class CentralValidation(object):
    def __init__(self):
        self.device = None
        self.logicFormula = None
        self.logicFormulaTrees = []
        self.CCDconditions = []


    def setDevice(self, device):
        self.devices = device

    def submitFormula(self, logicFormula):
        #TODO : classes LogicFormul, Quantifier
        if self.device!=None:  # and isinstance(logicFormula, LogicFormula):
            self.logicFormulaTrees = []
            self.CCDconditions = []
            self.logicFormula = logicFormula
            
    def generateTreesWithCCD(self):
        if self.device==None or self.logicFormula==None:
            return
        #TODO: generate trees from formula + find all cross-chain dependencies (CCD) 
        '''formulaTree.setCentral(self)
            formulaTree.setDevice(self.devices[0])
            self.logicFormulaTrees.append(formulaTree)
            #copy n times the formula, where n = number of devices - 1
            for i in range(1, self.devices.__len__()):
                formulaTreeCopy = formulaTree.getCopy()
                formulaTreeCopy.setCentral(self)
                formulaTreeCopy.setDevice(self.devices[i])
                self.logicFormulaTrees.append(formulaTreeCopy)'''

    def valuateTrees(self):
        if self.device==None or self.logicFormula==None:
            return
        print "* CENTRAL VALIDATION : beginning valuating formula..."
        for logicFormulaTree in self.logicFormulaTrees:
            logicFormulaTree.valuate()
    
    def computeTrees(self):
        if self.device==None or self.logicFormula==None:
            return
        print "* CENTRAL VALIDATION : beginning computing formula..."
        result = True
        for logicFormulaTree in self.logicFormulaTrees:
            tmp = logicFormulaTree.compute()
            print "* CENTRAL VALIDATION : computing result for device '"+logicFormulaTree.device.name+"' : "+str(tmp)
            result &= tmp
        return result
    
    def computeCCD(self):
        if self.device==None or self.logicFormula==None:
            return
        #TODO : compute CCD conditions
        pass
    
    def returnComputedTrees(self):
        return self.CCDconditions



    def __str__(self):
        affichage = "Central:\nFormulaTrees:\n"
        for logicFormulaTree in self.logicFormulaTrees:
            affichage += str(logicFormulaTree) +"\n"
        affichage = "CCD Conditions:\n"
        for ccdcond in self.CCDconditions:
            affichage += str(ccdcond) +"\n"
        return affichage




class LogicFormulaTree(object):
    def __init__(self, nodes = []):
        self.central = None
        self.nodes = []
        for node in nodes:
            self.nodes.append(node)
        self.device = None

    def setCentral(self, central):
        self.central = central

    def setDevice(self, device):
        self.device = device

    def getCopy(self):
        #TODO: Return a custom copy of the tree, do not use "deepcopy" !
        return copy.deepcopy(self)


    def addChild(self, node):
        self.nodes.append(node)

    def valuate(self):
        #use a temporary list for the 'foreach' because we will add another nodes to self.nodes
        tmpList = self.nodes[:]
        for node in tmpList:
            print "Valuating root node..."
            node.valuate(self, self.device)
            print node.getNbValuatedNodes()+" node(s) valuated."

    def compute(self):
        result = True
        for node in self.nodes:
            result &= node.compute()
        #TODO: compute interdependancies!!
        return result