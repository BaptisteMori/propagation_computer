
# Baptiste Mori 21602052
# Valentin Leblond 21609038

from random import *
from itertools import *
from copy import deepcopy

def powerset(iterable):    
    """
        powerset d'itertools, la méthode n'existe pas explicitement on a fait un copier-coller
        de la doc qui l'a proposée comme exemple d'utilisation de combinations()

        https://docs.python.org/3/library/itertools.html
        
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

    def __eq__(self,other):
        return self.number == other.number


class IA:

    def minmax(self,state,d,alphabeta):
        if d == 0 or state.isFinished():
            return state.getValue(),None
        if state.player == "defender":
            m = float("-inf")
            c = None
            for ordi in state.getDefense():
                for coup in ordi:
                    if alphabeta:
                        state_value = self.alphabeta(state.playDefense(coup),m,state.getValue(),d-1)
                    else:
                        state_value,c1 = self.minmax(state.playDefense(coup),d-1)
                    if state_value > m:
                        m = state_value
                        c = coup
        else:
            m = float("inf")
            c = None
            for coup in state.getAttack():
                if alphabeta:
                    state_value = self.alphabeta(state.playAttack(coup),state.getValue(),m,d-1)
                else:
                    state_value,c1 = self.minmax(state.playAttack(coup),d-1)
                if state_value < m:
                    m = state_value
                    c = coup
        return m,c

    def alphabeta(self,state,alpha,beta,d):
        if d == 0 or state.isFinished():
            return state.getValue()
        else:
            if state.player == "defender":
                for ordi in state.getDefense():
                    for coup in ordi:
                        alpha = max(alpha,self.alphabeta(state.playDefense(coup),alpha,beta,d-1))
                        if alpha >= beta:
                            return alpha
                return alpha
            else:
                for ordi in state.getAttack():
                    beta = min(beta,self.alphabeta(state.playAttack(ordi),alpha,beta,d-1))
                    if alpha >= beta:
                        return beta
                return beta


class State:

    def __init__(self,graph,player):
        self.graph = graph
        self.list_infected = self.listInfected()
        self.player = player

    def __str__(self):
        ch = ""
        ch += "\n" + self.player + " :\n\n"
        for x in self.graph:
            ch += str(x) + " ( infected : " + str(x.infected) + " ) :\n\n"
            for y in x.link:
                ch += str(y) + " infected : " + str(y.infected) + "\n"
            ch += "\n------\n\n"
        return ch

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
        new_graph = deepcopy(self.graph)
        for x in new_graph:
            if x == coup:
                x.infected = True
        return State(new_graph,"defender")

    def delLink(self,new_graph,couple):
        first = None
        second = None
        for ordi in new_graph:
            if ordi == couple[0]:
                first = ordi
            if ordi == couple[1]:
                second = ordi
        first.link.remove(second)
        second.link.remove(first)


    def playDefense(self,coup):
        new_state = State(deepcopy(self.graph),"attacker")
        for x in coup:
            new_state.delLink(new_state.graph,x)
        return new_state


def initNetwork(nbOrdi,nbInfected,proba):
    graph = []
    
    for i in range(nbOrdi):
        graph.append(Computer(i))

    for i in range(nbOrdi):
        for j in range(i,nbOrdi):
            if i != j:
                rand = random()
                if proba >= rand:
                    graph[i].link.append(graph[j])
                    graph[j].link.append(graph[i])

    for x in graph:
        if x.link == []:
            number_rand = randint(0,nbOrdi-1)
            while number_rand == x.number:
                number_rand = randint(0,nbOrdi-1)
            x.link.append(graph[number_rand])
            graph[number_rand].link.append(x)

    cpt = 0
    while cpt != nbInfected:
        rand_affected = randint(0,nbOrdi-1)
        if not graph[rand_affected].infected:
            graph[rand_affected].infected = True
            cpt += 1
    return graph


def main(nbOrdi,nbInfected,proba,prof_attacker,prof_defender,alphabeta):
    list_infected = []
    list_state = []
    
    graph=initNetwork(nbOrdi,nbInfected,proba)
    
    present_state = State(graph,"attacker")
    list_state.append(present_state)

    ia = IA()
    print("value defender de départ :",present_state.getValue())
    while not(present_state.isFinished()):

        print(present_state)
        new_state=deepcopy(present_state)
        
        if present_state.player=="attacker":
            
            value,coup = ia.minmax(new_state,prof_attacker,alphabeta)
            
            present_state = present_state.playAttack(coup)
            list_state.append(present_state)
            print("choix attacker : " + str(coup)) 
        else:
            
            value,coup = ia.minmax(new_state,prof_defender,alphabeta)
            
            for x in coup:
                print("choix defender : ",str(x[0]),str(x[1]))
            present_state = present_state.playDefense(coup)
            list_state.append(present_state)
        pause = input("...")
    print(present_state)
    print("value defender : " + str(present_state.getValue()))


# ATTENTION 
# gaffe aux nombre de pc mis
# surtout ...
# surtout ne pas plus 10 pc avec une probabilité de 0.9
# sous cause de plantage total
# ATTENTION

main(15,1,0.2,3,3,True)
