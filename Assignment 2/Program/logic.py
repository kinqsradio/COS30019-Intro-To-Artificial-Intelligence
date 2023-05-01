class Sentence:
    
    # Logical sentence
    def __init__(self, *args):
        self.args = args

    # Sub class implement
    def evaluate(self, model):
        pass
    
    # Sub class implement
    def symbols(self):
        return set()

class Symbol(Sentence):
    
    # Logical proposition with a specific truth value
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    # Evaluates the truth value in model
    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    # Return set of symbol
    def symbols(self):
        return {self.name}

class Negation(Sentence):
    # Negation = Not | Symbol ~
    # Logical Negation
    def __repr__(self):
        return f'~{self.args[0]}'

    # Evaluates the Negation value in model
    def evaluate(self, model):
        return not self.args[0].evaluate(model)

    # Return symbols in Negation
    def symbols(self):
        return self.args[0].symbols()

class Conjunction(Sentence):
    # Conjunction = And | Symbol &
    # Logical Conjunction
    def __repr__(self):
        return ' & '.join(str(arg) for arg in self.args)

    # Evaluates the Conjunction value in model
    def evaluate(self, model):
        return all(arg.evaluate(model) for arg in self.args)
    
    # Return symbols in Conjunction
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])

class Disjunction(Sentence):
    # Disjunction = Or | Symbol ||
    # Logical Disjunction
    def __repr__(self):
        return f'({self.args[0]} || {self.args[1]})'

    # Evaluates the Disjunction value in model
    def evaluate(self, model):
        return self.args[0].evaluate(model) or self.args[1].evaluate(model)

    # Return symbols in Disjunction
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])

class Implication(Sentence):
    # Symbol =>
    # Logical Implication
    def __repr__(self):
        return f'({self.args[0]} => {self.args[1]})'

    # Evaluates the Implication value in model
    def evaluate(self, model):
        return not self.args[0].evaluate(model) or self.args[1].evaluate(model)

    # Return symbols in Implication
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])

class Biconditional(Sentence):
    # Symbol <=>
    # Logical Bicondition
    def __repr__(self):
        return f'({self.args[0]} <=> {self.args[1]})'

    # Evaluates the Bicondition value in model
    def evaluate(self, model):
        return self.args[0].evaluate(model) == self.args[1].evaluate(model)

    # Return symbols in Bicondition
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # If model has an assignment for each symbol
        if not symbols:

            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())


def forward_chaining(knowledge, query):
    # Create a dictionary to hold the count of each symbol
    count = {s: 0 for s in knowledge.symbols()}

    # Create a dictionary to hold the inferred values of each symbol
    inferred = {s: False for s in knowledge.symbols()}

    # Initialize the agenda with known facts
    agenda = [s for s in knowledge if isinstance(s, Symbol) and s.known]

    # Loop until the agenda is empty
    while agenda:
        # Remove a symbol from the agenda
        p = agenda.pop()

        # If the symbol is the query, return True
        if p == query:
            return True

        # If the symbol is not already inferred, mark it as inferred and update the count of its supported sentences
        if not inferred[p]:
            inferred[p] = True
            for s in knowledge.sentences_containing_symbol(p):
                count[s] += 1

                # If all of the sentence's symbols have been inferred, add it to the agenda
                if count[s] == len(s.symbols()):
                    agenda.append(s)

    # If the query was not found, return False
    return False


def backward_chaining(KB, q):
    # Define a helper function to recursively evaluate each clause
    def evaluate(clause):
        # If the clause is a symbol, evaluate it
        if isinstance(clause, Symbol):
            return clause.known

        # If the clause is a negation, evaluate its argument
        elif isinstance(clause, Negation):
            return not evaluate(clause.args[0])

        # If the clause is a conjunction, evaluate its arguments
        elif isinstance(clause, Conjunction):
            return all(evaluate(arg) for arg in clause.args)

        # If the clause is a disjunction, evaluate its arguments
        elif isinstance(clause, Disjunction):
            return any(evaluate(arg) for arg in clause.args)

        # If the clause is an implication, evaluate its arguments
        elif isinstance(clause, Implication):
            return evaluate(clause.args[0]) <= evaluate(clause.args[1])

        # If the clause is a biconditional, evaluate its arguments
        elif isinstance(clause, Biconditional):
            return evaluate(clause.args[0]) == evaluate(clause.args[1])

    # Evaluate the query
    return evaluate(q)




