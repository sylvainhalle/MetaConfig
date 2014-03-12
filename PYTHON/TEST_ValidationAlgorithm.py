'''
Created on 8 fevr. 2014

@author: Sylvain
Construction d'un arbre de validation en "dur"
'''

from xml.dom import minidom
from IOSRef import *
from Node import *
from Conditions import *
from Terms import *
from CentralValidation import *
from Device import *

def main():
    print "*** Building validation tree ***"
    print "For any d=x : For any d=x, a=y : y<=0"

    '''

  -----------  CENTRAL  ----------
                  |
                  o  (node1)
                  |
                  | for any
                  |
                 d=x (node2)
                  |
                  | for any
                  |
                 a=y (node3) [cond. y<=0]


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

    uid_a = 101
    uid_d = 1

    #condition y<=0
    condition1 = Condition("<=")
    condition1.setTerms(AtomicAliasTerm(aliasY), AtomicConstantTerm(0))

    #nodes
    node3 = Node(uid_a, [], [condition1], aliasY)     #neutral
    node2 = NodeAnd(uid_d, [node3], [], aliasX)     #no conditions
    node1 = NodeAnd(0, [node2], [], None)           #no conditions and no aliases

    #Formula tree
    logicFormulaTree = LogicFormulaTree([node1], []) #just one node at root and no interdependancies
    central.submitFormula(logicFormulaTree)

    print central
    central.valuate()  #import values of parameters from the device META-CLI
    print central.compute() #compute conditions of the validation tree thanks to the imported values. Return true if the logic formula is verified.

    print "***           END              ***"



if __name__ == '__main__':
    main()
