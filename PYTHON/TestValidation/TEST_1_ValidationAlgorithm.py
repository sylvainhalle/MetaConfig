from xml.dom import minidom
from IOSRef import IOSReference
from Validation.Node import NeutralNode, ForAllNode
from Validation.Conditions import Condition, Alias
from Validation.Terms import AtomicAliasTerm, AtomicConstantTerm
from Validation.CentralValidation import CentralValidation, LogicFormulaTree
from Device import Device


def main():
    print "***           START              ***\n"

    #Loading IOS Reference (ALL commands and parameters available in a device, i.e. documentation)
    iosReference = IOSReference(minidom.parse('../TestFiles/IOSRef_AlgoValidation.xml'))

    #Loading devices connected to the network
    # USING Configuration #1 : 2 devices
    device1 = Device(minidom.parse('../TestFiles/DevicesConf1/Device1.xml'), iosReference)
    device2 = Device(minidom.parse('../TestFiles/DevicesConf1/Device2.xml'), iosReference)


    print "\n**   Building validation tree for formula #1:    For all d=x : For all d=x, a=y : y<=0 \n"

    '''

  -----------  CENTRAL  ----------
                  |
                  o  (node1)     FORALL
                  |
                  |
                  |
                 d=x (node2)     FORALL
                  |
                  |
                  |
                 a=y (node3) [cond. y<=0]


    '''


    #Central validation (main class)
    central = CentralValidation()
    central.addDevice(device1)
    central.addDevice(device2)

    #aliases x and y in the nodes
    aliasX = Alias("x")
    aliasY = Alias("y")

    uid_a = 101
    uid_d = 1

    #condition y<=0
    condition1 = Condition("<=")
    condition1.setTerms(AtomicAliasTerm(aliasY), AtomicConstantTerm(0))

    #nodes
    node3 = NeutralNode(uid_a, [], [condition1], aliasY)     #neutral, with condition y<=0
    node2 = ForAllNode(uid_d, [node3], [], aliasX)     #no conditions
    node1 = ForAllNode(0, [node2], [], None)           #no conditions and no aliases

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1])    #just one node at root
    central.submitFormula(logicFormulaTree)

    central.valuate()  #import values of parameters from the device META-CLI
    tmp = central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "** FINAL RESULT of computing for all devices : "+str(tmp)

    print "***           END              ***"



if __name__ == '__main__':
    main()
