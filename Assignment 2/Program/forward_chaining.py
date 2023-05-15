from sentence_transformers import *

class ForwardChaining:
    def __init__(self, KB, query):
        self.KB = KB
        self.query = query

    def __str__(self) -> str:
        pass

    def fc_entails(self):
        chain = [] # initialize an array to keep track of the result of forward chaining
        # initialize the count dictionary
        """ 
        Count is a dictionary that keeps count of the number of premises of each clause
        """
        count = {}
        for conjunct in self.KB.conjuncts():
            if isinstance(conjunct, Implication):
                count[conjunct] = len(self.KB.conjunct_premise(conjunct))
        agenda = [str(symbol) for symbol in self.KB.conjuncts() if isinstance(symbol, Symbol) == True]
        inferred = {symbol : False for symbol in self.KB.symbols()}
        while agenda:
            p = agenda.pop(0)
            chain.append(p)
            if p == self.query:
                # print("true")
                # chain.append(self.query)
                return True, chain
            if inferred[p] == False:
                inferred[p] = True
                for conjunct in self.KB.conjuncts():
                    if isinstance(conjunct, Implication):
                        if p in self.KB.conjunct_premise(conjunct):
                            count[conjunct] -= 1
                            if count[conjunct] == 0:
                                agenda.append(self.KB.conjunct_conclusion(conjunct))
        # print("False")
        return False, []
    
    def solve(self):
        solution_found, chain = self.fc_entails()
        return "YES: " + ', '.join(chain) if solution_found else "NO"