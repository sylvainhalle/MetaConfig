'''
Created on 8 fevr. 2014

@author: Sylvain
Construction d'un arbre de validation en "dur"
'''

from Node import *


def main():
    print "*** Building validation tree ***"
    print "For any x : For any z : There exists a=x, b=y : x>y and y=z"

    #alias x, y, z dans les noeuds
    aliasX = Alias("x")
    aliasY = Alias("y")
    aliasZ = Alias("z")

    #condition x>y
    condition1 = Condition(">")
    condition1.setTerms(AtomicAliasTerm(aliasX), AtomicAliasTerm(aliasY))

    #condition y=z
    condition2 = Condition("=")
    condition2.setTerms(AtomicAliasTerm(aliasY), AtomicAliasTerm(aliasZ))

    #nodes
    node3 = NodeAnd(3, [], [], aliasZ)
    node2 = NodeOr(2, [], [condition1], aliasY)
    node1 = NodeAnd(1, [node2], [], aliasX)

    #inter
    interdep = Interdependancy([aliasY, aliasZ], [condition2])

    #Central validation (main class)
    central = CentralValidation([interdep], [node1, node3])

    print central.__str__()

    print "***           END              ***"



if __name__ == '__main__':
    main()
