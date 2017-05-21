import networkx as nx
from constants import N, PROB_OF_ASSOCIATION, \
    PROB_OF_ANTI_VAC, COST_RATIO, PERCIEVED_INFECTION_RATE
from individual import Individual
import numpy as np
import random


'''Graph for social network of individuals'''
class SocialNetworkGraph:

    def __init__(self):
        self.g = nx.newman_watts_strogatz_graph(N, 30, 0.3)
        # self.g = nx.scale_free_graph(
        #     N, alpha=0.8, beta=0.1, gamma=0.1, delta_in=0, delta_out=0).to_undirected()
        for i in self.g.nodes():
            self.g.node[i]['decision'] = \
                np.random.choice([1,-1], p=[1-PROB_OF_ANTI_VAC, PROB_OF_ANTI_VAC])

    def draw(self):
        nx.draw(self.g)

    def updateGraph(self):
        count = 0
        n = self.g.nodes()
        random.shuffle(n)
        for i in n:
            # calc percieved risk
            self.calcPerceivedRiskOfInfection(i)
            # update decision
            count += self.changeChoice(i)
        return count == 0

    '''changes individuals choice'''
    def changeChoice(self, index):
        l = self.g.node[index]['percieved_risk']
        d = self.g.node[index]['decision']
        if COST_RATIO < l and d == -1:
            self.g.node[index]['decision'] = 1
            return 1
        elif COST_RATIO > l and d == 1:
            self.g.node[index]['decision'] = -1
            return 1
        return 0

    '''Gets number of neighbours with decision to vaccinate'''
    def getVacNeighbours(self, index):
        n = self.g.neighbors(index)
        n_vac = []
        for i in n:
            if self.g.node[i]['decision'] == 1:
                n_vac.append(i)
        return float(len(n_vac))

    '''Gets number of neighbours with decision to not vaccinate'''
    def getNonVacNeighbours(self, index):
        n = self.g.neighbors(index)
        n_non = []
        for i in n:
            if self.g.node[i]['decision'] == -1:
                n_non.append(i)
        return float(len(n_non))

    '''calc func for perceived risk of disease infection'''
    def calcPerceivedRiskOfInfection(self, index):
        n_vac = self.getVacNeighbours(index)
        n_non = self.getNonVacNeighbours(index)
        self.g.node[index]['percieved_risk'] = PERCIEVED_INFECTION_RATE * (n_non / (n_non + n_vac))
