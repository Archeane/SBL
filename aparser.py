from sly import Lexer
from sly import Parser
import sys

class SemanticError(Exception):
    pass

class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class BooleanNode(Node):
    def __init__(self, v):
        if v == 'True':
            self.value = True
        elif v == 'False':
            self.value = False

    def evaluate(self):
        return self.value

class NumberNode(Node):
    def __init__(self, v):
        # if(isinstance(v, int)):
        #     self.value = int(v)
        # elif isinstance(v, float):
        #     self.value = float(v)
        if('.' in v or 'e' in v):
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value

    def setValue(self, value):
        self.value = value

class StringNode(Node):
    def __init__(self, v):
        self.v = v[1:len(v) - 1]
        # store the quote type?
    def evaluate(self):
        return self.v

class ListNode(Node):
    def __init__(self, elem):
        self.v = elem
    def prepend(self, elem):
        self.v = [elem] + self.v
    def evaluate(self):
        if self.v is not None:
            # return [self.v.evaluate()]
            temp = []
            for e in self.v:
                temp.append(e.evaluate())
            return temp
        else:
            return []

class IndexNode(Node):
    def __init__(self, l, v):
        self.listVal = l
        self.index = v
    def evaluate(self):
        if not (isinstance(self.listVal, ListNode) or isinstance(self.listVal, StringNode) 
            or isinstance(self.listVal, IndexNode)):
            raise SemanticError('SEMANTIC ERROR')
        if not isinstance(self.index.evaluate(), int):
            raise SemanticError('SEMANTIC ERROR')
        if self.index.evaluate() >= len(self.listVal.evaluate()):
            raise SemanticError('SEMANTIC ERROR')
        return self.listVal.evaluate()[self.index.evaluate()]

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def evaluate(self):
        if (self.op == '+'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 + val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 + val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 + val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 + val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 + val2
            elif isinstance(val1, list) and isinstance(val2, list):
                return val1 + val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == '-'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, int) and isinstance(val2, int):
                return val1 - val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 - val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 - val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 - val2
            else:
                raise SemanticError()
        elif (self.op == '*'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, int) and isinstance(val2, int):
                return val1 * val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 * val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 * val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 * val2
            else:
                raise SemanticError()
        elif (self.op == '/'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val2, int) or isinstance(val2, int) and val2 == 0:
                raise SemanticError("division by zero")
            if isinstance(val1, int) and isinstance(val2, int):
                return val1 / val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 / val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 / val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 / val2
            else:
                raise SemanticError()
        elif (self.op == 'div'):
            return self.left.evaluate() // self.right.evaluate()
        elif (self.op == 'mod'):
            return self.left.evaluate() % self.right.evaluate()
        elif (self.op == '<'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 < val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 < val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 < val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 < val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 < val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == '>'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 > val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 > val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 > val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 > val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 > val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == '=='):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 == val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 == val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 == val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 == val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 == val2
            else:
                raise SemanticError('SEMANTIC ERROR')

        elif (self.op == '<='):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 <= val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 <= val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 <= val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 <= val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 <= val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == '>='):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 >= val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 >= val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 >= val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 >= val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 >= val2
            else:
                raise SemanticError('SEMANTIC ERROR')
            
        elif (self.op == '<>'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 != val2
            elif isinstance(val1, int) and isinstance(val2, int):
                return val1 != val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 != val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 != val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 != val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == '**'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, int) and isinstance(val2, int):
                return val1 ** val2
            elif isinstance(val1, float) and isinstance(val2, int):
                return val1 ** val2
            elif isinstance(val1, int) and isinstance(val2, float):
                return val1 ** val2
            elif isinstance(val1, float) and isinstance(val2, float):
                return val1 ** val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == 'andalso'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, bool) and isinstance(val2, bool):
                return val1 and val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif (self.op == 'orelse'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, bool) and isinstance(val2, bool):
                return val1 or val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif self.op == 'in':
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val2, list) or (isinstance(val2, str) and isinstance(val1, str)):
                return val1 in val2
            else:
                raise SemanticError('SEMANTIC ERROR')
        elif self.op == '::':
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val2, list):
                return [val1] + self.right.evaluate()
            else:
                raise SemanticError('SEMANTIC ERROR')

class OneOp(Node):
    def __init__(self, op, v):
        self.op = op
        self.v = v

    def evaluate(self):
        if self.op == 'not':
            if not isinstance(self.v.evaluate(), bool):
                raise SemanticError("SEMANTIC ERROR")
            return not self.v.evaluate()
        elif self.op == '-':
            if not isinstance(self.v.evaluate(), (float, int)):
                raise SemanticError("SEMANTIC ERROR")
            return self.v.evaluate() * -1

class CSLNode(Node):
    def __init__(self, v1, v2):
        self.left = v1
        self.right = v2
    def appendElem(self, elem):
        self.v.append(elem)
    def evaluate(self):
        if isinstance(self.left, CSLNode):
            return self.left.evaluate() + [self.right.evaluate()]
        else:
            return [self.left.evaluate(), self.right.evaluate()]

