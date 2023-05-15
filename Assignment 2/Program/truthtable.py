from itertools import product
from tabulate import tabulate
from typing import List, Union
from sentence_transformers import *
from logic import *

class TruthTable:
    def __init__(self, symbols, knowledgeBase, query):
        self.symbols = sorted(symbols)
    
        # If the knowledge base is a list, convert it into a conjunction
        if isinstance(knowledgeBase, list):
            self.knowledgeBase = Conjunction(*knowledgeBase)
        else:
            self.knowledgeBase = knowledgeBase

        self.query = self.parse(query) if isinstance(query, str) else query
        self.table = self.generate_table()
        self.count = 0


    def generate_table(self):
        combinations = list(product([True, False], repeat=len(self.symbols)))
        models = [{symbol: value for symbol, value in zip(self.symbols, combination)} for combination in combinations]
        evaluations = [[self.knowledgeBase.evaluate(model)] for model in models]
        return list(zip(models, evaluations))

    def check_facts(self):
        for model, evaluation in self.table:
            if all(evaluation) and self.query.evaluate(model):
                self.count += 1
        return False
    
    def brute_force_check(self):
        is_Valid = model_check(self.knowledgeBase, self.query)
        return is_Valid

    def get_entailed_symbols(self):
        self.check_facts()
        valid = self.brute_force_check()

        if self.count > 0 and valid:
            return f'YES: {self.count}'
        else:
            return f'NO {self.query} cannot be proven'
        
        
        
    def __str__(self):
        headers = [str(symbol) for symbol in self.symbols]
        headers += [str(self.knowledgeBase)] + [str(self.query)]

        rows = []
        for model, evaluations in self.table:
            row = [str(model[symbol]) for symbol in self.symbols]
            row += [str(evaluations[0])] + [str(self.query.evaluate(model))]
            rows.append(row)

        return tabulate(rows, headers, tablefmt='fancy_grid')