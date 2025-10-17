import math
import threading

class OptimizeableSolution:
    def __init__(self):
        print("Cannot initialize abstract class.")
        
    def getRandomSolution(self):
        print("Function not implemented")
    
    def fudgeSelf(self, fudge_factor):
        print("Function not implemented")
    
    # create a new solution that is the old sulution randomly fudged a bit
    def fudgeSolution(self, fudge_factor):
        print("Function not implemented")
    
    # create new solutions based on two parents
    def makeBabies(self, other_parent, fudge_factor, count, include_parents=True):
        print("Function not implemented")
    


class EvolutionaryOptimizer:
    def __init__(self, seed_sol : OptimizeableSolution):
        self.seed = seed_sol
        self.max_learn_rate = 1
        self.generation_size = 100
        self.fudge_factor_calc = self.exp_fudge_factor
        self.anneal_rate = 0.5
    
    def lerp_fudge_factor(self, cur_epoch, last_epoch):
        perc = (last_epoch - cur_epoch) / last_epoch
        return perc * self.max_learn_rate
    
    def exp_fudge_factor(self, cur_epoch, last_epoch):
        return math.exp(-self.anneal_rate * (cur_epoch))
    
    def train(self, score, epochs, print_interval=10, random_first_gen=True):
        print("Beginning training...")

        parents = []
        if (not random_first_gen):
            parents = [self.seed.fudgeSolution(0), self.seed.fudgeSolution(0)] # copy seed solution
        
        generation = []
        for c_ep in range(epochs):
            if ((c_ep == 0) and random_first_gen):
                for i in range(self.generation_size):
                    generation.append(self.seed.fudgeSolution(0).getRandomSolution())
            else:
                generation = parents[0].makeBabies(parents[1], self.fudge_factor_calc(c_ep, epochs), 
                                                self.generation_size, True)
            
            scored = []
            for i in range(len(generation)):
                new_score = score(generation[i])
                scored.append((new_score, generation[i]))
            
            scored.sort(key=(lambda pair : pair[0]), reverse=True)
            parents = [scored[0][1], scored[1][1]] # get the actual models
                
            top_performance = scored[0][0] # get the highest score out of the table

            if (c_ep % print_interval == 0):
                print("\tFinished epoch " + str(c_ep) + " out of " + str(epochs) 
                      + " : SCORE (" + str(top_performance) + ")")
        
        print("TRAINING COMPLETE: Best = " + str(score(parents[0])))
        return parents[0]






class GenerationBatch:
    def __init__(self, generation, chunk_size):
        self.todo = []
        for i in range(chunk_size):
            if (len(generation) == 0): # if for some reason all the tasks have been taken, this one will just be empty
                self.done = []
                print("EMPTY THREAD DISPATCHED")
                return
            
            self.todo.append(generation.pop())
        self.done = []
    
    def purge(self, scored_table):
        if (len(self.todo)):
            print("ERROR: Purging incomplete GenerationBatch")
        while (len(self.done)):
            scored_table.append(self.done.pop())

    def score_all(self, score_funct):
        while (len(self.todo)):
            solution = self.todo.pop()
            self.done.append((score_funct(solution), solution))

class MultithreadedEvolutionaryOptimizer:
    def __init__(self, seed_sol : OptimizeableSolution, num_threads):
        self.seed = seed_sol
        self.max_learn_rate = 1
        self.generation_size = 100
        self.fudge_factor_calc = self.exp_fudge_factor
        self.anneal_rate = 0.5
        self.num_threads = num_threads
    
    def lerp_fudge_factor(self, cur_epoch, last_epoch):
        perc = (last_epoch - cur_epoch) / last_epoch
        return perc * self.max_learn_rate
    
    def exp_fudge_factor(self, cur_epoch, last_epoch):
        return math.exp(-self.anneal_rate * (cur_epoch))
    
    def train(self, score, epochs, print_interval=10, random_first_gen=True):
        print("Beginning training...")

        generation_batch_size = math.ceil(self.generation_size / self.num_threads)

        parents = []
        if (not random_first_gen):
            parents = [self.seed.fudgeSolution(0), self.seed.fudgeSolution(0)] # copy seed solution

        best_scoring_individual = None
        
        generation = []
        for c_ep in range(epochs):
            if ((c_ep == 0) and random_first_gen):
                for i in range(self.generation_size):
                    generation.append(self.seed.fudgeSolution(0).getRandomSolution())
            else:
                generation = parents[0].makeBabies(parents[1], self.fudge_factor_calc(c_ep, epochs), 
                                                self.generation_size, True)
            
            batches = [] # devide scoring into batches and assign each to a thread
            worker_threads = []
            for i in range(self.num_threads):
                cur_batch = GenerationBatch(generation, generation_batch_size)
                batches.append(cur_batch)
                cur_thread = threading.Thread(target=cur_batch.score_all, args=[score])
                worker_threads.append(cur_thread)
                cur_thread.start()

            assert(len(generation) == 0) # assume all the individuals have been added to a batch

            for thread in worker_threads: # wait for all the threads to finish scoring
                thread.join()
            
            scored = [] # join together all the results
            for batch in batches:
                batch : GenerationBatch
                batch.purge(scored)

            
            scored.sort(key=(lambda pair : pair[0]), reverse=True)
            parents = [scored[0][1], scored[1][1]] # get the actual models
                
            top_performance = scored[0][0] # get the highest score out of the table
            best_scoring_individual = scored[0][1] # get the best individual

            if (c_ep % print_interval == 0):
                print("\tFinished epoch " + str(c_ep) + " out of " + str(epochs) 
                      + " : SCORE (" + str(top_performance) + ")")
        
        print("TRAINING COMPLETE: Best = " + str(score(best_scoring_individual)))
        return best_scoring_individual






