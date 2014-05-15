from xml.dom import minidom
from IOSRef import IOSReference
from Validation.Node import NeutralNode, ForAllNode
from Validation.Conditions import Condition, Alias
from Validation.Terms import AtomicAliasTerm
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


    print "\n**   Building validation tree for formula #2:    For all d=x : For all d=x, a=y : For all d=x, b=z : y<z \n"

    '''

  -----------  CENTRAL  ----------
                  |
                  o  (node1)   FORALL
                  |
                  |
                  |
                 d=x (node2)   FORALL   [cond. y<z]
                 /\
                /  \
               /    \
              /      \
      a=y (node3)    b=z (node4)


    '''


    #Central validation (main class)
    central = CentralValidation()
    central.addDevice(device1)
    central.addDevice(device2)

    #aliases x, y, z in the nodes
    aliasX = Alias("x")
    aliasY = Alias("y")
    aliasZ = Alias("z")

    uid_a = 101
    uid_b = 102
    uid_d = 1

    #condition y<z
    condition1 = Condition("<")
    condition1.setTerms(AtomicAliasTerm(aliasY), AtomicAliasTerm(aliasZ))

    #nodes
    node4 = NeutralNode(uid_b, [], [], aliasZ)     #neutral
    node3 = NeutralNode(uid_a, [], [], aliasY)     #neutral
    node2 = ForAllNode(uid_d, [node3, node4], [condition1], aliasX)     #condition y<z
    node1 = ForAllNode(0, [node2], [], None)           #no conditions and no aliases

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1]) #just one node at root
    central.submitFormula(logicFormulaTree)

    central.valuate()  #import values of parameters from the device META-CLI
    tmp = central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "** FINAL RESULT of computing for all devices : "+str(tmp)

    print "***           END              ***"



if __name__ == '__main__':
    main()
