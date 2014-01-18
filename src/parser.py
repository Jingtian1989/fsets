__author__ = 'ZhangJingtian'
import lexer

class Symobl(object):
    def __init__(self, word):
        super(Symobl, self).__init__()
        self.firstset   = list()
        self.followset  = list()
        self.flag       = 0
        self.word       = word

    def __str__(self):
        return str(self.word)


class Expresstion(object):
    def __init__(self):
        super(Expresstion, self).__init__()
        self.symbols = list()

    def __str__(self):
        s = "["
        i = 0
        for i in range(len(self.symbols)-1):
            s = s + str(self.symbols[i]) + ","
        s = s + str(self.symbols[len(self.symbols)-1]) + "]"
        return s



class Production(object):
    def __init__(self, left):
        self.left   = left
        self.exprs  = dict()

    def __str__(self):
        return str(self.left)

    def addExpression(self, expr):
        self.exprs[str(expr)] = expr


class Parser(object):
    '''Parser'''
    def __init__(self, lexer):
        self.lexer  = lexer
        self.terminals   = dict()
        self.nontermials = dict()
        self.pros        = dict()
        self.look        = lexer.scan()
    def error(self, s):
        raise Exception("parser error : %s, at line %d."%(s, self.lexer.line))

    def move(self):
        self.look = self.lexer.scan()

    def match(self, tag):
        if self.look.tag != tag:
            self.error("syntax error.")
        else:
            self.move()

    def parse(self):
        while self.look != None:
            pro = self.production()
            self.match(lexer.Tag.EOL)
            self.pros[str(pro)] = pro

    def production(self):
        word = self.look
        self.match(lexer.Tag.NONTERMINAL)
        pro = Production(word)
        if self.pros.get(str(pro)) == None:
            self.pros[str(pro)] = pro
        else:
            pro = self.pros.get(str(pro))
        self.match(lexer.Tag.GENERATOR)
        exp = self.expr()
        pro.addExpression(exp)
        while self.look.tag == lexer.Tag.SEPERATOR:
            self.match(lexer.Tag.SEPERATOR)
            exp = self.expr()
            pro.addExpression(exp)
        return pro

    def expr(self):
        pass