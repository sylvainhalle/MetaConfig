class Alias(object):
    def __init__(self, name = "", uid = 0):
        self.name = name
        self.uid = uid
        self.currentValue = None

    def setValue(self, currentValue):
        self.currentValue = currentValue

    def getValue(self):
        if self.currentValue != None:
            return self.currentValue
        else:
            print "Warning: alias not defined : " + str(self)
            return 0

    def __str__(self):
        return str(self.name)







class Condition(object):
    def __init__(self, operator, term1 = None, term2 = None, isCrossChainDependency = False):
        self.operateur = operator
        self.term1 = term1
        self.term2 = term2
        self.nodesBound = []
        self.isCrossChainDependency = isCrossChainDependency

    def setTerms(self, term1, term2):
        self.term1 = term1
        self.term2 = term2
        
    def addNodeBoundToThisCondition(self, node):
        if not self.nodesBound.__contains__(node):
            self.nodesBound.append(node)

    def compute(self):
        #print "Evaluate", str(self)
        t1 = int(self.term1.compute())
        t2 = int(self.term2.compute())
        #print "*** Compute condition : "+str(t1)+" "+self.operateur+" "+str(t2)
        if self.operateur == "==":
            return t1 == t2
        elif self.operateur == "<":
            return t1 <  t2
        elif self.operateur == ">":
            return t1 >  t2
        elif self.operateur == "!=":
            return t1 != t2
        elif self.operateur == "<=":
            return t1 <= t2
        elif self.operateur == ">=":
            return t1 >= t2
        else:
            return False

    def __str__(self):
        return "Condition: operator="+str(self.operateur)+", terms= "+str(self.term1)+", "+str(self.term2)
