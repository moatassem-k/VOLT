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
    symbol_tilde    = '~'
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

    def tokenize(self):
        ...

    def peek(self, offset = 0):
        index = 0
        if (index := self.idx + offset) >= self.len:
            return None
        return self.src[index]

    def peek_at(self, idx):
        if idx >= self.len:
            return None
        return self.src[idx]

    def peek_until(self, r_idx):
        if r_idx >= self.len:
            return None
        return self.src[self.idx : r_idx]

    def peek_and_check_match(self, check_fn, offset = 0):
        c = self.peek(offset)
        if c and check_fn(c):
            return c
        return None

    def consume(self, count = 1):
        self.idx += count
        return self.src[self.idx - count : self.idx]

    def consume_until(self, r_idx):
        l_idx = self.idx
        self.idx = r_idx
        return self.src[l_idx : r_idx]

    def skip_whitespace(self):
        c = self.src[self.idx]
        if c.isspace():
            if c == '\n':
                self.row += 1
                self.col = 1
            elif c == ' ':
                self.col += 1
            self.idx += 1
        return None

    def match_symbol(self):
        for t_name, t_type in vars(TokenType).items():
            if t_name.startswith('symbol_') and self.peek() == t_type.value:
                self.col += 1
                return Token(t_type, self.consume(), self.row, self.col)
        else:
            return None
        
    def match_literal(self):
        for t_name, t_type in vars(TokenType).items():
            if t_name.startswith('lit_'):
                ...

    def match_keyword_ident(self):
        if self.peek().isalpha() or self.peek() == '_':
            print('starter match:{}'.format(self.peek()))
            r_idx = self.idx + 1
            while r_idx < self.len and \
                (self.peek_at(r_idx).isalnum() or self.peek_at(r_idx) == '_'):
                r_idx += 1
            print(r_idx)
            for t_name, t_type in vars(TokenType).items():
                if t_name.startswith('keyword_'):
                    if self.peek_until(r_idx) == t_type.value:
                        count = r_idx - self.idx
                        tok = Token(t_type, self.consume_until(r_idx), self.row, self.col)
                        self.col += count
                        return tok

            count = r_idx - self.idx
            print('count: {}'.format(count))
            tok = Token(TokenType.ident, self.consume_until(r_idx), self.row, self.col)
            self.col += count
            return tok
        else:
            return None
        

if __name__ == '__main__':
    input_string = ''
    with open('src/test.volt') as file:
         input_string = file.read()
    t = Tokenizer(input_string)