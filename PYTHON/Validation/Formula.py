'''
Created on 20 mai 2014

@author: Clement
'''

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
    
    def __str__(self):
        ret_str = "Alias:["
        ret_str += ', '.join(map(str, self.aliasList))
        ret_str += "]\nQuantifier:["
        ret_str += ', '.join(map(str, self.quantList))
        ret_str += "]\nConditions:["
        ret_str += ', '.join(map(str, self.condList))
        return ret_str + "]"

class Alias(object):
    
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
        
    def __str__(self):
        return self.name
        
class Quantifier(object):
    
    def __init__(self, quant_type, parent_ref, alias_ref):
        self.quant_type = quant_type
        self.parent_ref = parent_ref
        self.alias_ref = alias_ref
        
    def __str__(self):
        return str(self.quant_type) + ":" + str(self.alias_ref)
    
class Condition(object):
    
    def __init__(self, term1_alias, operator, term2_alias):
        self.operator = operator
        self.term1 = term1_alias
        self.term2 = term2_alias
    
    def __str__(self):
        return str(self.term1) + str(self.operator) + str(self.term2)

class AtomicAliasTerm(object):
    
    def __init__(self, alias_ref):
        self.alias_ref = alias_ref
        
    def __str__(self):
        return str(self.alias_ref)
    
class AtomicConstantTerm(object):
    
    def __init__(self, constant):
        self.constant = constant
        
    def __str__(self):
        return str(self.constant)

if __name__ == '__main__':
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
    c_y_2 = Condition(AtomicAliasTerm(y), "=", AtomicConstantTerm(2))
    c_y_z = Condition(AtomicAliasTerm(y), "=", AtomicAliasTerm(z))
    
    formula = Formula([x, y, z], [fa_x, fa_y, te_z], [c_y_2, c_y_z])
    print "Formula:\n", formula
    