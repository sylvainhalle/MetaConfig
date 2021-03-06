'''
Created on 8 fevr. 2014

@author: Clement
'''
import copy

class Node(object):
    '''
    Node abstrait de l'arbre d'evaluation
    '''
    def __init__(self, uidParamOrCommand, childrens = [], conditions = [], alias = None, computedValue = None):
        '''
        Constructeur
        '''
        self.uidParamOrCommand = uidParamOrCommand
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

    # parent is the parent Node of this node (useful for adding brothers to this node)
    # deviceNode can be the device itself (if we are at the level of the root) or a DeviceCommand, or a DeviceParameter
    # this fonction browses the elements under the deviceNode, looking for uids matching this 'uidParamOrCommand'
    def valuate(self, parent, deviceNode):
        if (isinstance(deviceNode, Device)):
            None
        elif (isinstance(deviceNode, DeviceCommand)):
            None
        elif (isinstance(deviceNode, DeviceParameter)):
            None

    def __str__(self):
        return "Node: uidParamOrCommand:" + str(self.uidParamOrCommand)

class NodeAnd(Node):
    def __init__(self, uidParamOrCommand, childrens = [], conditions = [], alias = None):
        Node.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        Node.updateAlias(self)
        result = True
        for cond in self.conditions:      #On commence par verifier l'ensemble des conditions liees a ce noeud
            print cond
            result &= cond.compute()      #les conditions sont toujours separees par des 'et'
        if result:                        #Si les conditions sont verifiees, on peut passer a la verification des enfants
            for child in self.childs:
                result &= child.compute() #C'est un noeud 'et' (pour tout) donc c'est TOUS les enfants qui doivent etre vrais
        return result

    def __str__(self):
        return "NodeAnd: uidParamOrCommand:" + str(self.uidParamOrCommand)

class NodeOr(Node):
    def __init__(self, uidParamOrCommand, childrens, conditions = [], alias = None):
        Node.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        Node.updateAlias(self)
        result = True
        for cond in self.conditions:      #On commence par verifier l'ensemble des conditions liees a ce noeud
            print cond
            result &= cond.compute()      #les conditions sont toujours separees par des 'et'
        if result:                        #Si les conditions sont verifiees, on peut passer a la verification des enfants
            result = False
            for child in self.childs:
                result |= child.compute() #C'est un noeud 'ou' (il existe) donc il suffit d'un enfant verifie pour que le resultat le soit
        return result

    def __str__(self):
        return "NodeOr: uidParamOrCommand:" + str(self.uidParamOrCommand)

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

class LogicFormulaTree(object):

    def __init__(self, central, nodes = [], device):
        self.central = central
        self.nodes = []
        for node in nodes:
            self.nodes.append(node)
        self.device = device

    def valuate(self):
        print "Valuation de l'arbre"
        #TODO: valuer l'arbre avec les valeurs des parametres du device

    def getCopy(self):
        #TODO: Return copy of the tree
        return copy.deepcopy(self)

    def compute(self):
        self.node.compute()