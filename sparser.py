from sly import Lexer
from sly import Parser

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, BOOLEAN,
                ANDALSO, NOT}
    ignore = '\t '
    literals = { '=', '+', '-', '/', 
                '*', '(', ')', ',', ';'}

    ANDALSO = r'andalso'
    NOT     = r'not'

    @_(r'(True|False)')
    def BOOLEAN(self, t):
        if t.value == "False":
            t.value = False
        else:
            t.value = True
        return t

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    @_(r"['\"](.*?)['\"]")
    def STRING(self, t):
        t.value = str(eval(t.value))
        return t
  
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value) 
        return t
  
    @_(r'//.*')
    def COMMENT(self, t):
        pass
  
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
    tokens = BasicLexer.tokens
    precedence = (
        ('left', '+', '-'),
        ('right', 'UMINUS'),
    )
  
    def __init__(self):
        self.env = { }
  
    @_('')
    def statement(self, p):
        pass
  
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
  
    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
  
    @_('NAME "=" str')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.str)
    
    @_('NAME "=" bool')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.bool)

    @_('expr')
    def statement(self, p):
        return (p.expr)
    
    @_('str')
    def statement(self, p):
        return (p.str)
    
    @_('bool')
    def statement(self, p):
        return (p.bool)
    
    # @_('name')
    # def statement(self, p):
    #     return (p.name)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)
  
    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)
  
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('str "+" str')
    def str(self, p):
        return ('add', p.str0, p.str1)
    
    @_('bool ANDALSO bool')
    def bool(self, p):
        return ('andalso', p.bool0, p.bool1)
    
    @_('NOT bool')
    def bool(self, p):
        return ('not', p.bool)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)
  
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('NAME')
    def str(self, p):
        return ('var', p.NAME)
    
    @_('STRING')
    def str(self, p):
        return ('str', p.STRING)
    
    @_('BOOLEAN')
    def bool(self, p):
        return ('str', p.BOOLEAN)
    
    @_('NAME')
    def bool(self, p):
        return ('var', p.NAME)


class BasicExecute:
    
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None:
            print(result)
  
    def walkTree(self, node):
  
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
  
        if node is None:
            return None
  
        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])
  
        if node[0] == 'num':
            return node[1]
        if node[0] == 'str':
            return node[1]
        if node[0] == 'bool':
            return node[1]
  
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'not':
            return not(self.walkTree(node[1]))
        elif node[0] == 'andalso':
            return self.walkTree(node[1]) and self.walkTree(node[2])
  
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]
  
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
      
    while True:          
        try:
            text = input('GFG Language > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env)