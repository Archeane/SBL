from sly import Parser
from sbllexer import SblLexer

class SblParser(Parser):
    # Get the token list from the lexer (required)
    tokens = SblLexer.tokens

    precedence = (
    #    ('nonassoc', LT, GT, LE, GE, NE, EQ),
       ('left', ORELSE),
       ('left', ANDALSO),
       ('left', NOT),
       ('left', LT, GT, LE, GE, NE, EQ),
       ('right', CON),
       ('left', IN),
       ('left', PLUS, MINUS),
       ('left', TIMES, DIVIDE, DIV, MODULUS), 
       ('right', EXPONENTIAL),
       ('left', TUPLEINDEX),
    )

    def __init__(self):
        self.names = {}
        self.stack = []
    

    @_('PRINT "(" statement ")"')
    def statement(self, p):
        print(p.statement)
        return

    # @_('LBRAC expr RBRAC')
    # def list(self, p):
    #     return [p.expr]

    # @_('LBRAC expr "," exprlist RBRAC')
    # def list(self, p):
    #     return [p.expr] + p.exprlist

    # @_('expr "," exprlist')
    # def exprlist(self, p):
    #     p.exprlist.insert(0, p.expr)
    #     return p.exprlist 
    
    # @_('expr')
    # def exprlist(self, p):
    #     return [ p.expr ]

    # list =====

    # @_('"[" elements "]"')
    # def array(self, p):
    #     return p.elements
    # @_('expr')
    # def elements(self, p):
    #     return [p.expr]

    # @_('expr "," elements')
    # def elements(self, p):
    #     return [p.expr] + p.elements

    # @_('array PLUS array')
    # def array(self, p):
    #     return p.array0 + p.array1

    # tuple

    # arthmetic
    @_('expr')
    def statement(self, p):
        return p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        if p.expr1 == 0:
            print("SEMANTIC ERROR: division by zero")
            raise EOFError
        return p.expr0 / p.expr1

    @_('expr DIV expr')
    def expr(self, p):
        return int(p.expr0 / p.expr1)

    @_('expr MODULUS expr')
    def expr(self, p):
        return p.expr0 % p.expr1
    
    @_('expr EXPONENTIAL expr')
    def expr(self, p):
        return p.expr0 ** p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr LT expr')
    def expr(self, p):
        return p.expr0 < p.expr1

    @_('expr GE expr')
    def expr(self, p):
        return p.expr0 >= p.expr1

    @_('expr LE expr')
    def expr(self, p):
        return p.expr0 <= p.expr1

    @_('expr NE expr')
    def expr(self, p):
        return p.expr0 != p.expr1

    @_('expr EQ expr')
    def expr(self, p):
        return p.expr0 == p.expr1

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    # bool
    @_('bool')
    def statement(self, p):
        return p.bool

    @_('"(" bool ")"')
    def bool(self, p):
        return p.bool
    
    @_('NOT bool')
    def bool(self, p):
        return not(p.bool)

    @_('bool ANDALSO bool')
    def bool(self, p):
        return p.bool0 and p.bool1
    
    @_('bool ORELSE bool')
    def bool(self, p):
        return p.bool0 or p.bool1

    @_('BOOLEAN')
    def bool(self, p):
        return p.BOOLEAN
    
    # string
    @_('string')
    def statement(self, p):
        return p.string

    @_('string PLUS string')
    def string(self, p):
        return p.string0 + p.string1

    @_('string GT string')
    def string(self, p):
        return p.string0 > p.string1

    @_('string LT string')
    def string(self, p):
        return p.string0 < p.string1

    @_('string GE string')
    def string(self, p):
        return p.string0 >= p.string1

    @_('string LE string')
    def string(self, p):
        return p.string0 <= p.string1

    @_('string NE string')
    def string(self, p):
        return p.string0 != p.string1

    @_('string EQ string')
    def string(self, p):
        return p.string0 == p.string1

    @_('string IN string')
    def string(self, p):
        return p.string0 in p.string1

    @_('STRING')
    def string(self, p):
        return p.STRING

    # tuple
    @_('tuple')
    def statement(self, p):
        return p.tuple

    @_('TUPLEINDEX tuple')
    def tuple(self, p):
        index = p.TUPLEINDEX
        if index > len(p.tuple):
            print("SEMANTIC ERROR: index exceeds tuple length")
            raise EOFError
        else:
            return p.tuple[index-1]

    @_('TUPLE')
    def tuple(self, p):
        return p.TUPLE

    # list

    # @_('"[" elements "]"')
    # def statement(self, p):
    #     return p.elements
    
    # @_("statement")
    # def elements(self, p):
    #     return [p.statement]

    # @_('statement "," elements')
    # def elements(self, p):
    #     return [p.statement] + p.elements


    @_('elements')
    def statement(self, p):
        return p.elements

    @_('statement "," elements')
    def elements(self, p):
        return [p.statement] + p.elements

    @_('elements PLUS elements')
    def elements(self, p):
        return p.elements0 + p.elements1

    @_('statement IN elements')
    def elements(self, p):
        return p.statement in p.elements

    @_('statement CON elements')
    def elements(self, p):
        return [p.statement] + p.elements

    @_('elements elements')
    def elements(self, p):
        if(len(p.elements1) > 1):
            print(f"Syntax Error at token {p.elements1}: list indices must be integers, not tuple")
            raise EOFError
        if type(p.elements1[0]) != int:
            print(f"Syntax Error: index must be integer")
            raise EOFError
        if p.elements1[0] >= len(p.elements0):
            print(f"Semantic Error: index out of bounds")
            raise EOFError
        return p.elements0[p.elements1[0]]

    @_('string elements')
    def string(self, p):
        if len(p.elements) > 1:
            print(f"Syntax Error at token {p.elements1}: string indices must be integers")
            raise EOFError
        if type(p.elements[0]) != int:
            print(f"Syntax Error at token {p.elements}: string indices must be integers")
            raise EOFError
        if p.elements[0] >= len(p.string):
            print(f"Semantic Error: index out of bounds")
            raise EOFError
        return p.string[p.elements[0]]
    
    @_('LIST')
    def elements(self, p):
        return p.LIST


    @_('statements')
    def block(self, p):
        return p.elements

    @_('statement ";" statements')
    def statements(self, p):
        self.stack.append(p.statement)
        return p.statements
    
    @_('"{" BLOCK "}"')
    def statements(self, p):
        return p.BLOCk

    def error(self, p):
        print("Syntax error at token %s" % str(p))
        raise EOFError

if __name__ == '__main__':
    lexer = SblLexer()
    parser = SblParser()

    while True:
        try:
            text = input('sbl > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break