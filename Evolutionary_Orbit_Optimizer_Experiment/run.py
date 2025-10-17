from Optimizer import EvolutionaryOptimizer, MultithreadedEvolutionaryOptimizer
from OrbitAsSolution import Const_Solution
from Scoring import score_constellation

# RUN THIS FILE TO EVOLVE AN OPTIMAL ORBIT




# # Single Threaded Approach
# seed_sol = Const_Solution()
# optimizer = EvolutionaryOptimizer(seed_sol)
# optimizer.anneal_rate = 0.1
# optimizer.generation_size = 100
# final_sol = optimizer.train(score_constellation, 100, 1, True)
# score_constellation(final_sol, 1)

# MultiThreaded Approach
seed_sol = Const_Solution()
optimizer = MultithreadedEvolutionaryOptimizer(seed_sol, 5) # use 5 threads
optimizer.anneal_rate = 0.1
optimizer.generation_size = 1000
final_sol = optimizer.train(score_constellation, 20, 1, True)
print("\n")
score_constellation(final_sol, 1)

print("\n\n----------- FINAL SOLUTION -----------")
print(final_sol._to_string())
