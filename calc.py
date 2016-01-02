# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, OPERATOR, OPEN_PAREN, CLOSE_PAREN, EOF = 'INTEGER', 'OPERATOR', 'OPEN_PAREN', 'CLOSE_PAREN', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, MUL, DIV, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '*', '/', ' ', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class AST(object):
  pass

class BinOp(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right

class Num(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Lexer(object):
  def __init__(self, text):
    # client string input, e.g. "3*5/5"
    self.text = text
    # self.pos is an index into self.text
    self.pos = 0
    # current token instance
    self.current_token = self.get_next_token()

  def error(self):
      raise Exception('Error parsing input')

  def get_next_token(self):
      """Lexical analyzer (also known as scanner or tokenizer)

      This method is responsible for breaking a sentence
      apart into tokens. One token at a time.
      """
      text = self.text

      # is self.pos index past the end of the self.text ?
      # if so, then return EOF token because there is no more
      # input left to convert into tokens
      if self.pos > len(text) - 1:
        return Token(EOF, None)

      # get a character at the position self.pos and decide
      # what token to create based on the single character
      current_char = text[self.pos]

      if current_char.isspace():
        self.pos += 1
        return self.get_next_token()

      # if the character is a digit then convert it to
      # integer, create an INTEGER token, increment self.pos
      # index to point to the next character after the digit,
      # and return the INTEGER token
      if current_char.isdigit():
        digits = current_char
        while len(text) > self.pos+1 and text[self.pos+1].isdigit():
          self.pos += 1
          current_char = text[self.pos]
          digits += current_char
        
        self.pos += 1
        token = Token(INTEGER, int(digits))
        return token

      if current_char in ('*', '/', '-', '+'):
        token = Token(OPERATOR, current_char)
        self.pos +=1
        return token

      if current_char == '(':
        token = Token(OPEN_PAREN, current_char)
        self.pos += 1
        return token

      if current_char == ')':
        token = Token(CLOSE_PAREN, current_char)
        self.pos += 1
        return token

      self.error()

class Parser(object):

  def __init__(self, lexer):
    self.lexer = lexer
    # set current token to the first token taken from the input
    self.current_token = self.lexer.current_token

  def error(self):
    raise Exception('Invalid syntax')

  def eat(self, token_type):
    # compare the current token type with the passed token
    # type and if they match then "eat" the current token
    # and assign the next token to the self.current_token,
    # otherwise raise an exception.
    if self.lexer.current_token.type == token_type:
      self.lexer.current_token = self.lexer.get_next_token()
    else:
      self.error()

  def factor(self):
    token = self.lexer.current_token

    if (token.type == OPEN_PAREN):
      return self.paren()

    self.eat(INTEGER)
    return Num(token)

  def paren(self):
    self.eat(OPEN_PAREN)
    rvalue = self.expr()
    self.eat(CLOSE_PAREN)
    return rvalue

  def term(self, result = 1):
    """expr -> INTEGER+ SPACE? DIVIDE|MULTIPLY SPACE? INTEGER+"""
    left = self.factor()

    while self.lexer.current_token.value in ('/', '*'):
      token = self.lexer.current_token

      self.eat(OPERATOR)
      right = self.factor()
      left = BinOp(left, token, right)

    return left

  def expr(self):
    """expr -> INTEGER+ SPACE? DIVIDE|MULTIPLY SPACE? INTEGER+"""
    left = self.term()

    while self.lexer.current_token.value in ('+', '-'):
      token = self.lexer.current_token

      self.eat(OPERATOR)
      right = self.term()
      left = BinOp(left, token, right)

    return left

def main():
  while True:
    try:
        # To run under Python3 replace 'raw_input' call
        # with 'input'
        text = raw_input('calc> ')
    except EOFError:
        break
    if not text:
        continue
    lexer = Lexer(text)
    parser = Parser(lexer)
    result = parser.expr()
    print(result)

if __name__ == '__main__':
    main()