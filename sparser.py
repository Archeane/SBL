from sly import Lexer
from sly import Parser

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, BOOLEAN,
                ANDALSO, NOT, PRINT, ARRAY, ASSIGN, EQ,
                BLOCK}
    ignore = '\t '
    literals = { '=', '+', '-', '/', 
                '*', '(', ')', ',', ';', '[', ']', '{', '}'}

    EQ      = r'=='
    ASSIGN  = r'='
    ANDALSO = r'andalso'
    NOT     = r'not'


    @_(r'(True|False)')
    def BOOLEAN(self, t):
        if t.value == "False":
            t.value = False
        else:
            t.value = True
        return t
    
    # @_(r'\[[^\]]*\]')
    # def ARRAY(self, t):
    #     t.value = eval(str(t.value))
    #     return 
    

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
  
    NAME['print'] = PRINT

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
    
    @_('PRINT "(" statement ")"')
    def statement(self, p):
        return ('print', p.statement)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign
  
    @_('NAME ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
  
    @_('NAME ASSIGN str')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.str)
    
    @_('NAME ASSIGN bool')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.bool)

    @_('NAME ASSIGN array')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.array)

# =================================

    @_('expr')
    def statement(self, p):
        return (p.expr)
    
    @_('str')
    def statement(self, p):
        return (p.str)
    
    @_('bool')
    def statement(self, p):
        return (p.bool)

    @_('array')
    def statement(self, p):
        return (p.array)

# =======================

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

    # @_('ARRAY')
    # def array(self, p):
    #     return ('arr', p.ARRAY)

    @_('"[" elements "]"')
    def array(self, p):
        return ('arr', p.elements)

    @_('statement')
    def elements(self, p):
        return [p.statement]

    @_('statement "," elements')
    def elements(self, p):
        return [p.statement] + p.elements
    
    @_('NAME')
    def array(self, p):
        return ('var', p.NAME)


# ==================== ops =================

    @_('statement "+" statement')
    def statement(self, p):
        return p.statement0 + p.statement1

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

    @_('array "+" array')
    def array(self, p):
        return ('add', p.array0, p.array1)

    @_('array "+" expr')
    def array(self, p):
        return ('add', p.array, p.expr)

    @_('array "+" str')
    def array(self, p):
        return ('add', p.array, p.str)
    
    @_('array "[" expr "]"')
    def array(self, p):
        return ('index', p.array, p.expr)


class BasicExecute:
    
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        # if result is not None:
        #     print(result)
  
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
        if node[0] == 'arr':
            temp = []
            for e in node[1]:
                temp.append(self.walkTree(e))
            return temp

        if node[0] == 'block':
            for e in node[1]:
                self.walkTree(e)
  
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
        if node[0] == 'print':
            print(self.walkTree(node[1]))
            return
        if node[0] == 'index':
            array = self.walkTree(node[1])
            index = self.walkTree(node[2])
            return array[index]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

if __name__ == '__main__':
    lexer = BasicLexer()
    data = '''
{
    a = 1;
    print(a)
}
'''
    for tok in lexer.tokenize(data):
        print(tok)

    parser = BasicParser()

    temp = parser.parse(lexer.tokenize(data))
    print(temp)

    env = {}
      
    while True:          
        try:
            text = input('GFG Language > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            # print(tree)
            BasicExecute(tree, env)