import networkx as nx
from constants import N, RECOVERY_RATE, \
PROB_OF_ANTI_VAC, COST_RATIO, INFECTION_RATE, PERCIEVED_INFECTION_RATE,\
RESPONSIVENESS, REPRODUCTION_NUMBER, I_START, INFECTION_RISK
import numpy as np
import random
import matplotlib.pyplot as plt
import math


'''Graph for social network of individuals'''
class SocialNetworkGraph:

    def __init__(self):
        self.graphs = []
        self.graphs.append(nx.watts_strogatz_graph(N, 4, 0.5))
        self.graphs.append(nx.scale_free_graph(
            N, alpha=0.4, beta=0.2, gamma=0.4, delta_in=0, delta_out=0).to_undirected())
        self.graphs.append(nx.barabasi_albert_graph(N, 2))
        for i, g in enumerate(self.graphs):
            for i in g.nodes():
                g.node[i]['decision'] = \
                    np.random.choice([1,-1], p=[1-PROB_OF_ANTI_VAC, PROB_OF_ANTI_VAC])
                g.node[i]['weight'] = float(np.random.binomial(1000, 0.5, 1))/float(1000)
                g.node[i]['social-influence'] = float(np.random.binomial(1000, 0.5, 1)) / float(1000)

    def draw(self):
        for i, g in enumerate(self.graphs):
            plt.figure(i)
            vac = []
            non = []
            pos = nx.spring_layout(g, weight=None)
            for i in g.nodes():
                if g.node[i]['decision'] == 1:
                    vac.append(i)
                else:
                    non.append(i)
            nx.draw_networkx_nodes(g, pos,
                                   nodelist=vac,
                                   node_color='b',
                                   alpha=0.5,
                                   label="Pro Vaxx")
            nx.draw_networkx_nodes(g, pos,
                                   nodelist=non,
                                   node_color='r',
                                   alpha=0.5,
                                   label="Anti Vaxx")
            nx.draw(g)

    def updateGraphs(self):
        for i, g in enumerate(self.graphs):
            count = None
            while(count != 0):
                count = 0
                n = g.nodes()
                random.shuffle(n)
                for i in n:
                    # calc percieved risk
                    self.calcPerceivedRiskOfInfection(g, i)
                    # update decision
                    count += self.updateDecision(g, i)
            # add social influence
            self.addSocialInfluence(g)
            # access impact
            v_0 = self.calcInfectionRate(g, i)

    def calcInfectionRate(self, g, index):
        s, i, r = [], [], []
        R = 0
        I = I_START
        S = N - I
        # exclude vaccinated individuals
        for j in g.nodes():
            if g.node[j]['decision'] == 1:
                S -= 1
        dS, dR, dI = None, None, None
        beta = REPRODUCTION_NUMBER * RECOVERY_RATE
        while (dS == None or np.absolute(dS) > 0.001 or np.absolute(dI) > 0.001 or np.absolute(dR) > 0.001 ):
            s.append(S)
            i.append(I)
            r.append(R)
            lam = beta * I / N
            dS = -lam * S
            dI = lam * S - RECOVERY_RATE * I
            dR = RECOVERY_RATE * I
            S = max(S + dS, 0)
            I = max(I + dI, 0)
            R = max(R + dR, 0)
        plt.figure(index)
        plt.plot(range(len(s)), s)
        plt.plot(range(len(i)), i)
        plt.plot(range(len(r)), r)




    def addSocialInfluence(self, g):
        n = g.nodes()
        random.shuffle(n)
        for i in n:
            l_vac = 0
            l_non = 0
            neighbours = g.neighbors(i)
            for j in neighbours:
                if g.node[j]['decision'] == 1:
                    l_vac += g.node[i]['weight']
                else:
                    l_non += g.node[i]['weight']

            l_diff = (l_vac - l_non)/(l_vac + l_non)
            prob = 1/(1 + math.exp(-RESPONSIVENESS*l_diff))
            sd = np.random.choice([1, -1], p=[prob, 1-prob])
            org = g.node[i]['decision']
            new = g.node[i]['decision'] = np.random.choice([g.node[i]['decision'], sd],
                p=[g.node[i]['social-influence'], 1-g.node[i]['social-influence']])
            if org != new:
                pass


    '''changes individuals choice'''
    def updateDecision(self, g, index):
        l = g.node[index]['percieved_risk']
        d = g.node[index]['decision']
        if COST_RATIO < l and d == -1:
            g.node[index]['decision'] = 1
            return 1
        elif COST_RATIO > l and d == 1:
            g.node[index]['decision'] = -1
            return 1
        return 0

    '''Gets number of neighbours with decision to vaccinate'''
    def getVacNeighbours(self, g, index):
        n = g.neighbors(index)
        n_vac = []
        for i in n:
            if g.node[i]['decision'] == 1:
                n_vac.append(i)
        return float(len(n_vac))

    '''Gets number of neighbours with decision to not vaccinate'''
    def getNonVacNeighbours(self, g, index):
        n = g.neighbors(index)
        n_non = []
        for i in n:
            if g.node[i]['decision'] == -1:
                n_non.append(i)
        return float(len(n_non))

    '''calc func for perceived risk of disease infection'''
    def calcPerceivedRiskOfInfection(self, g, index):
        n_vac = self.getVacNeighbours(g, index)
        n_non = self.getNonVacNeighbours(g, index)
        g.node[index]['percieved_risk'] = PERCIEVED_INFECTION_RATE * (n_non / (n_non + n_vac))


if __name__ == '__main__':
    sng = SocialNetworkGraph()
    stable = False
    sng.draw()
    sng.updateGraphs()
    plt.show()