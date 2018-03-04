"""
    Baptiste Mori 21602052
    Valentin Leblond 21609038
    groupe 4A
"""

from random import *
from itertools import *
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


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
        """
            Classe représentant un ordinateur

            attribut (int) number : l'identifiant de l'ordinateur
            attribut (boolean) infected : boolean indiquant si l'ordinateur est infecte
            attribut (list) link : liste des autres ordinateur auxquels l'ordinateur est connecte 
        """
        self.number = number
        self.infected = False
        self.link = []

    def __str__(self):
        """
            L'affichage de l'ordinateur est l'affichage de son identifiant
        """
        return str(self.number)

    def __eq__(self,other):
        """
            Deux ordinateurs sont egaux si ils ont le meme identifiant
        """
        return self.number == other.number


class IA:

    """
        Classe de l'IA
    """
    def __init__(self):
        """
            Contient les compteurs des algorithmes alphabeta et minmax

            atribut (int) n_mm : conteur de minmax
            atribut (int) n_ab : conteur de alphabeta
        """
        self.n_mm = 0
        self.n_ab = 0

    def minmax(self,state,d):
        '''
            Algorithme Minmax

            param (State) state : l'etat du jeu
            param (int) d : la profondeur dans l'arbre de l'IA
            return (int,Computer or tuple): la valeur du noeud et le coup a jouer pour aller a ce noeud
        '''
        self.n_mm += 1
        if d == 0 or state.isFinished():
            return state.getValue(),None
        if state.player == "defender":
            m = float("-inf")
            c = None
            for ordi in state.getDefense():
                for coup in ordi:
                    state_value,c1 = self.minmax(state.playDefense(coup),d-1)
                    if state_value > m:
                        m = state_value
                        c = coup
        else:
            m = float("inf")
            c = None
            for coup in state.getAttack():
                state_value,c1 = self.minmax(state.playAttack(coup),d-1)
                if state_value < m:
                    m = state_value
                    c = coup
        return m,c

    def alphabeta(self,state,alpha,beta,d):
        '''
            Algorithme Alphabeta

            param (State) state : l'etat du jeu
            param (int) alpha : valeur minimum du joueur Max
            param (int) beta : la valeur maximum du joueur Min
            param (int) d : la profondeur dans l'arbre de l'IA
            return (int,Computer or tuple) : la meilleur valeur obtenable du noeud
        '''
        self.n_ab += 1
        if d == 0 or state.isFinished():
            return state.getValue(),None
        else:
            if state.player == "defender":
                m = float("-inf")
                c = None
                for ordi in state.getDefense():
                    for coup in ordi:
                        value,action = self.alphabeta(state.playDefense(coup),alpha,beta,d-1)
                        if value > m:
                            c = coup
                            m = value
                        alpha = max(alpha,value)
                        if alpha >= beta:
                            return alpha,coup
                return alpha,c
            else:
                m = float("inf")
                c = None
                for ordi in state.getAttack():
                    value,action = self.alphabeta(state.playAttack(ordi),alpha,beta,d-1)
                    if value < m:
                        c = ordi
                        m = value
                    beta = min(beta,value)
                    if alpha >= beta:
                        return beta,ordi
                return beta,c

    def reset(self):
        """
            rinitialise les compteurs
        """
        self.n_mm = 0
        self.n_ab = 0


