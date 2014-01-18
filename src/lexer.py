__author__ = 'ZhngJingtian'

class Tag(object):
    '''Tag'''
    TERMINAL    = 1
    NONTERMINAL = 2
    EPSILON     = 3
    EOL         = 4
    GENERATOR   = 5
    SEPERATOR   = 6
    def __init__(self, tag):
        super(Tag, self).__init__()
        self.tag = tag


class Word(Tag):
    '''Word'''
    def __init__(self, tag, lexeme):
        super(Word, self).__init__(tag)
        self.lexeme = lexeme
    def __str__(self):
        if self.tag == Tag.TERMINAL:
            return "'" + self.lexeme + "'"
        else:
            return str(self.lexeme)

Word.EPSILON    = Word(Tag.EPSILON, '\xa6\xc5')
Word.EOL        = Word(Tag.EOL, '\n')
Word.GENERATOR  = Word(Tag.GENERATOR, '->')
Word.SEPERATOR  = Word(Tag.SEPERATOR, '|')

class Lexer(object):
    '''Lexer'''
    line = 0

    def __init__(self, text):
        super(Lexer, self).__init__()
        self.text   = text
        self.peek   = ' '
        self.curr   = 0
        self.nonterminals    = dict()
        self.terminals      = dict()
    def __readchar(self):
        if self.curr < len(self.text):
            self.peek = self.text[self.curr]
            self.curr = self.curr + 1
        else:
            self.peek = None

    def __readcharc(self, c):
        self.__readchar()
        if self.peek != c:
            return False
        self.peek = ' '
        return True


    def isCharacter(self, c):
        if c != None and ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')):
            return True
        else:
            return False

    def isEpsilon(self, c):
        if c != None and c == Word.EPSILON.lexeme:
            return True
        else:
            return False

    def error(self, s):
        raise Exception("lexer error : %s, at line %d."%(s,Lexer.line))

    def scan(self):
        while self.peek == ' ' or self.peek == '\t':
            self.__readchar()

        if self.peek == '\n':
            Lexer.line = Lexer.line + 1
            self.__readchar()
            return Word.EOL

        if self.peek == '-':
            if self.__readcharc('>'):
                return Word.GENERATOR
            else:
                self.error("incomplete symbol ->.")

        if self.peek == '|':
            self.__readchar()
            return Word.SEPERATOR

        if self.isEpsilon(self.peek):
            self.__readchar()
            return Word.EPSILON

        if self.isCharacter(self.peek):
            s = ""
            while self.isCharacter(self.peek):
                s = s + self.peek
                self.__readchar()
            if self.nonterminals.get(s) == None:
                word = Word(Tag.NONTERMINAL, s)
                self.nonterminals[word.lexeme] = word
                return word
            else:
                return self.nonterminals.get(s)

        if self.peek == '\'':
            s = ""
            self.__readchar()
            while self.peek != '\'':
                s = s + self.peek
                self.__readchar()
            self.__readchar()
            word =  Word(Tag.TERMINAL, s)
            if self.terminals.get(word.lexeme) == None:
                self.terminals[word.lexeme] = word
                return word
            else:
                return self.terminals.get(word.lexeme)
        return None

