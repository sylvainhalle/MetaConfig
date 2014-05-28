from Device.Device import Device
from Device.DeviceCommand import DeviceCommand
from Device.DeviceParameter import DeviceParameter



COUNT_COMMANDS = True
NB_VALUATED_NODES = 0

class NeutralNode(object):
    '''
    Abstract node in the evaluation tree
    '''
    def __init__(self, uidParamOrCommand, childrens = [], conditions = [], alias = None, computedValue = None):
        '''
        Constructor
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
        if isinstance(self, ForAllNode):
            nodeCopy = ForAllNode(self.uidParamOrCommand, childsCopy, self.conditions, self.alias)
        elif isinstance(self, ExistsNode):
            nodeCopy = ExistsNode(self.uidParamOrCommand, childsCopy, self.conditions, self.alias)
        else:
            nodeCopy = NeutralNode(self.uidParamOrCommand, childsCopy, self.conditions, self.alias, self.computedValue)
        return nodeCopy


    def getNbValuatedNodes(self):
        return NB_VALUATED_NODES

    # parent is the parent NeutralNode of this node (useful for adding brothers to this node). It can also be the FormulaTree itself.
    # deviceNode can be the device itself (if we are at the level of the root) or a DeviceCommand
    # this fonction browses the elements under the deviceNode, looking for uids matching this 'uidParamOrCommand'
    def valuate(self, parent, deviceNode):

        if self.uidParamOrCommand==0:                           #if it's the root
            NB_VALUATED_NODES = 0
            tmpList = self.childs[:]                            #use a temporary list for the 'foreach' because we will add another nodes to self.childs
            for child in tmpList:
                child.valuate(self, deviceNode)                 #valuates subNodes (recursive calls)
            return

        deviceParametersAndCommandsList = []
        if (isinstance(deviceNode, Device)):
            deviceParametersAndCommandsList = deviceNode.deviceCommandList
        elif (isinstance(deviceNode, DeviceCommand)):
            deviceParametersAndCommandsList = deviceNode.deviceParametersAndCommandsList

        thisNodeUsed = False
        for devNode in deviceParametersAndCommandsList:

            paramOrCommandDeviceUID = -1
            if isinstance(devNode, DeviceCommand):
                paramOrCommandDeviceUID = devNode.ref_cmd
            if isinstance(devNode, DeviceParameter):
                paramOrCommandDeviceUID = devNode.ref_param

            #print "***VALUATE  START Loop :  self.uidParamOrCommand="+str(self.uidParamOrCommand)+"  paramOrCommandDeviceUID="+str(paramOrCommandDeviceUID)+"   LISTE="+str(deviceParametersAndCommandsList)

            if str(self.uidParamOrCommand)==str(paramOrCommandDeviceUID):
                #print "**VALUATE param or command found!   thisNodeUsed="+str(thisNodeUsed)
                if thisNodeUsed:
                    nodeCopy = self.copy()                                  #create a copy of this node
                    if isinstance(devNode, DeviceCommand):
                        nodeCopy.computedValue = None                       #it's a DeviceCommand, so there's no value on it
                        if COUNT_COMMANDS:
                            NB_VALUATED_NODES += 1
                    else:
                        nodeCopy.computedValue = devNode.values[0]          #it's a DeviceParameter, so we can valuate this node
                        NB_VALUATED_NODES += 1

                    #if nodeCopy.computedValue!=None:
                    #    print "***VALUATE  computedValue="+str(nodeCopy.computedValue)+" parent:"+str(parent)+" this:"+str(self)

                    if nodeCopy.computedValue!=None or (nodeCopy.childs!=None and nodeCopy.childs.__len__()>0):
                        tmpList = nodeCopy.childs[:]
                        for child in tmpList:
                            child.valuate(self, devNode)                       #valuates subNodes (recursive calls)
                        parent.addChild(nodeCopy)                           #if there's a value or childs in this node, we can keep this node in the formula tree
                else:
                    thisNodeUsed = True
                    if isinstance(devNode, DeviceCommand):
                        self.computedValue = None                           #it's a DeviceCommand, so there's no value on it
                        if COUNT_COMMANDS:
                            NB_VALUATED_NODES += 1
                    else:
                        self.computedValue = devNode.values[0]              #it's a DeviceParameter, so we can valuate this node
                        NB_VALUATED_NODES += 1

                    #if self.computedValue!=None:
                    #    print "***VALUATE  computedValue="+str(self.computedValue)+" parent:"+str(parent)+" this:"+str(self)

                    if self.computedValue==None and (self.childs==None or self.childs.__len__()==0):
                        parent.removeChild(self)                            #if no value and no childs, don't keep this node in the formula tree
                    else:
                        tmpList = self.childs[:]
                        for child in tmpList:
                            child.valuate(self, devNode)                       #valuates subNodes (recursive call)

    def compute(self):
        self.updateAlias()
        result = True
        for cond in self.conditions:      #We check all conditions bound to this node
            result &= cond.compute()      #conditions are separated by "and"
        return result

    def __str__(self):
        return "NeutralNode: uidParamOrCommand=" + str(self.uidParamOrCommand)





class ForAllNode(NeutralNode):
    def __init__(self, uidParamOrCommand, childrens = [], conditions = [], alias = None):
        NeutralNode.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        result = True
        for child in self.childs:
            result = child.compute() and result     #it's an "AND" node, so ALL childs must be verified

        if result:
            return NeutralNode.compute(self)     #If childrens are verified, we can verify conditions attached to this node
        else:
            return False

    def __str__(self):
        return "ForAllNode: uidParamOrCommand=" + str(self.uidParamOrCommand)




class ExistsNode(NeutralNode):
    def __init__(self, uidParamOrCommand, childrens, conditions = [], alias = None):
        NeutralNode.__init__(self, uidParamOrCommand, childrens, conditions, alias)

    def compute(self):
        result = False
        for child in self.childs:
            result = child.compute() or result     #it's an "OR" node, one child is enough to verify this node

        if result:
            return NeutralNode.compute(self)    #If childrens are verified, we can verify conditions attached to this node
        else:
            return False

    def __str__(self):
        return "ExistsNode: uidParamOrCommand=" + str(self.uidParamOrCommand)