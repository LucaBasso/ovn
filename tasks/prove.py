import random
import string

import scipy.constants
from scipy.constants import *
from core.elements import *

class Ciao:
    def __init__(self):
        self._stringa="ciaociao"

    @property
    def stringa(self):
        return self._stringa


def main():
    # stringa="ciao"
    # prova=['A','B']
    # print(str(prova))
    #dizionario={"casfadf":{"1":1,"2":[2,3,4]},"ciao":"Luca è bello"}
    #print(list(dizionario.keys()))
    #ciaociao=Ciao()
    #for i in range(len(ciaociao.stringa)-1):
    #    print(ciaociao.stringa[i]+ciaociao.stringa[i+1])

    #nodi=["A","B","C","D","E"]
    # T=[[1 for i in range(len(nodi))] for j in range(len(nodi))]
    # print(T)
    # for i in range(len(nodi)):
    #     T[i][i]=0
    #     print(i)
    # print(T)
    # T={}
    # for node1 in nodi:
    #     T.update({node1:{}})
    #     for node2 in nodi:
    #         if node1!=node2:
    #             T[node1].update({node2:100})
    #         else:
    #             T[node1].update({node2:0})
    # print(T)
    # net=Network("/home/luchino/scuola/ovn/resources/258211.json")
    # net.draw()
    for i in range(10):
        print(i)

if __name__ == "__main__":
    main()