from xml.dom import minidom
from IOSRef import IOSReference
from Validation.Node import NeutralNode, ExistsNode
from Validation.Conditions import Condition, Alias
from Validation.Terms import AtomicAliasTerm, AtomicConstantTerm
from Validation.CentralValidation import CentralValidation, LogicFormulaTree
from Device import Device

def main():
    print "***           START              ***\n"

    #Loading IOS Reference (ALL commands and parameters available in a device, i.e. documentation)
    iosReference = IOSReference(minidom.parse('../TestFiles/IOSRef_AlgoValidation.xml'))

    #Loading devices connected to the network
    # USING Configuration #2 : 5 devices
    device1 = Device(minidom.parse('../TestFiles/DevicesConf1/Device1.xml'), iosReference)
    device2 = Device(minidom.parse('../TestFiles/DevicesConf1/Device2.xml'), iosReference)
    device3 = Device(minidom.parse('../TestFiles/DevicesConf2/Device3.xml'), iosReference)
    device4 = Device(minidom.parse('../TestFiles/DevicesConf2/Device4.xml'), iosReference)
    device5 = Device(minidom.parse('../TestFiles/DevicesConf2/Device5.xml'), iosReference)


    print "\n**   Building validation tree for formula #3:    Exists d=x : Exists d=x, a=y : Exists d=x, b=z : y=0 ^ z=3 \n"

    '''

  -----------  CENTRAL  ----------
                  |
                  o  (node1)   EXISTS
                  |
                  |
                  |
                 d=x (node2)   EXISTS
                 /\
                /  \
               /    \
              /      \
      a=y (node3)    b=z (node4)
     [cond. y=0]      [cond. z=3]

    '''


    #Central validation (main class)
    central = CentralValidation()
    central.addDevice(device1)
    central.addDevice(device2)
    central.addDevice(device3)
    central.addDevice(device4)
    central.addDevice(device5)

    #aliases x, y, z in the nodes
    aliasX = Alias("x")
    aliasY = Alias("y")
    aliasZ = Alias("z")

    uid_a = 101
    uid_b = 102
    uid_d = 1

    #condition y=0
    condition1 = Condition("==")
    condition1.setTerms(AtomicAliasTerm(aliasY), AtomicConstantTerm(0))
    #condition z=3
    condition2 = Condition("==")
    condition2.setTerms(AtomicAliasTerm(aliasZ), AtomicConstantTerm(3))


    #nodes
    node4 = NeutralNode(uid_b, [], [condition2], aliasZ)
    node3 = NeutralNode(uid_a, [], [condition1], aliasY)
    node2 = ExistsNode(uid_d, [node3, node4], [], aliasX)
    node1 = ExistsNode(0, [node2], [], None)

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1]) #just one node at root
    central.submitFormula(logicFormulaTree)

    central.valuate()  #import values of parameters from the device META-CLI
    tmp = central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "** FINAL RESULT of computing for all devices : "+str(tmp)

    print "***           END              ***"



if __name__ == '__main__':
    main()
