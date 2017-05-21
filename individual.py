from constants import COST_RATIO, PERCIEVED_INFECTION_RATE, PROB_OF_ANTI_VAC
import numpy as np
import networkx as nx

'''Class for individuals of nodes in system'''
class Individual:

    def __init__(self, g, node):
        # 1 if vac, -1 if non vac, None otherwise
        self.decision = np.random.choice([1,-1], p=[1-PROB_OF_ANTI_VAC, PROB_OF_ANTI_VAC])
        self.g = g
        self.node = node

    '''changes individuals choice'''
    def changeChoice(self):

        # perceived risk of disease infection
        l = self.calcPerceivedRiskOfInfection()

        if COST_RATIO < l:
            self.decision = 1
        elif COST_RATIO > l:
            self.decision = -1

    '''Gets number of neighbours with decision to vaccinate'''
    def getVacNeighbours(self):
        pass
        neighbours = nx.all_neighbors(self.g, self.node)
        for n in neighbours:
            pass

    '''Gets number of neighbours with decision to not vaccinate'''
    def getNonVacNeighbours(self):
        pass

    '''calc func for perceived risk of disease infection'''
    def calcPerceivedRiskOfInfection(self):
        n_vac = self.getVacNeighbours()
        n_non = self.getNonVacNeighbours()
        self.l = PERCIEVED_INFECTION_RATE * (n_non / (n_non + n_vac))

    '''calc cost for a decision'''
    def calcCost(self):
        return (1 + self.decision)*self.r + (1 + self.decision)*self.l