from sly import Lexer
from sly import Parser

class SemanticError(Exception):
    pass

class Expr:
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

class BinOp(Expr):
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
        elif (self.op == 'andalso'):
            val1 = self.left.evaluate()
            val2 = self.right.evaluate()
            if isinstance(val1, bool) and isinstance(val2, bool):
                return val1 and val2
            else:
                raise SemanticError('SEMANTIC ERROR')

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
        # self.value = value
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
                ANDALSO, NOT, PRINT, ARRAY, ASSIGN, EQ, SEMICOLON,
                BLOCK, IF, ELSE, WHILE,
                MOD, AND}
                # LBRAC, RBRAC}
    ignore = '\t '
    literals = { '=', '+', '-', '/', '<', '>',
                '*', '(', ')', ',', ';', '[', ']', '{', '}'}

    EQ      = r'=='
    ASSIGN  = r'='
    ANDALSO = r'andalso'
    NOT     = r'not'
    PRINT   = r'print'
    IF      = r'if'
    ELSE    = r'else'
    WHILE   = r'while'
    MOD     = r'mod'
    SEMICOLON = r';'
    # LBRAC   = r'\['
    # RBRAC   = r'\]'

    BOOLEAN = r'(True|False)'
    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r"['\"](.*?)['\"]"
    NUMBER = r'\d+'
    
    # VARIABLE['print'] = PRINT

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
    tokens = BasicLexer.tokens
    precedence = (
        ('left', 'AND'),
        ('left', 'EQ'),
        ('left', '+', '-'),
        ('left', 'MOD'),
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
  
    # @_('VARIABLE ASSIGN expr SEMICOLON')
    @_('var ASSIGN expr SEMICOLON')
    def var_assign(self, p):
        return AssignmentNode(p.var, p.expr)
    
    # @_('VARIABLE "[" expr "]" ASSIGN expr SEMICOLON')
    @_('var "[" expr "]" ASSIGN expr SEMICOLON')
    def var_assign(self, p):
        return AssignmentNode(VariableIndexNode(p.var, p.expr0), p.expr1)

    @_('block')
    def statement(self, p):
        return p.block

    @_('"{" stmt_list "}"')
    def block(self, p):
        return BlockNode(p.stmt_list)

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

    # @_('var_index')
    # def expr(self, p):
    #     return p.var_index

    @_('var "[" expr "]"')
    # def var_index(self,p):
    def expr(self, p):
        return VariableIndexNode(p.var, p.expr)

    @_('array')
    def expr(self, p):
        return (p.array)

    @_('"[" expr_list "]"')
    def array(self, p):
        return ListNode(p.expr_list)

    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('expr "," expr_list')
    def expr_list(self, p):
        return [p.expr] + p.expr_list
    
    @_('array "[" expr "]"')
    def array(self, p):
        return IndexNode(p.array, p.expr)

# =================================

    @_('expr "+" expr',
        'expr "-" expr',
        'expr "<" expr',
        'expr ">" expr',
        'expr MOD expr',
        'expr EQ expr',
        'expr ANDALSO expr')
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)
    
    # @_('"(" expr ")"')
    # def expr(self, p):
    #     return p.expr

    @_('NUMBER')
    def expr(self, p):
        return NumberNode(p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return StringNode(p.STRING)
    
    @_('BOOLEAN')
    def expr(self, p):
        return BooleanNode(p.BOOLEAN)

    @_('var')
    def expr(self, p):
        return p.var
        
    @_('VARIABLE')
    def var(self, p):
        return VariableNode(p.VARIABLE)

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}

    fd = open("tests/test1.txt", 'r')
    code = ""

    for line in fd:
        code += line.strip()

    try:
        ast = parser.parse(lexer.tokenize(code))
        ast.evaluate()
    except Exception as e:
        print(str(e))

    while True:          
        try:
            text = input('GFG Language > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            # print(tree)
            tree.evaluate()
            # BasicExecute(tree, env)