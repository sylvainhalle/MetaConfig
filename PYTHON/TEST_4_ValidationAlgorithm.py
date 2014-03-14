'''
Created on 8 fevr. 2014

@author: Sylvain STOESEL & Clement PARISOT
Building a validation tree - Formula test #4
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


    print "\n**   Building validation tree for formula #4:    Exists d=x : Exists d=x, a=y : For all e=w : For all e=w, c=z : y=-1 ^ z=3 \n"

    '''

  -----------  CENTRAL  ----------
                 /\
                /  \
               /    \
              /      \
             /        \
            /          \
           /            \
          /              \
         o EXISTS         o FORALL
         | (node1)        | (node2)
         |                |
         |                |
         |                |
        d=x EXISTS       e=w FORALL
         | (node3)        | (node4)
         |                |
         |                |
         |                |
        a=y (node5)      c=z (node6)
         [cond. y=-1]     [cond. z=3]

    '''


    #Central validation (main class)
    central = CentralValidation()
    central.addDevice(device1)
    central.addDevice(device2)

    #aliases w, x, y, z in the nodes
    aliasW = Alias("w")
    aliasX = Alias("x")
    aliasY = Alias("y")
    aliasZ = Alias("z")

    uid_a = 101
    uid_c = 103
    uid_d = 1
    uid_e = 2

    #condition y=-1
    condition1 = Condition("==")
    condition1.setTerms(AtomicAliasTerm(aliasY), AtomicConstantTerm(-1))
    #condition z=3
    condition2 = Condition("==")
    condition2.setTerms(AtomicAliasTerm(aliasZ), AtomicConstantTerm(3))

    #nodes
    node6 = Node(uid_c, [], [condition2], aliasZ)
    node5 = Node(uid_a, [], [condition1], aliasY)
    node4 = NodeAnd(uid_e, [node6], [], aliasW)
    node3 = NodeOr(uid_d, [node5], [], aliasX)
    node2 = NodeAnd(0, [node4], [], None)
    node1 = NodeOr(0, [node3], [], None)

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1, node2]) #two nodes at root
    central.submitFormula(logicFormulaTree)

    central.valuate()  #import values of parameters from the device META-CLI
    tmp = central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "** FINAL RESULT of computing for all devices : "+str(tmp)

    print "***           END              ***"



if __name__ == '__main__':
    main()
