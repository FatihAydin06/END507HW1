# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 14:19:26 2021

@author: Fatih
"""

import numpy as np
import numpy.random as rn
import pandas as pd

dist1 = pd.read_csv('dist.csv')
flow1 = pd.read_csv('flow.csv')
transformation1 = pd.read_csv('transformation.csv')

dist = dist1.to_numpy()
flow = flow1.to_numpy()
transformation = transformation1.to_numpy()
r = np.zeros(shape=(5))

def annealing(random_start,
              cost_fnc,
              random_neighbour,
              acceptance,
              temperature,
              maxsteps=250,
              debug=True):
    state = random_start()
    cost = cost_fnc(state)
    states, costs = [state], [cost]
    for step in range(maxsteps):
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = random_neighbour(state, fraction)
        new_cost = cost_fnc(new_state)
        if debug: print("Step #{:>2}/{:>2} : T = {:>4.3g}, state = {:>4.3g}, cost = {:>4.3g}, new_state = {:>4.3g}, new_cost = {:>4.3g} ...".format(step, maxsteps, T, state, cost, new_state, new_cost))
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
    return state, cost_fnc(state), states, costs

interval = (0, 119)

def f(x):
    for i in range(5):
        r[i] = transformation[x,i]
        a = 0
    for i in range(5):
        for j in range(5):
            a = a + flow[i,j]*dist[int(r[i])-1,int(r[j])-1]
        #sum(flow[i,j]*dist[int(r[i]),int(r[j])] for i,j in range(5))
    return a

def clip(x):
    a, b = interval
    return max(min(x, b), a)

def random_start():
    a, b = interval
    #return int(round(a + (b - a) * rn.random_sample()))
    return 29
def cost_fnc(x):
    return f(x)
def random_neighbour(x, fraction=1):
    amp = (max(interval) - min(interval)) * (fraction)
    delta = (-amp/2.) + amp * rn.random_sample()
    return int(round(clip(x + delta)))
def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        # print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temperature)
        # print("    - Acceptance probabilty = {:.3g}...".format(p))
        return p
def temperature(fraction):
    return max(0.01, min(1, 1 - (fraction**0.5)))

annealing(random_start, cost_fnc, random_neighbour, acceptance_probability, temperature, maxsteps=250, debug=True);