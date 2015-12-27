# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS|MINUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', '-', ' ', or None
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


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

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
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+' or current_char == '-':
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def collect_digits(self):
        scale = 0
        val = 0
        if self.current_token.type != INTEGER:
            self.error()

        while self.current_token.type == INTEGER:
            val = val * 10 * scale + self.current_token.value
            scale += 1
            self.eat(INTEGER)
        return val

    def expr(self):
        """expr -> INTEGER+ SPACE? PLUS|MINUS SPACE? INTEGER+"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        value = self.collect_digits()

        # we expect the current token to be a '+' or '-' token
        op = self.current_token
        while op.type == OPERATOR:
            self.eat(OPERATOR)

            right = self.collect_digits()

            if op.value == '+':
                value = value + right
            elif op.value == '-':
                value = value - right

            op = self.current_token

        return value

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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()