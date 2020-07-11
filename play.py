from life import *

s = SimulationParams(100, 100, 50, 200)
g = GraphicGeneticAlgorithm(s, RouletteWheelSelector(2), 0.5, 25)
g.play(100, 200)