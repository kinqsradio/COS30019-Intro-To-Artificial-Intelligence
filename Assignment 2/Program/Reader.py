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
def extract_symbols_and_sentences(tell):
    symbols = set()
    sentences = []
    for sentence in tell:
        symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
        sentences.append(sentence)
    return symbols, sentences