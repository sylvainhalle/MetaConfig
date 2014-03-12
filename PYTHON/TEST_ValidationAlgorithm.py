'''
Created on 8 fevr. 2014

@author: Sylvain
Construction d'un arbre de validation en "dur"
'''

from Node import *
from Conditions import *
from Terms import *
from CentralValidation import *
from Device import *

def main():
    print "*** Building validation tree ***"
    print "For any a=x : For any c=z : There exists a=x, b=y : x>y and y=z"

    '''

  ----------- CENTRAL ----------
  |                            |
  o  (node1)                   o  (node2)
  |                            |
  | for any                    | for any
  |                            |
 a=x (node3)                  c=z (node5)
  |
  | there exists                              [interdep: cond y=z]
  |
 b=y (node4) [cond. x>y]


    '''

    #IOS Reference (catalogue des commandes et parametres possibles pour un device)
    iosReference = IOSReference(minidom.parse('IOSRef_AlgoValidation.xml'))

    #Devices presents sur le reseau
    device1 = Device(minidom.parse('Device1_AlgoValidation.xml'), iosReference)
    device2 = Device(minidom.parse('Device2_AlgoValidation.xml'), iosReference)

    #Central validation (main class)
    central = CentralValidation()
    central.addDevice(device1)
    central.addDevice(device2)

    #alias x, y, z dans les noeuds
    aliasX = Alias("x")
    aliasY = Alias("y")
    aliasZ = Alias("z")

    uid_a = 1
    uid_b = 2
    uid_c = 3

    #condition x>y
    condition1 = Condition(">")
    condition1.setTerms(AtomicAliasTerm(aliasX), AtomicAliasTerm(aliasY))

    #condition y=z
    condition2 = Condition("=")
    condition2.setTerms(AtomicAliasTerm(aliasY), AtomicAliasTerm(aliasZ))

    #nodes
    node5 = Node(uid_c, [], [], aliasZ)             #neutral
    node4 = Node(uid_b, [], [condition1], aliasY)   #neutral
    node3 = NodeOr(uid_a, [node4], [], aliasX)
    node2 = NodeAnd(0, [node5], [], None)           #no conditions and no aliases
    node1 = NodeAnd(0, [node3], [], None)           #no conditions and no aliases

    #interdependancy between nodes 4 and 5
    interdep = Interdependancy([aliasY, aliasZ], [condition2])

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1, node2], [interdep])
    central.submitFormula(logicFormulaTree)

    print central
    central.valuate()  #import values of parameters from the device META-CLI
    print central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "***           END              ***"



if __name__ == '__main__':
    main()
