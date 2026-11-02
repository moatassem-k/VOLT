from enum import Enum, auto

class TokenType(Enum):
    keyword_if      = auto()
    keyword_return  = auto()
    keyword_exit    = auto()

    symbol_dot      = auto()
    symbol_comma    = auto()
    symbol_semi     = auto()
    symbol_colon    = auto()
    symbol_plus     = auto()
    symbol_minus    = auto()
    symbol_star     = auto()
    symbol_equal    = auto()
    symbol_f_slash  = auto()
    symbol_b_slash  = auto()
    symbol_l_paren  = auto()
    symbol_r_paren  = auto()
    symbol_l_curly  = auto()
    symbol_r_curly  = auto()
    symbol_l_angle  = auto()
    symbol_r_angle  = auto()
    symbol_l_square = auto()
    symbol_r_square = auto()

    ident           = auto()

    lit_int         = auto()
    lit_float       = auto()
    lit_char        = auto()
    lit_str         = auto()

    special_eof     = auto()


class Token:
	def __init__(self, type, value = None, row = 0, col = 0):
		self.type = type
		self.value = value
		self.row = row
		self.col = col

	def __repr__(self):
		value = f"[{self.value}]" if self.value else ''
		return f"{self.type.name}({self.row}, {self.col}){value}"