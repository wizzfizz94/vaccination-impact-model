'''Main loop for time iterataions in model'''
from social_network_graph import SocialNetworkGraph
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''Constants'''
INFECTION_RATE = float(10)
PERCIEVED_INFECTION_RATE = INFECTION_RATE
INFECTION_RISK = float(10)
RECOVERY_RATE = float(0.312)
N = 788
R_0 = float(1.6)
MEAN_ASSOCIATIONS = float(35)
PROB_OF_ASSOCIATION = MEAN_ASSOCIATIONS / N

def update_graph(i, sg):
    sg.updateGraph()


if __name__ == '__main__':
    #build graph and animate simualtion
    g = SocialNetworkGraph(N, PROB_OF_ASSOCIATION)
    g.draw()
    plt.show()
    # fig = plt.figure()
    # animation.FuncAnimation(fig, update_graph, fargs=(g), interval=200, blit=True, repeat=False )
    # plt.show()
