from sly import Lexer

class SblLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, BOOLEAN, STRING, LIST, TUPLE,
                IN, CON, TUPLEINDEX,
               ID, WHILE, IF, ELSE, PRINT, LISTINDEX,
               PLUS, MINUS, TIMES, DIVIDE, EXPONENTIAL, ASSIGN,
               DIV, MODULUS, ANDALSO, ORELSE, NOT,
               EQ, LT, LE, GT, GE, NE,
               }

    literals = {'(',')', '{', '}', ';', ',', '[', ']'}

    # String containing ignored characters
    ignore = ' \t'


    @_(r'\([^\)]*\,+\)')
    def TUPLE(self, t):
        t.value = eval(str(t.value))
        return t
    
    # @_(r'\[\d+\]')
    # def LISTINDEX(self, t):
    #     t.value = eval(str(t.value)[1:-1])
    #     return t
    @_(r'\#\d+')
    def TUPLEINDEX(self, t):
        k = str(t.value)
        t.value = int(k[1:])
        return t


    @_(r'\[[^\]]*\]')
    def LIST(self, t):
        t.value = eval(str(t.value))
        return t

    # @_(r'[+-]?([0-9]*[.])?[0-9]+')
    @_(r'-?[\d.]+(?:e-?\d+)?')
    def NUMBER(self, t):
        try:
            t.value = int(str(t.value))
        except:
            t.value = float(str(t.value))

        return t

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    EXPONENTIAL = r'\*\*'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    DIV     = r'div'
    MODULUS = r'mod'
    IN      = r'in'
    CON     = r'::'
    # TUPLEINDEX = r'#'
    
    EQ      = r'=='
    ASSIGN  = r'='
    NE      = r'<>'
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    
    
    ANDALSO = r'andalso'
    ORELSE  = r'orelse'
    NOT     = r'not'
    
    @_(r'(True|False)')
    def BOOLEAN(self, t):
        if t.value == "False":
            t.value = False
        else:
            t.value = True
        return t

    
    # @_(r'\"(\\.|[^"\\])*\"')
    @_(r"['\"](.*?)['\"]")
    def STRING(self, t):
        t.value = str(eval(t.value))
        return t

        
    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    data = '''
{

}
'''
    lexer = SblLexer()
    for tok in lexer.tokenize(data):
        print(tok)