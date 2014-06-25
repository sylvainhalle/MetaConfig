from Terms import AtomicAliasTerm

class Formula(object):
    '''
    classdocs
    '''
    def __init__(self, aliasList = [], quantList = [], condList = []):
        '''
        Constructor
        '''
        self.aliasList = aliasList
        self.quantList = quantList
        self.condList = condList
        
    def get_cross_chain(self):
        cond = []
        for c in self.condList:
            if(self.is_cross_chain(c, self.quantList)):
                cond.append(c)
        return cond
    
    def is_cross_chain(self, condition, quantList):
        iterList = list(quantList)
        #Term1
        term1 = self.getAlias(condition.term1, iterList)
        #Term2
        term2 = self.getAlias(condition.term2, iterList)
        print "Term1:", term1, "Term2:", term2
        if(term1 == None or term2 == None):
            return False
        else:
            #Is term1 parent of term2 ?
            parent = term1
            while parent != None:
                if parent == term2:
                    return False
                parent = parent.parent_ref
            #Is term2 parent of term1 ?
            parent = term2
            while parent != None:
                if parent == term1:
                    return False
                parent = parent.parent_ref
            #else return True
            return True
    
    def getAlias(self, term, quantList):
        for q in quantList:
            if type(term) == AtomicAliasTerm:
                if(q.alias_ref == term.alias):
                    return q
        return None
    
    def __str__(self):
        ret_str = "Alias:["
        ret_str += ', '.join(map(str, self.aliasList))
        ret_str += "]\nQuantifier:["
        ret_str += ', '.join(map(str, self.quantList))
        ret_str += "]\nConditions:["
        ret_str += ', '.join(map(str, self.condList))
        return ret_str + "]"
        







class Quantifier(object):
    
    def __init__(self, quant_type, parent_ref, alias_ref):
        self.quant_type = quant_type
        self.parent_ref = parent_ref
        self.alias_ref = alias_ref
        
    def __str__(self):
        return str(self.quant_type) + ":" + str(self.alias_ref)



    