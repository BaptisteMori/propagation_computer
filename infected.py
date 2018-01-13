from random import *

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
        # module itertools methode powerset
        list_couple = []
        list_defend = []
        for x in self.graph:
            if not x.infected:
                for y in x.link:
                    if not y.infected:
                        list_couple.append([x,y])
            list_defend.append(
            list_defend.append([x,list_couple])
        
                

    #def getValue(self):
        

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
            number_rand = randint(0,n)
            x.link.append(graph[number_rand])
            graph[number_rand].link.append(x)
        
    return graph

    



def main(n,p):
    list_infected = []
    list_state = []
    graph=initNetwork(n,p)
    for x in graph:
        print(x.number," : ")
        for y in x.link:
            print(y.number)

main(15,0.01)
