import math

'''Constants'''
INFECTION_RATE = float(0.5)
SOCIAL_INFLUENCE_FACTOR = float(0.5)
CLOSENESS_FACTOR = float(0.6)
PERCIEVED_INFECTION_RATE = INFECTION_RATE
INFECTION_RISK = float(10)
RECOVERY_RATE = float(0.312)
N = 788
REPRODUCTION_NUMBER = float(5)
MEAN_ASSOCIATIONS = float(35)
PROB_OF_ASSOCIATION = MEAN_ASSOCIATIONS / N
COST_RATIO = float(0.5)
PROB_OF_ANTI_VAC = 0.3
RESPONSIVENESS = 5

I_START = math.floor(max(N * 0.01, 1))
