
from random import *
from itertools import *
from copy import deepcopy

def powerset(iterable):    
    """
        powerset d'itertools, la méthode n'existe pas explicitement j'ai fais un copier-coller
        de la doc qui l'a proposée comme exemple d'utilisation de combinations().
        
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Computer:

    def __init__(self,number):
        self.number = number
        self.infected = False
        self.link = []

    def __str__(self):
        return str(self.number)


class IA:

    def minmax(self,state,d):
        if d == 0 or state.isFinished():
            return state.getValue(),None
        if state.player == "defender":
            print('minmax defenser')
            m = float("-inf")
            c = None
            for coup in state.getDefense():
                state_value,c1 = self.minmax(state.playDefense(coup),d-1)
                if state_value > m:
                    m = state_value
                    c = coup
        elif state.player == "attacker":
            print("minmax attacker")
            m = float("inf")
            c = None
            for coup in state.getAttack():
                state_value,c1 = self.minmax(state.playAttack(coup),d-1)
                if state_value < m:
                    m = state_value
                    c = coup
        return m,c


class State:

    def __init__(self,graph,player):
        self.graph = graph
        self.list_infected = self.listInfected()
        self.player = player
    

    def listInfected(self):
        L = []
        for x in self.graph:
            if x.infected:
                L.append(x)
        return L
                
    def getAttack(self):
        list_attack = []
        for x in self.list_infected:
            for y in x.link:
                if not y.infected and y not in list_attack:
                    list_attack.append(y)
        return list_attack

    def isFinished(self):
        return self.getAttack() == []


    def getDefense(self):
        list_defend = []
        for x in self.graph:
            if not x.infected:
                list_couple = []
                for y in x.link:
                    # rajouter .number à x et y pour afficher les numeros des machines
                    list_couple.append([x,y])
                list_combination = list(powerset(list_couple))
                list_defend.append(list_combination[1:])
        return list_defend

    def getValue(self):
        s = 0
        for x in self.graph:
            if not x.infected:
                for y in x.link:
                    if not(y.infected):
                        s += 1
        return s

    def playAttack(self,coup):
        for x in self.graph:
            if x.number == coup.number:
                x.infected = True
        return State(deepcopy(self.graph),"defender")

    def delLink(self,couple):
        if couple[1] in couple[0].link:
            couple[0].link.remove(couple[1])
        #couple[1].link.remove(couple[0])


    def playDefense(self,coup):
        for x in coup:
            for y in x:
                self.delLink(y)
        return State(deepcopy(self.graph),"attacker")

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

    rand_affected = randint(0,n-1)
    graph[rand_affected].infected = True
    
    return graph


def main(n,p):
    list_infected = []
    list_state = []
    
    graph=initNetwork(n,p)
    list_state.append(State(graph,"defender"))
    
    present_state = list_state[-1]

    ia = IA()
    print("value :",present_state.getValue())
    while not(present_state.isFinished()):

        present_state = list_state[-1]
        
        print(present_state.player)
        
        for x in graph:
            print(x,"( infected :",x.infected,")",":\n")
            for y in x.link:
                print(y,"infected :",y.infected)
            print("\n------\n")
    
        new_state=deepcopy(present_state)
        if present_state.player=="attacker":
            value,coup = ia.minmax(new_state,3)
            print("minmax coup = ", coup)
            list_state.append(present_state.playAttack(coup))
        elif present_state.player=="defender":
            value,coup = ia.minmax(new_state,3)
            print("minmax coup = ", coup)
            list_state.append(present_state.playDefense(coup))
        pause = input("oep")




    
    """
    state2 = state.playDefense(L[0][0])
    
    graph2 = state2.graph
    L = state2.getDefense()
    print("ooooooooooooooooooooooooooooooooooooooooooo")
    print(state2.graph)
    
    for x in graph2:
        print(x,"( infected :",x.infected,")",":\n")
        for y in x.link:
            print(y,"infected :",y.infected)
        print("\n------\n")

    for x in L:
        print(x)
    print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    """


# ATTENTION 
# gaffe aux nombre de pc mis
# surtout ...
# surtout ne pas plus 10 pc avec une probabilité de 0.9
# sous cause de plantage total
# ATTENTION

test = main(5,0.5)
