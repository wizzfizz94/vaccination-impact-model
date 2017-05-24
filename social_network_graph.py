import networkx as nx
from constants import N, PROB_OF_ASSOCIATION, \
    PROB_OF_ANTI_VAC, COST_RATIO, PERCIEVED_INFECTION_RATE
from individual import Individual
import numpy as np
import random
import matplotlib.pyplot as plt


'''Graph for social network of individuals'''
class SocialNetworkGraph:

    def __init__(self):
        self.graphs = []
        self.graphs.append(nx.watts_strogatz_graph(50, 4, 0.5))
        self.graphs.append(nx.scale_free_graph(
            50, alpha=0.4, beta=0.2, gamma=0.4, delta_in=0, delta_out=0).to_undirected())
        self.graphs.append(nx.barabasi_albert_graph(50, 2))
        for g in self.graphs:
            for i in g.nodes():
                g.node[i]['decision'] = \
                    np.random.choice([1,-1], p=[1-PROB_OF_ANTI_VAC, PROB_OF_ANTI_VAC])
                g.node[i]['weight'] = np.random.normal()

    def draw(self):
        for i, g in enumerate(self.graphs):
            plt.figure(i)
            nx.draw(g)

    def updateGraphs(self):
        for g in self.graphs:
            count = None
            while(count != 0):
                count = 0
                n = self.g.nodes()
                random.shuffle(n)
                for i in n:
                    # calc percieved risk
                    self.calcPerceivedRiskOfInfection(i)
                    # add social influence
                    self.addSocialInfluence(i)
                    # update decision
                    count += self.updateDecision(i)

    def addSocialInfluence(self):
        # calc pro vac influence
        pass

    '''changes individuals choice'''
    def updateDecision(self, index):
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
