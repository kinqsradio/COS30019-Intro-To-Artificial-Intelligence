from sentence_transformers import *

class BackwardChaining:
    def __init__(self, KB, goal):
        self.KB = KB
        self.goal = goal

    def __str__(self) -> str:
        pass
    
    def prove(self, removed, chain, goal):
        for conjunct in self.KB.conjuncts():
            if isinstance(conjunct, Symbol):
                if goal == str(conjunct):
                    chain.append(goal)
                    return True, chain
                
        removed.append(goal)

        for conjunct in self.KB.conjuncts():
            if isinstance(conjunct, Implication):
                if goal == self.KB.conjunct_conclusion(conjunct):
                    all_true = True
                    for subgoal in self.KB.conjunct_premise(conjunct):
                        if subgoal in chain:
                            continue
                        if subgoal in removed:
                            all_true = False
                            break
                        established, chain = self.prove(removed, chain, subgoal)
                        if not established:
                            all_true = False
                    if all_true:
                        chain.append(goal)
                        return True, chain
        return False, chain

    def bc_entails(self):
        return self.prove([], [], self.goal) if self.goal not in (conjunct for conjunct in self.KB.conjuncts() if isinstance(conjunct, Symbol)) else (True, [self.goal])


    def solve(self):
        solution_found, chain = self.bc_entails()
        return "YES: " + ', '.join(chain) if solution_found else "NO"
