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

    def isTerminal(self):
        return self.word.tag == lexer.Tag.TERMINAL
    def isEpsi(self):
        return self.word.tag == lexer.Tag.EPSILON

    def addFirsts(self, l):
        self.firstset += l

    def addFollows(self, l):
        self.followset += l

    def getFirsts(self):
        return self.firstset

    def setFlag(self, f):
        self.flag = f

    def getFlag(self):
        return self.flag


class Expresstion(object):
    def __init__(self):
        super(Expresstion, self).__init__()
        self.symbols = list()

    def addSymbol(self, sym):
        self.symbols.append(sym)

    def size(self):
        return len(self.symbols)

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

    def addExpr(self, expr):
        self.exprs[str(expr)] = expr

    def getExprs(self):
        return self.exprs.values()

    def hasEpsiExpr(self):
        for expr in self.exprs.values():
            if expr.symbols[0].isEpsi():
                return True
        return False

class Table(object):
    def __init__(self):
        super(Table, self).__init__()
        self.symbols  = dict()

    def addSymbol(self, symbol):
        self.symbols[str(symbol)] = symbol


class Parser(object):
    '''Parser'''
    def __init__(self, lexer):
        self.lexer  = lexer
        self.pros   = dict()
        self.look   = lexer.scan()
        self.symbols= dict()

    def error(self, s):
        raise Exception("parser error : %s, at line %d."%(s, self.lexer.line))

    def move(self):
        self.look = self.lexer.scan()

    def match(self, tag):
        if self.look.tag != tag:
            self.error("syntax error.")
        else:
            self.move()

    def __getsymbol(self, word):
        if self.symbols.get(str(word)) != None:
            return self.symbols.get(str(word))
        else:
            symbol = Symobl(word)
            self.symbols[str(word)] = symbol
            return symbol

    def __getpro(self, symbol):
        if self.pros.get(str(symbol)) != None:
            return self.pros.get(str(symbol))
        else:
            pro = Production(symbol)
            self.pros[str(pro)] = pro
            return pro


    def parse(self):
        while self.look != None:
            self.pro()
            self.match(lexer.Tag.EOL)

    def pro(self):
        word = self.look
        self.match(lexer.Tag.NONTERMINAL)
        symbol = self.__getsymbol(word)
        pro = self.__getpro(symbol)
        self.match(lexer.Tag.GENERATOR)
        exp = self.expr()
        pro.addExpr(exp)
        while self.look.tag == lexer.Tag.SEPERATOR:
            self.match(lexer.Tag.SEPERATOR)
            exp = self.expr()
            pro.addExpr(exp)
        return pro

    def expr(self):
        exp = Expresstion()
        while self.look.tag != lexer.Tag.SEPERATOR and self.look.tag != lexer.Tag.EOL:
            symbol = self.__getsymbol(self.look)
            exp.addSymbol(symbol)
            self.move()
        return exp

    def __hasflag(self, pros, flag):
        for pro in pros:
            if pro.left.getFlag() == flag:
                return pro
        return None

    def __hasepsi(self, f):
        for sym in f:
            if sym.isEpsi():
                return True
        return False

    def __getexprfirst(self, expr, table):
        f = list()
        if expr.symbols[0].isTerminal() or expr.symbols[0].isEpsi():
            f.append(expr.symbols[0])
            return f
        else:
            for sym in expr.symbols:
                if sym.getFlag() == 1:
                    f += sym.getFirsts()
                else:
                    tmp = self.__getprofirst(self.pros.get(str(sym)), table)
                    sym.addFirsts(tmp)
                    table.addSymbol(sym)
                    f += tmp
                if self.__hasepsi(f) == False:
                    return f

    def __getprofirst(self, pro, table):
        f = list()
        for expr in pro.getExprs():
            if expr.symbols[0] != pro.left:
                f += self.__getexprfirst(expr, table)
            else:
                if pro.hasEpsiExpr():
                    tmp = Expresstion()
                    tmp.symbols = expr.symbols[1:len(expr.symbols)]
                    f += self.__getexprfirst(tmp, table)
        pro.left.setFlag(1)
        return f

    def getFirstTable(self):
        table = Table()
        for pro in self.pros.values():
            for expr in pro.getExprs():
                for sym in expr.symbols:
                    if sym.isTerminal():
                        sym.addFirsts([sym])
                        sym.setFlag(1)
                        table.addSymbol(sym)
        pro = self.__hasflag(self.pros.values(), 0)
        while pro != None:
            pro.left.addFirsts(self.__getprofirst(pro, table))
            table.addSymbol(pro.left)
            pro = self.__hasflag(self.pros.values(), 0)
        return table



if __name__ == '__main__':
    text = "E   ->   E '+' ε \n"
    lex = lexer.Lexer(text)
    par = Parser(lex)
    par.parse()
    table = par.getFirstTable()
    print("ok")
