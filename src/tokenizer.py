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

class LitPatterns(Enum):
    pattern_int   = r'\d+'
    pattern_float = r'\d+\.\d+(?:[eE][+-]?\d+)?'
    pattern_char  = r"'(?:\\.|[^'\\])'"
    pattern_str   = r'"(?:\\.|[^"\\])*"'

KEYWORDS = {
    "if"     : TokenType.keyword_if,
    "else"   : TokenType.keyword_else,
    "return" : TokenType.keyword_return,
    "exit"   : TokenType.keyword_exit,
}

LITERAL_PATTERNS = {
    TokenType.lit_float : re.compile(LitPatterns.pattern_float.value),
    TokenType.lit_int   : re.compile(LitPatterns.pattern_int.value),
    TokenType.lit_char  : re.compile(LitPatterns.pattern_char.value),
    TokenType.lit_str   : re.compile(LitPatterns.pattern_str.value),
}

class Token:
	def __init__(self, type, value = None, row = 0, col = 0):
		self.type  = type
		self.value = value
		self.row   = row
		self.col   = col

	def __repr__(self):
		value = f"[{self.value}]" if self.value is not None else ''
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
        index = self.idx + offset
        if index >= self.len:
            return None
        return self.src[index]

    def peek_at(self, idx):
        if idx >= self.len:
            return None
        return self.src[idx]

    def peek_until(self, r_idx):
        return self.src[self.idx:r_idx]

    def advance_position(self, text):
        lines = text.split('\n')

        if len(lines) > 1:
            self.row += len(lines) - 1
            self.col = len(lines[-1]) + 1
        else:
            self.col += len(text)

    def consume(self, count=1):
        text = self.src[self.idx:self.idx + count]
        self.idx += len(text)
        self.advance_position(text)
        return text

    def consume_until(self, r_idx):
        return self.consume(r_idx - self.idx)

    def skip_whitespace(self):
        if self.peek():
            self.consume()
            return True

        return False

    def make_token(self, token_type, value, row, col):
        return Token(token_type, value, row, col)

    def match_symbol(self):
        for t_type in TokenType:
            if t_type.name.startswith('symbol_') and self.peek() == t_type.value:
                row, col = self.row, self.col
                value = self.consume()

                return self.make_token(t_type, value, row, col)
        else:
            return None
        
    def match_literal(self):
        for t_type, pattern in LITERAL_PATTERNS.items():
            if match := pattern.match(self.src, self.idx):
                text = match.group(0)
                row, col = self.row, self.col

                value = self.consume(len(text))
                return Token(t_type, value, row, col)

        return None

    def match_keyword_ident(self):
        if self.peek().isalpha() or self.peek() == '_':
            r_idx = self.idx + 1
            while r_idx < self.len and \
                (self.peek_at(r_idx).isalnum() or self.peek_at(r_idx) == '_'):
                r_idx += 1

            word = self.peek_until(r_idx)
            t_type = KEYWORDS.get(word, TokenType.ident)

            row, col = self.row, self.col
            value = self.consume_until(r_idx)

            return self.make_token(t_type, value, row, col)
        else:
            return None
        

if __name__ == '__main__':
    input_string = ''
    with open('src/test.volt') as file:
         input_string = file.read()
    t = Tokenizer(input_string)

    # print(TokenType.symbol_dot)
    # print(TokenType.symbol_dot.name)
    # print(TokenType.symbol_dot.value)

    print(t.match_keyword_ident())
    t.skip_whitespace()
    print(t.match_literal())
    t.skip_whitespace()
    print(t.match_symbol())
    t.skip_whitespace()
    print(t.match_keyword_ident())
    t.skip_whitespace()
    print(t.match_literal())
    t.skip_whitespace()
    print(t.match_symbol())

    # lit = "\"string literal\""
    # lit = "123.456"

    # for t_type, pattern in LITERAL_PATTERNS.items():
    #     if match := pattern.match(lit, 0):
    #         text = match.group(0)
    #         token = Tokenizer.make_token(None,
    #                                      t_type,
    #                                      text,
    #                                      0, 0)
    #         print(token)
            