class TupleNode(Node):
    def __init__(self, l):
        self.v = l
    def evaluate(self):
        return tuple(self.v.evaluate())

class IndexTupleNode(Node):
    def __init__(self, tup, ind):
        self.tup = tup
        self.index = ind
    def evaluate(self):
        if not((isinstance(self.tup, TupleNode) or isinstance(self.tup, VariableNode) or isinstance(self.tup, IndexNode))
         and isinstance(self.index.evaluate(), int)):
            raise SemanticError('SEMANTIC ERROR')
        if isinstance(self.index.evaluate(), int):
            if self.index.evaluate() >= len(self.tup.evaluate()):
                raise SemanticError('SEMANTIC ERROR')
            return self.tup.evaluate()[self.index.evaluate() - 1]

class PrintNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        print(self.value.evaluate())

class BlockNode(Node):
    def __init__(self,sl):
        self.statementList = sl

    def evaluate(self):
        if self.statementList is None:
            return
        for statement in self.statementList:
            statement.evaluate()

class IfNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def evaluate(self):
        if self.condition.evaluate():
            self.block.evaluate()

class IfElseNode(Node):
    def __init__(self, condition, ifblock, elseblock):
        self.condition = condition
        self.ifblock = ifblock
        self.elseblock = elseblock
    def evaluate(self):
        if self.condition.evaluate():
            self.ifblock.evaluate()
        else:
            self.elseblock.evaluate()

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def evaluate(self):
        while(self.condition.evaluate()):
            self.block.evaluate()

variables = {}

class VariableIndexNode(Node):
    def __init__(self, var, index):
        self.var = var
        self.index = index
    def evaluate(self):
        if not (isinstance(self.var, VariableNode) or isinstance(self.var, VariableIndexNode)):
            print(type(self.var))
            raise SemanticError('SEMANTIC ERROR')
        if not (isinstance(self.var.evaluate(), list) or isinstance(self.var.evaluate(), str)):
            raise SemanticError('SEMANTIC ERROR')
        if not isinstance(self.index.evaluate(), int):
            raise SemanticError('SEMANTIC ERROR')
        if self.index.evaluate() >= len(self.var.evaluate()):
            raise SemanticError('SEMANTIC ERROR')
        return self.var.evaluate()[self.index.evaluate()]

class AssignmentNode(Node):
    def __init__(self, var, val):
        self.var = var
        self.val = val
    def evaluate(self):
        if isinstance(self.var, VariableIndexNode):
            if isinstance(self.var.var, VariableNode):
                variables[self.var.var.name][self.var.index.evaluate()] = self.val.evaluate()
            elif isinstance(self.var.var, VariableIndexNode):
                variables[self.var.var.var.name][self.var.var.index.evaluate()][self.var.index.evaluate()] = self.val.evaluate()
            else:
                raise SemanticError('SEMANTIC ERROR')
        else:
            variables[self.var.name] = self.val.evaluate()
            # variables[self.var] = self.val.evaluate()

class VariableNode(Node):
    def __init__(self, var):
        self.name = var
    def evaluate(self):
        val = variables.get(self.name)
        if val is None:
            raise SemanticError()
        else:
            return val

    def prepend(self, elem):
        if isinstance(self.evaluate(), list):
            variables[self.name] = [elem] + variables.get(self.name)

