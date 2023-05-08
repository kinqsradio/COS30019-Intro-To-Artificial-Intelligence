from logic import *
from ForwardChaining import *
from BackwardChaining import *
from truthtable import *
from sentence_transformers import *
import re


'''Read from file'''
def read(filename):
    with open(filename) as f:
        lines = [line.strip().lower().split(";") for line in f]
    flattened_lines = [item for sublist in lines for item in sublist]
    
    try:
        query_index = flattened_lines.index('ask')
    except ValueError:
        query_index = len(flattened_lines)

    tell = [x.replace(" ", "") for x in flattened_lines[:query_index] if x not in ["", "tell", "ask"]]
    query = flattened_lines[query_index + 1].replace(" ", "") if query_index + 1 < len(flattened_lines) else ''

    return tell, query  
    
'''Extract Symbol'''
# def extract_symbols(tell):
#     symbols = set()
#     for sentence in tell:
#         symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
#     return symbols

def extract_symbols_and_sentences(tell):
    symbols = set()
    sentences = []
    for sentence in tell:
        symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
        sentences.append(sentence)
    return symbols, sentences


def parse_sentences(symbols, sentences):
    sentence_objects = []
    
    for sentence in sentences:
        # Replace logical operators with Python operators
        sentence = sentence.replace('<=>', 'Biconditional')\
                           .replace('=>', 'Implication')\
                           .replace('~', 'Negation')\
                           .replace('&', 'Conjunction')\
                           .replace('||', 'Disjunction')
                           
        # Replace symbols with Symbol instances
        for symbol in sorted(symbols, key=len, reverse=True):  # sort symbols by length in descending order
            pattern = r'\b' + symbol + r'\b'  # match the symbol as a whole word
            replacement = f"Symbol('{symbol}')"
            sentence = re.sub(pattern, replacement, sentence)

        sentence_objects.append(eval(sentence))

    return Conjunction(*sentence_objects)

'''Test Function'''
# Read File
# filename = 'test.txt'
# filename = 'test_genericKB.txt' 
# filename = 'test_HornKB.txt'
# filename = 'test_unproven.txt'
# filename = 'test1.txt'
filename = 'test2.txt'
# filename = 'test3.txt'
# filename = 'test4.txt'
# filename = 'test5.txt'
# filename = 'test6.txt'

print(f'\nDebug filename: {filename}\n')

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

knowledge_base.print_arg_types()


print(f'\nDebug knowledge: {knowledge_base}')
print(f'Debug query: {query_sentence}\n')

# Model Check
is_Valid = model_check(knowledge_base, query_sentence)
print("Model Check Result (True = Can be proven, else cannot):", model_check(knowledge_base, query_sentence))

# Create a TruthTable instance
truth_table = TruthTable(symbols, knowledge_base, query_sentence)

if is_Valid:
    entailed_symbols = truth_table.get_entailed_symbols()
else:
    entailed_symbols = f'NO {query_sentence} cannot be proven'

print(f'Truth Table Result: {entailed_symbols}\n')
    
# print(truth_table)

'''Reverse Checking:'''
kb_string = knowledge_base_to_string(knowledge_base)
print(f'Current KB: {kb_string}')
rv_knowledge = parse_knowledge_base(kb_string)
print(f'Reverse checking: {rv_knowledge}\n')


kb = KnowledgeBase()
for sentence in sentences:
    kb.add_sentence(sentence)
    
bc = BackwardChaining(kb)
query = Symbol('d')

result = bc.solve(query)
print(f"Query: {query}")
print(f"Result: {result}")
