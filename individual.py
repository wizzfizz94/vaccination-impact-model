'''Class for individuals of nodes in system'''
class Individual:

    def __init__(self):

        # 1 if vac, -1 if non vac, None otherwise
        self.decision = None

    '''changes individuals choice'''
    def changeChoice(self):

        # Calc r
        r = None

        # perceived risk of disease infection
        l = None

        if(r < l):
            self.decision = 1
        elif r > l:
            self.decision = -1

    '''Gets number of neighbours with decision to vaccinate'''
    def getVacNeighbours(self):
        pass

    '''Gets number of neighbours with decision to not vaccinate'''
    def getNoVacNeighbours(self):
        pass

    '''calc func for perceived risk of disease infection'''
    def calcPerceivedRiskOfInfection(self):
        n_vac = self.getVacNeighbours()
        n_non = self.getNoVacNeighbours()
        self.l = b * (n_non / (n_non + n_vac))

    '''calc cost for a decision'''
    def calcCost(self):
        return (1 + self.decision)*self.r + (1 + self.decision)*self.l