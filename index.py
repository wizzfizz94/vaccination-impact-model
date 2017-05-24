'''Main loop for time iterataions in model'''
from social_network_graph import SocialNetworkGraph
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_graph(i, sg):
    sg.updateGraph()


if __name__ == '__main__':
    # build graph and animate simualtion
    sng = SocialNetworkGraph()
    stable = False
    sng.draw()
    sng.updateGraphs()
    plt.show()

    # fig = plt.figure()
    # animation.FuncAnimation(fig, update_graph, fargs=(g), interval=200, blit=True, repeat=False )
    # plt.show()
