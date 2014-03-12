#-------------------------------------------------------------------------------
# Name:        Terms
# Purpose:
#
# Author:      Sylvain
#
# Created:     26/02/2014
# Copyright:   (c) Sylvain 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class AbstractTerm(object):
    '''
    Abstract Term
    '''
    def compute(self):
        #print "Compute the node..."
        return 0



class AtomicAliasTerm(AbstractTerm):
    '''
    Term corresponding to an alias (i.e. temporary variable like x, y, z...)
    '''
    def __init__(self, alias):
        self.alias = alias

    def __str__(self):
        return str(self.alias)

    def compute(self):
        #print "Compute the node "+ str(self.alias)
        return self.alias.getValue()



class AtomicConstantTerm(AbstractTerm):
    '''
    Term corresponding to a constant value (0, 1, ...)
    '''
    def __init__(self, constant):
        self.constant = constant

    def __str__(self):
        return str(self.constant)

    def compute(self):
        return self.constant

class Term(AbstractTerm):
    '''
    Term
    '''
    def __init__(self, operator, term1 = None, term2 = None):
        self.operator = operator
        self.term1 = term1
        self.term2 = term2

    def setTerms(self, term1, term2):
        self.term1 = term1
        self.term2 = term2

    def compute(self):
        #print "Evaluate", str(self)
        if self.operateur == "+":
            return int(self.term1.compute()) + int(self.term2.compute())
        elif self.operateur == "-":
            return int(self.term1.compute()) - int(self.term2.compute())
        elif self.operateur == "*":
            return int(self.term1.compute()) * int(self.term2.compute())
        elif self.operateur == "/":
            return int(self.term1.compute()) / int(self.term2.compute())
        else:
            return False

    def __str__(self):
        return "(" + str(self.operator) + ":" + str(self.term1) + ","+ str(self.term2) + ")"