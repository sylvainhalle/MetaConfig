#-------------------------------------------------------------------------------
# Name:        Conditions
# Purpose:
#
# Author:      Sylvain
#
# Created:     26/02/2014
# Copyright:   (c) Sylvain 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
