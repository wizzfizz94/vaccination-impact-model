import networkx as nx


'''Graph for social network of individuals'''
class SocialNetworkGraph:

    def __init__(self, nodes, prob):
        self.g = nx.gnp_random_graph(nodes, prob)

    def draw(self):
        nx.draw(self.g)

    def updateGraph(self):
        pass