class State:

    def __init__(self,graph,player):
        """
            Classe de l'etat du jeu

            attribut (list) graph : liste des ordinateurs du reseau
            attribut (str) player : nom du joueur (attaquant ou defenseur)
            attribut (list) list_infected : liste des ordinateurs infectes
        """
        self.graph = graph
        self.list_infected = self.listInfected()
        self.player = player

    def __str__(self):
        """
            Affichage de l'etat du jeu
        """
        ch = ""
        ch += "\n" + self.player + " :\n\n"
        for x in self.graph:
            ch += str(x) + " ( infected : " + str(x.infected) + " ) :\n\n"
            for y in x.link:
                ch += str(y) + " infected : " + str(y.infected) + "\n"
            ch += "\n------\n\n"
        return ch

    def listInfected(self):
        """
            Liste les ordinateurs infectes
            
            return (list) : liste des ordinateurs infectes
        """
        L = []
        for x in self.graph:
            if x.infected:
                L.append(x)
        return L
                
    def getAttack(self):
        """
            Liste tous les ordinateurs qui peuvent etre attaques
            
            return (list) : liste des ordinateurs
        """
        list_attack = []
        for x in self.list_infected:
            for y in x.link:
                if not y.infected and y not in list_attack:
                    list_attack.append(y)
        return list_attack

    def isFinished(self):
        """
            Test si la partie est finie, elle l'est quand l'attaquant ne peut plus jouer
            
            return (boolean) : True si la partie est finie
        """
        return self.getAttack() == []


    def getDefense(self):
        """
            Liste tous les coups jouables par le defenseur

            return (list) : liste des coup sous la forme suivante

            Liste de liste par ordi
                tuple des coups de l'ordi
                    liste d'un couple [ordi1,ordi2]

            exemple si on a 3 ordi avec ordi1 connecte avec le 2 et 3 et le 2 connecte avec le 1:
            [ [([ordi1,ordi2],),([ordi1,ordi3],),([ordi1,ordi2],[ordi1,ordi3])] , [([ordi2,ordi1],)] , [] ]
                                          ordi1                                         ordi2         ordi3
        """
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
        """
            Fonction d'evaluation

            return (int) : le nombre de liens que les ordinateurs non-infectes ont avec
            d'autres ordinateurs non-infectes
        """
        s = 0
        for x in self.graph:
            if not x.infected:
                for y in x.link:
                    if not(y.infected):
                        s += 1
        return s

    def playAttack(self,coup):
        """
            Infecte l'odinateur donne

            param (Computeur) coup : ordinateur qui a infecter
            return (State) : le nouvel etat après infection
        """
        new_graph = deepcopy(self.graph)
        for x in new_graph:
            if x == coup:
                x.infected = True
        return State(new_graph,"defender")

    def delLink(self,new_graph,couple):
        """
            Supprime le lien entre 2 ordinateurs

            param (list) new_graph : le graph dans lequel on va supprimer le lien
            param (list) couple : couple d'ordinateurs a separer
        """
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
        """
            Supprime tous les liens du coup donne

            param (tuple) : le tuple des couples d'ordinateurs a separer
            return (State) : le nouvel etat après suppression des liens
        """
        new_state = State(deepcopy(self.graph),"attacker")
        for x in coup:
            new_state.delLink(new_state.graph,x)
        return new_state


def initNetwork(nbOrdi,nbInfected,proba):
    """
        Initialisation d'un graph

        param (int) nbOrdi : nombre d'ordinateurs a creer
        param (int) nbInfected : nombre d'ordinateurs qui doient etre infectes
        param (float) proba : probabilite qu'un lien se forme entre 2 ordinateurs
        return (list) : graph construit
    """
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


def main2Ia(nbOrdi, nbInfected, proba, prof_attacker, prof_defender,sameGraph=[]):
    """
        Fonction principale avec alphabeta et minmax en parallèle

        param (int) nbOrdi : nombre d'ordinateurs du reseau
        param (int) nbInfected : nombre d'ordinateurs infectes au départ
        param (float) proba : probabilité qu'un lien se forme entre 2 ordinateurs
        param (int) prof_attacker : profondeur de l'IA de l'attaquant
        param (int) prof_defender : profondeur de l'IA du defenseur
        param (list) sameGraph : utilisation d'un graph particulier
    """
    list_infected = []
    list_state = []

    if sameGraph != []:
        graph = deepcopy(sameGraph)
        graph_mm = deepcopy(sameGraph)
    else:
        graph = initNetwork(nbOrdi,nbInfected,proba)
        graph_mm = deepcopy(graph)
    
    present_state = State(graph,"defender")
    present_state_mm = State(graph_mm,"defender")
    list_state.append(present_state)

    ia = IA()
    print("value defender de départ :",present_state.getValue())
    while not(present_state.isFinished()) or not(present_state_mm.isFinished()):
        print("Alphabeta :")
        print(present_state)
        print("Minmax :")
        print(present_state_mm)
        new_state = deepcopy(present_state)
        new_state_mm = deepcopy(present_state_mm)
        
        if present_state.player == "attacker":

            if not(present_state.isFinished()):
                value,coup = ia.alphabeta(new_state,float("-inf"),float("inf"),prof_attacker)
                present_state = present_state.playAttack(coup)
                print("choix attacker_alphabeta : " + str(coup))
            if not(present_state_mm.isFinished()):
                value_mm,coup_mm = ia.minmax(new_state_mm,prof_attacker) 
                present_state_mm = present_state_mm.playAttack(coup_mm)
                print("choix attacker_minmax : " + str(coup_mm))
            
            print("n_ab :",ia.n_ab)
            print("n_mm :",ia.n_mm)
            
            list_state.append(present_state)
        else:
            
            if not(present_state.isFinished()):
                value,coup = ia.alphabeta(new_state,float("-inf"),float("inf"),prof_defender)
                present_state = present_state.playDefense(coup)
                for x in coup:
                    print("choix defender_alphabeta : ",str(x[0]),"--",str(x[1]))

            if not(present_state_mm.isFinished()):
                value_mm,coup_mm = ia.minmax(new_state_mm,prof_defender)
                present_state_mm = present_state_mm.playDefense(coup_mm)
                for x in coup_mm:
                    print("choix defender_minmax : ",str(x[0]),"--",str(x[1]))


            print("n_ab :",ia.n_ab)
            print("n_mm :",ia.n_mm) 
            
            list_state.append(present_state)
        #ia.reset()
        pause = input("...")
        print("<>"*30)
        print("Value defender_ab :",present_state.getValue())
        print("Value defender_mm :",present_state_mm.getValue())
    print("Alphabeta :")
    print(present_state)
    print("Minmax :")
    print(present_state_mm)
    print("value defender_alphabeta : " + str(present_state.getValue()))
    print("value defender_minmax : " + str(present_state_mm.getValue()))
    return ia