class BasicLexer(Lexer):
    tokens = { VARIABLE, NUMBER, STRING, BOOLEAN,
                ANDALSO, PRINT, ASSIGN, EQ, SEMICOLON,
                IF, ELSE, WHILE,
                MOD, NOT, IN, ORELSE, DIV, CONS,
                EXPONENTIAL, NE, LE, LT, GE, GT}
                # LBRAC, RBRAC}
    ignore = '\t '
    literals = { '=', '+', '-', '/', '<', '>', 
                '*', '(', ')', ',', '[', ']', '{', '}', '#'}

    EQ      = r'=='
    ASSIGN  = r'='
    NE      = r'<>'
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    EXPONENTIAL = r'\*\*'
    ANDALSO = r'andalso'
    NOT     = r'not'
    PRINT   = r'print'
    IF      = r'if'
    
    ORELSE  = r'orelse'
    DIV     = r'div'
    ELSE    = r'else'
    WHILE   = r'while'
    MOD     = r'mod'
    IN      = r'in'
    SEMICOLON = r';'
    CONS    = r'::'

    BOOLEAN = r'(True|False)'
    STRING = r"['\"](.*?)['\"]"
    # NUMBER = r'\d*(\d\.|\.\d)\d*(e-?\d+)? | \d+ (e-?\d+)?'
    NUMBER  = r'[\d.]+(?:e-?\d+)?'
    
    # @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    # def VARIABLE(self, t):
    #     t.value = str(t.value)
    #     return t

    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'


    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
    tokens = BasicLexer.tokens
    precedence = (
        ('left', 'ORELSE'),
       ('left', 'ANDALSO'),
       ('left', 'NOT'),
       ('left', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'),
       ('right', 'CONS'),
       ('left', 'IN'),
       ('left', '+', '-'),
       ('left', '*', '/', 'DIV', 'MOD'), 
       ('right', 'EXPONENTIAL'),
       ('right', 'UMINUS'),
    )
  
    def __init__(self):
        self.env = { }
  
    # @_('')
    # def statement(self, p):
    #     pass  

    @_('print_stmt')
    def statement(self, p):
        return p.print_stmt
    
    @_('PRINT "(" expr ")" SEMICOLON')
    def print_stmt(self, p):
        return PrintNode(p.expr)
  
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
  
    @_('var ASSIGN expr SEMICOLON')
    def var_assign(self, p):
        return AssignmentNode(p.var, p.expr)
    
    @_('var "[" expr "]" ASSIGN expr SEMICOLON')
    def var_assign(self, p):
        return AssignmentNode(VariableIndexNode(p.var, p.expr0), p.expr1)

    @_('block')
    def statement(self, p):
        return p.block

    @_('"{" stmt_list "}"')
    def block(self, p):
        return BlockNode(p.stmt_list)

    @_('"{" "}"')
    def block(self, p):
        return BlockNode(None)

    @_('statement stmt_list')
    def stmt_list(self, p):
        return [p.statement] + p.stmt_list 
    
    @_('statement')
    def stmt_list(self, p):
        return [p.statement]

    @_('if_stmt')
    def statement(self, p):
        return p.if_stmt

    @_('IF "(" expr ")" block')
    def if_stmt(self, p):
        return IfNode(p.expr, p.block)

    @_('while_stmt')
    def statement(self, p):
        return p.while_stmt
    
    @_('WHILE "(" expr ")" block')
    def while_stmt(self, p):
        return WhileNode(p.expr, p.block)

    @_('ifelse_stmt')
    def statement(self, p):
        return p.ifelse_stmt

    @_('IF "(" expr ")" block ELSE block')
    def ifelse_stmt(self, p):
        return IfElseNode(p.expr, p.block0, p.block1)
# =================================

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('array')
    def expr(self, p):
        return (p.array)

    @_('"[" expr_list "]"')
    def array(self, p):
        return ListNode(p.expr_list)

    @_('"[" "]"')
    def array(self, p):
        return ListNode([])

    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('expr "," expr_list')
    def expr_list(self, p):
        return [p.expr] + p.expr_list
    
    @_('array "[" expr "]"')
    def array(self, p):
        return IndexNode(p.array, p.expr)

    @_('expr "[" expr "]"')
    def expr(self, p):
        return VariableIndexNode(p.expr0, p.expr1)

    @_('tuple')
    def expr(self, p):
        return p.tuple

    @_('"(" csl ")"')
    def tuple(self, p):
        return TupleNode(p.csl)

    @_('expr "," expr ","')
    def csl(self, p):
        return CSLNode(p.expr0, p.expr1)
    
    @_('csl expr ","')
    def csl(self, p):
        return CSLNode(p.csl, p.expr)

    @_('"#" expr tuple')
    def tuple(self,p):
        return IndexTupleNode(p.tuple, p.expr)

# =================================

    @_('expr "+" expr',
        'expr "-" expr',
        'expr "*" expr',
        'expr "/" expr',
        'expr EXPONENTIAL expr',
        'expr "<" expr',
        'expr ">" expr',
        'expr DIV expr',
        'expr MOD expr',
        'expr EQ expr',
        'expr NE expr',
        'expr LT expr',
        'expr LE expr',
        'expr GT expr',
        'expr GE expr',
        'expr ANDALSO expr',
        'expr ORELSE expr',
        'expr IN expr',
        'expr CONS expr')
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)

    @_('NOT expr')
    def expr(self,p):
        return OneOp(p[0], p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return OneOp(p[0], p.expr)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return NumberNode(p.NUMBER)

    @_('string')
    def expr(self,p):
        return p.string

    @_('STRING')
    def string(self, p):
        return StringNode(p.STRING)

    @_('string "[" expr "]"')
    def string(self, p):
        return IndexNode(p.string, p.expr)
    
    @_('BOOLEAN')
    def expr(self, p):
        return BooleanNode(p.BOOLEAN)

    @_('var')
    def expr(self, p):
        return p.var
        
    @_('VARIABLE')
    def var(self, p):
        return VariableNode(p.VARIABLE)


lexer = BasicLexer()
parser = BasicParser()
fd = open(sys.argv[1], 'r')
code = ""

for line in fd:
    code += line.strip()

try:
    ast = parser.parse(lexer.tokenize(code))
    ast.evaluate()
except Exception as e:
    print(str(e))

# if __name__ == '__main__':
#     lexer = BasicLexer()
#     parser = BasicParser()
#     env = {}

#     while True:          
#         try:
#             text = input('GFG Language > ')
#         except EOFError:
#             break
#         if text:
#             tree = parser.parse(lexer.tokenize(text))
#             # print(tree)
#             tree.evaluate()