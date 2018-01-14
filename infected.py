from random import *
from itertools import *

def powerset(iterable):    
    """
        powerset d'itertools, la méthode n'existe pas explicitement j'ai fait un copier-coller
        de la doc qui la proposé comme exemple d'utilisation de combinaison
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Computer:

    def __init__(self,number):
        self.number = number
        self.infected = False
        self.link = []


class State:

    def __init__(self,graph,player):
        self.graph = graph
        self.list_infected = self.listInfected
        self.player = player        

    def listInfected(self):
        for x in self.graph:
            if x.infected:
                self.list_infected.append(x)
                
    def getAttack(self):
        list_attack = []
        for x in self.list_infected:
            for y in x.link:
                if not y.infected and y not in list_attack:
                    list_attack.append(y)
        return list_attack

    def isFinished(self):
        return getAttack() == []


    def getDefense(self):
        list_defend = []
        for x in self.graph:
            if not x.infected:
                list_couple = []
                for y in x.link:
                    list_couple.append([x,y])
                list_combination = list(powerset(list_couple))
                list_defend.append(list_combination[1:])
        return list_defend

    def getValue(self):
        s = 0
        for x in self.graph:
            if not x.infected:
                s += len(x.link)
        return s
            
        

def initNetwork(n,p):
    graph = []
    
    for i in range(n):
        graph.append(Computer(i))

    for i in range(n):
        for j in range(i,n):
            if i != j:
                rand = random()
                if p >= rand:
                    graph[i].link.append(graph[j])
                    graph[j].link.append(graph[i])

    for x in graph:
        if x.link == []:
            number_rand = randint(0,n-1)
            while number_rand == x.number:
                number_rand = randint(0,n-1)
            x.link.append(graph[number_rand])
            graph[number_rand].link.append(x)
        
    return graph


def main(n,p):
    list_infected = []
    list_state = []
    graph=initNetwork(n,p)
    state = State(graph,None)
    L = state.getDefense()
    
    for x in graph:
        print(x.number,":\n")
        for y in x.link:
            print(y.number)
        print("\n____")
    for x in L:
        print(x)

main(15,0.1)
