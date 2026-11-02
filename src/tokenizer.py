from enum import Enum, auto
import re

class TokenType(Enum):
    keyword_if      = 'if'
    keyword_else    = 'else'
    keyword_return  = 'return'
    keyword_exit    = 'exit'

    symbol_dot      = '.'
    symbol_comma    = ','
    symbol_semi     = ';'
    symbol_colon    = ':'
    symbol_plus     = '+'
    symbol_minus    = '-'
    symbol_star     = '*'
    symbol_equal    = '='
    symbol_l_paren  = '('
    symbol_r_paren  = ')'
    symbol_l_curly  = '{'
    symbol_r_curly  = '}'
    symbol_l_angle  = '<'
    symbol_r_angle  = '>'
    symbol_f_slash  = '/'
    symbol_b_slash  ='\\'
    symbol_l_square = '['
    symbol_r_square = ']'

    ident           = auto()

    lit_int         = auto()
    lit_float       = auto()
    lit_char        = auto()
    lit_str         = auto()

    # special_eof     = auto()


class Token:
	def __init__(self, type, value = None, row = 0, col = 0):
		self.type  = type
		self.value = value
		self.row   = row
		self.col   = col

	def __repr__(self):
		value = f"[{self.value}]" if self.value else ''
		return f"{self.type.name}({self.row}, {self.col}){value}"


class Tokenizer:
    def __init__(self, input_string):
        self.src = input_string
        self.row = 1
        self.col = 1
        self.idx = 0
        self.len = len(self.src)

    def peek(self, offset = 0):
        index = 0
        if (index := self.idx + offset) >= self.len:
            return None
        return self.src[index]

    def peek_with_type(self, check_fn, offset = 0):
        c = self.peek(offset)
        if c and check_fn(c):
            return c
        return None

    def consume(self, count = 0):
        if count > 0:
            self.idx += count
            return self.src[self.idx-count : self.idx]
        else:
            self.idx += 1
            return self.src[self.idx - 1]

    def match_symbol(self):
        for t_name, t_type in vars(TokenType).items():
            if t_name.startswith('symbol_'):
                if self.src[self.idx] == t_type.value:
                    return Token(t_type, t_type.value)
        else:
            return None
        
    def match_literal(self):
        pass
    def match_keyword(self):
        pass

if __name__ == '__main__':
    t = Tokenizer('+-*/=\\')
    print(t.match_symbol())
    t.consume()
    print(t.match_symbol())
    t.consume()
    print(t.match_symbol())
    t.consume()
    print(t.match_symbol())
    t.consume()
    print(t.match_symbol())
    t.consume()
    print(t.match_symbol())