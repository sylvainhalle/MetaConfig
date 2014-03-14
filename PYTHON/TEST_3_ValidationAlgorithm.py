'''
Created on 8 fevr. 2014

@author: Sylvain STOESEL & Clement PARISOT
Building a validation tree - Formula test #3
'''

from xml.dom import minidom
from IOSRef import *
from Node import *
from Conditions import *
from Terms import *
from CentralValidation import *
from Device import *

def main():
    print "***           START              ***\n"

    #Loading IOS Reference (ALL commands and parameters available in a device, i.e. documentation)
    iosReference = IOSReference(minidom.parse('IOSRef_AlgoValidation.xml'))

    #Loading devices connected to the network
    device1 = Device(minidom.parse('Device1_AlgoValidation.xml'), iosReference)
    device2 = Device(minidom.parse('Device2_AlgoValidation.xml'), iosReference)


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
    node4 = Node(uid_b, [], [condition2], aliasZ)
    node3 = Node(uid_a, [], [condition1], aliasY)
    node2 = NodeOr(uid_d, [node3, node4], [], aliasX)
    node1 = NodeOr(0, [node2], [], None)

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1]) #just one node at root
    central.submitFormula(logicFormulaTree)

    central.valuate()  #import values of parameters from the device META-CLI
    tmp = central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "** FINAL RESULT of computing for all devices : "+str(tmp)

    print "***           END              ***"



if __name__ == '__main__':
    main()
