import copy
from Formula import Formula, Quantifier
from Conditions import Alias, Condition
from Terms import AtomicAliasTerm, AtomicConstantTerm
from xml.dom import minidom
from Device import Device

class CentralValidation(object):
    def __init__(self):
        self.device = None
        self.formula = None
        self.logicFormulaTrees = []
        self.CCDconditions = []


    def setDevice(self, device):
        self.devices = device

    def submitFormula(self, formula):
        if self.device!=None and isinstance(formula, Formula):
            self.formula = formula
            self.logicFormulaTrees = []
            self.CCDconditions = formula.get_cross_chain()
            
            
    def generateTreesWithCCD(self):
        if self.device==None or self.formula==None:
            return
        #TODO: generate trees from formula 
        

    def valuateTrees(self):
        if self.device==None or self.formula==None:
            return
        print "* CENTRAL VALIDATION : beginning valuating formula..."
        for logicFormulaTree in self.logicFormulaTrees:
            logicFormulaTree.valuate()
    
    def computeTrees(self):
        if self.device==None or self.formula==None:
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
        for condition in self.CCDconditions:
            condition.compute()
    
    def returnComputedTrees(self):
        return self.logicFormulaTrees


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
        #we use a temporary list for the 'foreach' because we will add another nodes to self.nodes
        tmpList = self.nodes[:]
        for node in tmpList:
            print "Valuating root node..."
            node.valuate(self, self.device)
            print node.getNbValuatedNodes()+" node(s) valuated."

    def compute(self):
        result = True
        for node in self.nodes:
            result &= node.compute()
        #TODO: compute cross chain interdependancies!!
        return result
    
    
    
def generateTestFormula1():
    print "Test Formula [fa x=a]([fa x=a,y=b;te z=c](y=2 && x=y))"
    
    #Alias x,y,z
    x = Alias("x", "a")
    y = Alias("y", "b")
    z = Alias("z", "c")
    
    #Quantifiers
    fa_x = Quantifier("fa", None, x)
    fa_y = Quantifier("fa", fa_x, y)
    te_z = Quantifier("te", fa_x, z)
    
    #Conditions
    c_y_2 = Condition("=", AtomicAliasTerm(y), AtomicConstantTerm(2))
    c_y_z = Condition("=", AtomicAliasTerm(y), AtomicAliasTerm(z))
    
    formula = Formula([x, y, z], [fa_x, fa_y, te_z], [c_y_2, c_y_z])
    print "Formula:\n", formula
    conditions = formula.get_cross_chain()
    print "Cross chain dependancies:", len(conditions)
    for c in conditions:
        print c
    
    return formula






if __name__ == '__main__':
    device = Device(minidom.parse('../TestFiles/Real_Example_Device.xml'))
    formula = generateTestFormula1()
    
    centralValidation = CentralValidation()
    centralValidation.setDevice(device)
    centralValidation.submitFormula(formula)
    centralValidation.generateTreesWithCCD()
    centralValidation.valuateTrees()
    centralValidation.computeTrees()
    centralValidation.computeCCD()
    
    outputTrees = centralValidation.returnComputedTrees()
