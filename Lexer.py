""" Lexer module """

class LexerError(SyntaxError):
	pass

class LexerLexeme:
	""" Basic lexeme class """
	
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return "[{}: {}]".format(self.__class__.__name__, self.value)

	def __repr__(self):
		return "[{}: {}]".format(self.__class__.__name__, self.value)

class LexerParenthesis(LexerLexeme):
	pass

class LexerSymbol(LexerLexeme):
	pass

class LexerName(LexerLexeme):
	pass

class LexerValue(LexerLexeme):
	pass

class Lexer:
	""" Simple lexer """
	
	def __init__(self):
		self.operators = ['+', '-', '*', '/', '%', '\\', '=', '^', ',']
		self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		self.digits_decimal_point = ['.'] + self.digits
		lower = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
				"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		upper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
				"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.characters = lower + upper
		self.name_elements = self.characters + self.digits
		
	def lexe(self, string):
		""" Lexes a string into ... well ... lexemes. """
		string = string.replace(" ", "") #strip whitespaces.
		lexemes = list()
		
		while len(string) > 0:
			current = string[0]
			string = string[1:]
			
			if current == '(' or current == ')':
				lexemes.append(LexerParenthesis(current))
				continue
			
			if current in self.operators:
				lexemes.append(LexerSymbol(current))
				continue
			
			if current in self.digits_decimal_point:
				#also lets stuff like .0.45 pass. will give ValueError later on.
				while len(string) > 0 and string[0] in self.digits_decimal_point:
					current += string[0]
					string = string[1:]
				lexemes.append(LexerValue(current))
				continue
			
			if current in self.characters:
				while len(string) > 0 and string[0] in self.name_elements:
					current += string[0]
					string = string[1:]
				lexemes.append(LexerName(current))
				continue
			
			#unknown elements detected.
			raise LexerError("Illegal input: '{}'".format(current))
		return lexemes