def main(nbOrdi, nbInfected, proba, prof_attacker, prof_defender, alphabeta):
    """
        Fonction principale

        param (int) nbOrdi : nombre d'ordinateurs du reseau
        param (int) nbInfected : nombre d'ordinateurs infectes au départ
        param (float) proba : probabilité qu'un lien se forme entre 2 ordinateurs
        param (int) prof_attacker : profondeur de l'IA de l'attaquant
        param (int) prof_defender : profondeur de l'IA du defenseur
        param (boolean) alphabeta : utilisation de l'algorithme alphabeta
    """
    list_infected = []
    list_state = []
    
    graph = initNetwork(nbOrdi,nbInfected,proba)
    
    present_state = State(graph,"defender")
    list_state.append(present_state)

    ia = IA()
    print("value defender de départ :",present_state.getValue())
    while not(present_state.isFinished()):

        print(present_state)
        new_state = deepcopy(present_state)
        
        if present_state.player == "attacker":
            if alphabeta:
                value,coup = ia.alphabeta(new_state,float("-inf"),float("inf"),prof_attacker)
            else:
                value,coup = ia.minmax(new_state,prof_attacker)
            print("choix attacker : " + str(coup))
            
            present_state = present_state.playAttack(coup)
            list_state.append(present_state)
        else:

            if alphabeta:
                value,coup = ia.alphabeta(new_state,float("-inf"),float("inf"),prof_defender)
            else :
                value,coup = ia.minmax(new_state,prof_defender)
            
            for x in coup:
                print("choix defender : ",str(x[0]),"--",str(x[1]))
                
            present_state = present_state.playDefense(coup)
            list_state.append(present_state)
        pause = input("...")
        print("<>"*30)
        print("Value defender :",present_state.getValue())
    print(present_state)
    print("value defender : " + str(present_state.getValue()))
    
    cpt_com_infected = 0
    for ordi in present_state.graph:
        if ordi.infected:
            cpt_com_infected += 1

    if nbOrdi//2 < cpt_com_infected:
        print("L'attaquant a gagné")
    else:
        print("Le defenseur a gagné")
    print("Nombre de noeuds parcourus durant la partie :",ia.n_mm + ia.n_ab)


def showGraphStat(x,ab,mm):
    """
        affiche graphiquement x en fonction de ab et x en fonction de mm
    """
    plt.plot(x,ab,"red")
    plt.plot(x,mm,"green")
    courbe_alphabeta = mlines.Line2D(x, ab, color='red', label='Alphabeta')
    courbe_minmax = mlines.Line2D(x, mm, color='green', label='Minmax')
    plt.legend(handles=[courbe_alphabeta,courbe_minmax])
    plt.show()

def testProf(prof):
    """
        test du nombre de calculs des algorithmes de 1 à prof

        param (int) prof : la profondeur maximale auquel on va regarder
        note : on utilisera le meme graph pour le test de chaque profondeur
    """
    x = np.arange(1,prof+1)
    ab = np.zeros(prof)
    mm = np.zeros(prof)
    graph = initNetwork(5,1,0.5)
    for k in range(1,prof+1):
        ia = main2Ia(5,1,0.5,k,k,graph)
        ab[k-1] = ia.n_ab
        mm[k-1] = ia.n_mm
    print(ab)
    print(mm)
    showGraphStat(x,ab,mm)

def testProba(probaMax):
    """
        test du nombre de calculs des algorithmes de 1 à probaMax

        param (float) probaMax : la probabilite maximale auquel on va regarder
        note : on utilisera pas le même graph pour chaque probabilité
    """
    x = np.arange(0,probaMax+0.1,0.1)
    ab = np.zeros(int(10*probaMax)+1)
    mm = np.zeros(int(10*probaMax)+1)
    for p in range(int(probaMax*10)+1):
        ia = main2Ia(5,1,p/10,5,5)
        ab[p-1] = ia.n_ab
        mm[p-1] = ia.n_mm
    print(ab)
    print(mm)
    showGraphStat(x,ab,mm)

if __name__ == "__main__":
    
    main(5,1,0.5,5,5,True)
    
    #main2Ia(5,1,0.5,5,5)
    
    #testProf(6)
    
    #testProba(0.6)






