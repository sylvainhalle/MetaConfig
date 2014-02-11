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

    def __str__(self):
        return "Node: uid:" + self.uidParam

class NodeAnd(Node):
    def __init__(self, uid, childrens = [], conditions = [], alias = None):
        Node.__init__(self, uid, childrens, conditions, alias)

    def __str__(self):
        return "NodeAnd: uid:" + str(self.uidParam)

class NodeOr(Node):
    def __init__(self, uid, childrens, conditions = [], alias = None):
        Node.__init__(self, uid, childrens, conditions, alias)
    def __str__(self):
        return "NodeOr: uid:" + self.uidParam

class Alias(object):
    '''
    Identifiant de noeud pour l'arbre d'evaluation
    '''
    def __init__(self, name = ""):
        '''
        Constructeur
        '''
        self.name = name

    def __str__(self):
        return self.name

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
        return "Interdependancy entre:" + aliasNames

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

    def __str__(self):
        return "Condition: operateur:"+self.operateur+",terms:"+self.terms

class AbstractTerm(object):
    '''
    Terme abstrait
    '''
    def compute(self):
        print "Compute the node..."

class AtomicAliasTerm(AbstractTerm):
    '''
    Terme designant un alias
    '''
    def __init__(self, alias):
        self.alias = alias

    def __str__(self):
        return self.alias

class AtomicConstantTerm(AbstractTerm):
    '''
    Terme designant une constante
    '''
    def __init__(self, constant):
        self.constant = constant

    def __str__(self):
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

    def __str__(self):
        return "(" + self.operator + ":" + self.terms + ")"

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

    def __str__(self):
        affichage = "Central:\nNodes:"
        for node in self.nodes:
            affichage += node.__str__()+"\n"
        affichage +="\nInterdependance:\n"
        for interdependance in self.interdependancies:
            affichage += interdependance.__str__()+"\n"
        return affichage
