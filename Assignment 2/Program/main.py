from logic import *
from truthtable import *
from forward_chaining import *
from backward_chaining import *
from sentence_transformers import *
from Reader import *


'''Test Function'''
# Read File
filename = 'test_genericKB_proven.txt' 
# filename = 'test_genericKB_unproven.txt'
# filename = 'test.txt'
# filename = 'test1.txt'
# filename = 'test2.txt'
# filename = 'test3.txt'
# filename = 'test4.txt'
# filename = 'test5.txt'
# filename = 'test6.txt'
# filename = 'test7.txt'
# filename = 'test8.txt'

print(f'Debug filename: {filename}\n')

tell, query = read(filename)
print(f'Tell: {tell}')
print(f'Query/Ask: {query}\n')

# Extract symbol
symbols, sentences = extract_symbols_and_sentences(tell)
print(f'Symbols: {symbols}')
print(f'Sentence: {sentences}\n')


# Create a dictionary to hold Symbol instances
symbol_objects = {}

# Create a Symbol instance for each unique symbol and store it in the dictionary
for symbol in symbols:
    symbol_objects[symbol] = Symbol(symbol)

print(f'Debug symbol dict: {symbol_objects}')
print(f'Debug Length dict: {len(symbol_objects)}\n')

knowledge_base = create_knowledge_base(sentences) # Transform sentence into logical sentence
query_sentence = parse(query)

# Debug Arg Types
print(f'{knowledge_base.print_arg_types()}\n')


print(f'Debug knowledge: {knowledge_base}')
print(f'Debug query: {query_sentence}\n')

# Model Check
is_Valid = model_check(knowledge_base, query_sentence)
print(f'Model Check Result (True = Can be proven, else cannot): {model_check(knowledge_base, query_sentence)}\n')

print(is_Valid)

# Create a TruthTable instance
truth_table = TruthTable(symbols, knowledge_base, query_sentence)
entailed_symbols = truth_table.get_entailed_symbols()
print(entailed_symbols)

# Reverse string debug
print("Reversing")
kb_string = knowledge_base_to_string(knowledge_base)
print(f'String: {kb_string}')

knowledge_reversed = parse_knowledge_base(kb_string)
print(f'Knowledge Reversed: {knowledge_reversed}\n')


# Here are some expected result for debugging in test.txt
print(f'Here are some expected result for debugging in test.txt provided in this submission\n')
print(f'Result for case:\nKnowledge Base: {knowledge_base}\nQuery:{query}\n')
print('Expected Result:\nYES: 3')
print(f'Output:\n{entailed_symbols}')

fc = ForwardChaining(knowledge_base, query)
fc_result = fc.solve()
print('Expected Result:\nYES: a, b, p2, p3, p1, d')
print(f'Output:\n{fc_result}')

bc = BackwardChaining(knowledge_base, query)
bc_result = bc.solve()
print('Expected Result:\nYES: p2, p3, p1, d')
print(f'Output:\n{bc_result}\n')


# Actual Output Result if you want to look at the final output cleaner instead of debug
print(f'Results:\n')

print('Based on the extension, Truth Table are working perfectly with General KB.\n' +
      'It is not required FC and BC to work with General KB.\n' + 
      'We have combining check_facts and extension model_check that is\napplying brute-force to double check to make sure everything is appropritate.\n')

print(entailed_symbols)
print(fc_result)
print(bc_result)