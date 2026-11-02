from enum import Enum, auto
import re

class TokenType(Enum):
    keyword_if      = 'if'
    keyword_else    = 'else'
    keyword_return  = 'return'
    keyword_exit    = 'exit'
    keyword_logic_and  = 'AND'
    keyword_logic_or   = 'OR'
    keyword_logic_xor  = 'XOR'
    keyword_logic_not  = 'NOT'
    keyword_logic_nand = 'NAND'
    keyword_logic_xnor = 'XNOR'

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

    symbol_ne       = '!='
    symbol_eq_eq    = '=='
    symbol_lt_eq    = '<='
    symbol_gt_eq    = '>='

    ident           = auto()

    lit_int         = auto()
    lit_float       = auto()
    lit_char        = auto()
    lit_str         = auto()

    special_eof     = auto()

KEYWORDS = {
    t_type.value: t_type
    for t_type in TokenType
    if t_type.name.startswith('keyword_')
}

SYMBOLS = {
    t_type.value: t_type
    for t_type in TokenType
    if t_type.name.startswith('symbol_')
}

MAX_SYMBOL_LENGTH = max(map(len, SYMBOLS))

class LitPatterns(Enum):
    pattern_float = r'\d+\.\d*(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    pattern_int   = r'\d+'
    pattern_char = r"'(?:\\.|[^'\\\n])'"
    pattern_str  = r'"(?:\\.|[^"\\\n])*"'

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
        tokens = []
        
        while self.idx < self.len:
            if self.skip_whitespace() or self.skip_comment():
                continue

            if self.idx >= self.len:
                break

            token = (
                self.match_literal()
                or self.match_keyword_ident()
                or self.match_symbol()
            )

            if token is None:
                raise SyntaxError(
                    f"Unexpected character {self.peek()!r} "
                    f"at {self.row}:{self.col}"
                )

            tokens.append(token)
        tokens.append(Token(TokenType.special_eof,
                            None,
                            self.row, self.col))
        return tokens

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
        if (c := self.peek()) is not None and c.isspace():
            self.consume()
            return True

        return False

    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            self.consume(2)

            while (c := self.peek()) is not None and c != '\n':
                self.consume()

            return True
        return False

    def make_token(self, token_type, value, row, col):
        return Token(token_type, value, row, col)

    def match_symbol(self):
        max_len = min(MAX_SYMBOL_LENGTH, self.len - self.idx)
        for length in range(max_len, 0, -1):
            symbol = self.peek_until(self.idx + length)

            if symbol in SYMBOLS:
                row, col = self.row, self.col

                return self.make_token(
                    SYMBOLS[symbol],
                    self.consume(length),
                    row, col)
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
        if (c := self.peek()) is not None and (c.isalpha() or c == '_'):
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

    for token in t.tokenize():
        print(token)

            