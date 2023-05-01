from lark import Lark, Transformer, v_args
from logic import *

class SentenceTransformer(Transformer):
    def symbol(self, name):
        return Symbol(name[0].value)

    def negation(self, args):
        return Negation(args[0])

    def conjunction(self, args):
        return Conjunction(*args)

    def disjunction(self, args):
        return Disjunction(*args)

    def implication(self, args):
        return Implication(*args)

    def biconditional(self, args):
        return Biconditional(*args)

sentence_parser = Lark(r"""
    ?start: sentence
    ?sentence: symbol
        | "(" sentence ")"
        | negation
        | conjunction
        | disjunction
        | implication
        | biconditional
    negation: "~" sentence
    conjunction: sentence "&" sentence
    disjunction: sentence "||" sentence
    implication: sentence "=>" sentence
    biconditional: sentence "<=>" sentence
    symbol: /[a-z0-9_]+/
    %import common.WS
    %ignore WS
""", start='start', parser='lalr', transformer=SentenceTransformer())

def parse(sentence):
    return sentence_parser.parse(sentence)

def create_knowledge_base(sentences):
    parsed_sentences = []
    for sentence in sentences:
        # print(f"Before parsing: {sentence}")
        parsed_sentence = parse(sentence)
        # print(f"After parsing: {parsed_sentence}")
        parsed_sentences.append(parsed_sentence)
    
    # Ensure all parsed sentences are included in the final conjunction
    knowledge_base = Conjunction(*parsed_sentences)
    
    return knowledge_base


