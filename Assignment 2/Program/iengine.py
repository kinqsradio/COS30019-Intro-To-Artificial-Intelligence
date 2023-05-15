import sys
from Reader import *
from sentence_transformers import *
from logic import *
from truthtable import *
from backward_chaining import *
from forward_chaining import *

def main(filename):
    # Read File
    tell, query = read(filename)

    # Extract symbol
    symbols, sentences = extract_symbols_and_sentences(tell)

    # Create a dictionary to hold Symbol instances
    symbol_objects = {}

    # Create a Symbol instance for each unique symbol and store it in the dictionary
    for symbol in symbols:
        symbol_objects[symbol] = Symbol(symbol)

    knowledge_base = create_knowledge_base(sentences) # Transform sentence into logical sentence
    query_sentence = parse(query)

    # Model Check
    is_Valid = model_check(knowledge_base, query_sentence)

    # Create a TruthTable instance
    truth_table = TruthTable(symbols, knowledge_base, query_sentence)
    entailed_symbols = truth_table.get_entailed_symbols()

    # Forward Chaining
    fc = ForwardChaining(knowledge_base, query)
    fc_result = fc.solve()

    # Backward Chaining
    bc = BackwardChaining(knowledge_base, query)
    bc_result = bc.solve()

    # Output the results
    print('\nResults:')
    print(entailed_symbols)
    print(fc_result)
    print(bc_result)
    
    print(truth_table)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('You need to provide a filename as an argument.')
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
