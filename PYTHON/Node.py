'''
Created on 8 fevr. 2014

@author: Clement
'''
from Device import *
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

    def removeChild(self, child):
        self.childs.remove(child)

    def addCondition(self, condition):
        self.conditions.append(condition)

    def setAlias(self, alias):
        self.alias = alias

    def updateAlias(self):
        if self.alias!=None:
            self.alias.setValue(self.computedValue)

    def copy(self):
        childsCopy = []
        for child in self.childs:
            childsCopy.append(child.copy())
        nodeCopy = Node(self.uidParamOrCommand, childsCopy, self.conditions, self.alias, self.computedValue)
        return nodeCopy

    # parent is the parent Node of this node (useful for adding brothers to this node). It can also be the FormulaTree itself.
    # deviceNode can be the device itself (if we are at the level of the root) or a DeviceCommand
    # this fonction browses the elements under the deviceNode, looking for uids matching this 'uidParamOrCommand'
    def valuate(self, parent, deviceNode):
        deviceParametersAndCommandsList = []
        if (isinstance(deviceNode, Device)):
            deviceParametersAndCommandsList = deviceNode.deviceCommandList
        elif (isinstance(deviceNode, DeviceCommand)):
            deviceParametersAndCommandsList = deviceNode.deviceParametersAndCommandsList

        thisNodeUsed = False
        for node in deviceParametersAndCommandsList:
            print "**VALUATE  debut boucle self.uidParamOrCommand="+str(self.uidParamOrCommand)+"    LISTE="+str(deviceParametersAndCommandsList)
            if isinstance(node, DeviceCommand):
                print "**VALUATE   node.ref_cmd="+str(node.ref_cmd)
            if isinstance(node, DeviceParameter):
                print "**VALUATE   node.ref_param="+str(node.ref_param)

            if (self.uidParamOrCommand==0 or isinstance(node, DeviceCommand) and (node.ref_cmd==self.uidParamOrCommand)) or (isinstance(node, DeviceParameter) and (node.ref_param==self.uidParamOrCommand)):
                print "**VALUATE param ou commande trouvee   thisNodeUsed="+str(thisNodeUsed)
                if thisNodeUsed:
                    nodeCopy = self.copy()                                  #create a copy of this node
                    if isinstance(node, DeviceCommand):
                        nodeCopy.computedValue = None                       #it's a DeviceCommand, so there's no value on it
                    else:
                        print "**VALUATE  node.values recupere : "+str(node.values)
                        nodeCopy.computedValue = node.values                #it's a DeviceParameter, so we can valuate this node

                    if nodeCopy.computedValue!=None or (nodeCopy.childs!=None and nodeCopy.childs.__len__()>0):
                        for child in nodeCopy.childs:
                            child.valuate(self, node)                       #valuates subNodes (recursive call)
                        parent.addChild(nodeCopy)                           #if there's a value or childs in this node, we can keep this node in the formula tree
                else:
                    thisNodeUsed = True
                    if isinstance(node, DeviceCommand):
                        self.computedValue = None                           #it's a DeviceCommand, so there's no value on it
                    else:
                        print "**VALUATE NOT USED  node.values recupere : "+str(node.values)
                        self.computedValue = node.values                #it's a DeviceParameter, so we can valuate this node

                    if self.computedValue==None and (self.childs==None or self.childs.__len__()==0):
                        parent.removeChild(self)                            #if no value and no childs, don't keep this node in the formula tree
                    else:
                        for child in self.childs:
                            child.valuate(self, node)                       #valuates subNodes (recursive call)

    def compute(self):
        self.updateAlias()
        result = True
        for cond in self.conditions:      #We check all conditions bound to this node
            print cond
            result &= cond.compute()      #conditions are separated by "and"
        return result

    def __str__(self):
        return "Node: uidParamOrCommand:" + str(self.uidParamOrCommand)

class NodeAnd(Node):
    def __init__(self, uidParamOrCommand, childrens = [], conditions = [], alias = None):
        Node.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        if Node.compute(self):                #If conditions are verified, we can verify childrens
            result = True
            for child in self.childs:
                result &= child.compute()     #it's an "AND" node, so ALL childs must be verified
            return result
        else:
            return false

    def __str__(self):
        return "NodeAnd: uidParamOrCommand:" + str(self.uidParamOrCommand)

class NodeOr(Node):
    def __init__(self, uidParamOrCommand, childrens, conditions = [], alias = None):
        Node.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        if Node.compute(self):                #If conditions are verified, we can verify childrens
            result = False
            for child in self.childs:
                result |= child.compute()     #it's an "OR" node
            return result
        else:
            return false

    def __str__(self):
        return "NodeOr: uidParamOrCommand:" + str(self.uidParamOrCommand)