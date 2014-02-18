'''
Created on 8 fevr. 2014

@author: Clement
'''

class Node(object):
    '''
    Node abstrait de l'arbre d'evaluation
    '''
    def __init__(self, uid, childrens = [], conditions = [], alias = None, computedValue = None):
        '''
        Constructeur
        '''
        self.uidParam = uid
        self.childs = []
        for child in childrens:
            self.childs.append(child)
        self.conditions = []
        for condition in conditions:
            self.conditions.append(condition)
        self.alias = alias
        self.computedValue = computedValue

    def addChild(self, child):
        self.childs.append(child)

    def addCondition(self, condition):
        self.conditions.append(condition)

    def setAlias(self, alias):
        self.alias = alias
    
    def updateAlias(self):
        self.alias.setValue(self.computedValue)

    def __str__(self):
        return "Node: uid:" + str(self.uidParam)

class NodeAnd(Node):
    def __init__(self, uid, childrens = [], conditions = [], alias = None):
        Node.__init__(self, uid, childrens, conditions, alias)
    
    def compute(self):
        Node.updateAlias(self)
        result = True
        for cond in self.conditions:
            print cond
            result &= cond.compute()
        return result

    def __str__(self):
        return "NodeAnd: uid:" + str(self.uidParam)

class NodeOr(Node):
    def __init__(self, uid, childrens, conditions = [], alias = None):
        Node.__init__(self, uid, childrens, conditions, alias)
        
    def compute(self):
        Node.updateAlias(self)
        result = False
        for cond in self.conditions:
            result |= cond.compute()
        return result

    def __str__(self):
        return "NodeOr: uid:" + str(self.uidParam)

class Alias(object):
    '''
    Identifiant de noeud pour l'arbre d'evaluation
    '''
    def __init__(self, name = ""):
        '''
        Constructeur
        '''
        self.name = name
        self.currentValue = None
    
    def setValue(self, currentValue):
        self.currentValue = currentValue
    
    def getValue(self):
        if self.currentValue != None:
            return self.currentValue
        else:
            print "Erreur valeur alias non definie:" + str(self)
            return 0

    def __str__(self):
        return str(self.name)

class Interdependancy(object):
    '''
    Lie plusieurs alias interdependants
    '''
    def __init__(self, aliasList = [], conditions = []):
        self.aliasList = []
        for alias in aliasList:
            self.aliasList.append(alias)
        self.conditions = []
        for condition in conditions:
            self.conditions.append(condition)

    def __str__(self):
        aliasNames = ""
        for alias in self.aliasList:
            aliasNames += " " + alias.name
        return "Interdependancy entre:" + str(aliasNames)

class Condition(object):
    '''
    Condition reliant 2 termes
    '''
    def __init__(self, operator, term1 = None, term2 = None):
        self.operateur = operator
        self.term1 = term1
        self.term2 = term2

    def setTerms(self, term1, term2):
        self.term1 = term1
        self.term2 = term2
    
    def compute(self):
        print "Evaluate", str(self)
        if self.operateur == "==":
            return self.term1.compute() == self.term2.compute()
        elif self.operateur == "<":
            return self.term1.compute() < self.term2.compute()
        elif self.operateur == ">":
            return self.term1.compute() > self.term2.compute()
        elif self.operateur == "!=":
            return self.term1.compute() != self.term2.compute()
        elif self.operateur == "<=":
            return self.term1.compute() <= self.term2.compute()
        elif self.operateur == ">=":
            return self.term1.compute() >= self.term2.compute()
        else:
            return False

    def __str__(self):
        return "Condition: operateur:"+str(self.operateur)+",terms:"+str(self.term1)+","+str(self.term2)

class AbstractTerm(object):
    '''
    Terme abstrait
    '''
    def compute(self):
        print "Compute the node..."
        return 0

class AtomicAliasTerm(AbstractTerm):
    '''
    Terme designant un alias
    '''
    def __init__(self, alias):
        self.alias = alias

    def __str__(self):
        return str(self.alias)
    
    def compute(self):
        print "Compute the node "+ str(self.alias)
        return self.alias.getValue()

class AtomicConstantTerm(AbstractTerm):
    '''
    Terme designant une constante
    '''
    def __init__(self, constant):
        self.constant = constant

    def __str__(self):
        return str(self.constant)
    
    def compute(self):
        return self.constant

class Term(AbstractTerm):
    '''
    Terme
    '''
    def __init__(self, operator, term1 = None, term2 = None):
        self.operator = operator
        self.term1 = term1
        self.term2 = term2

    def setTerms(self, term1, term2):
        self.term1 = term1
        self.term2 = term2
    
    def compute(self):
        print "Evaluate", str(self)
        if self.operateur == "+":
            return self.term1.compute() + self.term2.compute()
        elif self.operateur == "-":
            return self.term1.compute() - self.term2.compute()
        elif self.operateur == "*":
            return self.term1.compute() * self.term2.compute()
        elif self.operateur == "/":
            return self.term1.compute() / self.term2.compute()
        else:
            return False    

    def __str__(self):
        return "(" + str(self.operator) + ":" + str(self.term1) + ","+ str(self.term2) + ")"

class CentralValidation(object):
    '''
    Central de validation des regles
    '''
    def __init__(self, interdependancies = [], nodes = []):
        self.interdependancies = []
        for interdependance in interdependancies:
            self.interdependancies.append(interdependance)
        self.nodes = []
        for node in nodes:
            self.nodes.append(node)

    def addNode(self, node):
        self.nodes.append(node)

    def addInterdependancy(self, interdependancy):
        self.interdependancies.append(interdependancy)
        
    def compute(self):
        result = True
        for node in self.nodes:
            result &= node.compute()
        return result

    def __str__(self):
        affichage = "Central:\nNodes:"
        for node in self.nodes:
            affichage += str(node) +"\n"
        affichage +="\nInterdependance:\n"
        for interdependance in self.interdependancies:
            affichage += str(interdependance)+"\n"
        return affichage
