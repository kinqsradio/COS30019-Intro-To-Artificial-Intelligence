import re
from lark import Lark, Transformer, v_args
from truthtable import *
from logic import *
from typing import List, Union
from lark.exceptions import ParseError


class SentenceTransformer(Transformer):
    def symbol(self, args):
        # print(f"symbol args: {args}")
        return Symbol(args[0].value)
    
    def atom(self, args):
        return args[0]

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

'''Version 1 - Works But Wrong Format 
    Example After debug:
    Before Parsing: b&e => f
    After Parsing: b & (e => f)
    Expected: ((b & e) => f)'''
# sentence_parser = Lark(r"""
#     ?start: sentence
#     ?sentence: symbol
#         | "(" sentence ")"
#         | negation
#         | conjunction
#         | disjunction
#         | implication
#         | biconditional
#     negation: "~" sentence
#     conjunction: sentence "&" sentence
#     disjunction: sentence "||" sentence
#     implication: sentence "=>" sentence
#     biconditional: sentence "<=>" sentence
#     symbol: /[a-z0-9_]+/
#     %import common.WS
#     %ignore WS
# """, start='start', parser='lalr', transformer=SentenceTransformer())

'''Version 2 - Works but a little bit wrong when having negation
    in front of each symbols
    Example After Debug Knowledge:
    Debug knowledge: (~p2 => ~p3) & (~p3 => ~p1) & 
    (~c => ~e) & (~b & ~e => ~f) & (~f & ~g => ~h) & 
    (~p1 => ~d) & (~p1 & ~p3 => ~c) & ~a & ~b & ~p2'''
    
# sentence_parser = Lark(r"""
#     ?start: biconditional
#     ?biconditional: implication
#                   | biconditional "<=>" implication
#     ?implication: conjunction
#                 | implication "=>" conjunction
#     ?conjunction: disjunction
#                 | conjunction "&" disjunction
#     ?disjunction: negation
#                 | disjunction "||" negation
#     negation: "~" atom
#             | atom
#     atom: symbol
#         | "(" biconditional ")"
#     symbol: /[a-z0-9_]+/
#     %import common.WS
#     %ignore WS
# """, start='start', parser='lalr', transformer=SentenceTransformer())


'''First Best - Improving and Fix from Version 2, works with either generic and horn'''

sentence_parser = Lark(r"""
    ?start: biconditional
    ?biconditional: implication
                  | biconditional "<=>" implication
    ?implication: conjunction
                | implication "=>" conjunction
    ?conjunction: disjunction
                | conjunction "&" disjunction
    ?disjunction: negation
                | disjunction "||" negation
    ?negation: "~" atom -> negation
            | atom
    atom: symbol
        | "(" biconditional ")"
    symbol: /[a-z0-9_]+/
    %import common.WS
    %ignore WS
""", start='start', parser='lalr', transformer=SentenceTransformer())


'''Second Best as this one shows error on generic form'''

# sentence_parser = Lark(r"""
#     ?start: biconditional
#     ?biconditional: implication
#                   | biconditional "<=>" implication
#     ?implication: conjunction
#                 | implication "=>" conjunction
#     ?conjunction: disjunction
#                 | conjunction "&" disjunction
#     ?disjunction: atom
#                 | disjunction "||" atom
#     atom: symbol
#         | parens
#     parens: "(" biconditional ")"
#     symbol: /[a-z0-9_]+/
#     negation: "~" atom
#     %import common.WS
#     %ignore WS
# """, start='start', parser='lalr', transformer=SentenceTransformer())

'''End'''

def parse(sentence):
    return sentence_parser.parse(sentence)

def parse_knowledge_base(kb_string):
    kb_list = []

    # Split the string into individual statements
    statements = re.split(r'\s*&\s*', kb_string)

    for statement in statements:
        # Implication
        if "=>" in statement:
            premise, conclusion = statement.strip("()").split(" => ")

            # Check if premise is a Conjunction
            if " & " in premise:
                conjuncts = [Symbol(s.strip()) for s in premise.split(" & ")]
                kb_list.append(Implication(Conjunction(*conjuncts), Symbol(conclusion)))
            else:
                kb_list.append(Implication(Symbol(premise), Symbol(conclusion)))

        # Symbol
        else:
            kb_list.append(Symbol(statement))

    return kb_list


def knowledge_base_to_string(kb_list):
    kb_string = ""

    for element in kb_list.args:
        # Implication
        if isinstance(element, Implication):
            premise = element.args[0]
            conclusion = element.args[1]

            # Check if the premise is a Conjunction
            if isinstance(premise, Conjunction):
                conjuncts = " & ".join(str(arg) for arg in premise.args)
                kb_string += f"({conjuncts} => {conclusion})"
            else:
                kb_string += f"({premise} => {conclusion})"

        # Symbol
        else:
            kb_string += str(element)

        kb_string += " & "

    # Remove the trailing " & " and return the string
    return kb_string[:-3]


def create_knowledge_base(sentences):
    parsed_sentences = []
    for sentence in sentences:
        print(f"Before parsing: {sentence}")
        parsed_sentence = parse(sentence.strip())
        print(f"After parsing: {parsed_sentence}")
        parsed_sentences.append(parsed_sentence)
    knowledge_base = Conjunction(*parsed_sentences)

    return knowledge_base


# sentences = ['p2=>p3', 'p3=>p1', 'c=>e', 'b&e=>f', 'f&g=>h', 'p1=>d', 'p1&p3=>c', 'a', 'b', 'p2']
# knowledge_base = create_knowledge_base(sentences)
# print(knowledge_base)

# kb_string = knowledge_base_to_string(knowledge_base)
# print(kb_string)

# knowledge = parse_knowledge_base(kb_string)
# print(knowledge)
