""" Classes that represent a formula's structure
	
	NOTE:
	Parsing logic contains some aspects that don't comply with the grammar's rules.
	This will not effect user experience - it only changes (simplifies) the resulting
	syntax tree. The parser will correctly parse the language defined by the grammar,
	but with some simplifications (e.g. remove the need of wrapping productions:
	grammar would require sum->product->power->toplevel->decimal->5,
	with simplifications, it is decimal->5.
	Simplifications are marked with NOTE.
"""

from Lexer import LexerName, LexerValue, LexerSymbol, LexerParenthesis, LexerLexeme

class ParserError(SyntaxError):
	pass

class AdditionalElement:
	""" Additional multiplication or addition to be appended to Sum / Product """
	
	def __init__(self, operator, value):
		self.operator = operator
		self.value = value
	
	def __str__(self):
		return "{} {}".format(self.operator, self.value)
	
	def __repr__(self):
		return "{} {}".format(self.operator, self.value)

class FormulaElement:
	""" Base element a formula is made up from """
	
	def __init__(self, value):
		""" Should-be-private constructor, signature might vary in subclasses """
		self.value = value
	
	def evaluate(self, context):
		""" Evaluates this element and its child elements in a given EvaluationContext """
		raise NotImplementedError
	
	def parse(lexemes):
		""" Parses a list of lexemes into a class instance.
			Uses a lot of recursion and removes lexemes from the list on its way.
			This is the only supported way to construct a class instance (via private constructor) """
		raise NotImplementedError
	
	def __str__(self):
		return "[{}: {}]".format(self.__class__.__name__, self.value)
	
	def __repr__(self):
		return "[{}: {}]".format(self.__class__.__name__, self.value)

class Function(FormulaElement):
	""" Formula element representing a function """
	
	def __init__(self, name, arguments):
		self.name = name
		self.arguments = arguments
	
	def evaluate(self, context):
		evaluated_arguments = [arg.evaluate(context) for arg in self.arguments]
		return context.call_function(self.name, evaluated_arguments)
	
	def parse(lexemes):
		if len(lexemes) < 3:
			raise ParserError("Too few lexemes for Function")
		
		name = lexemes[0].value
		
		if lexemes[1].value != '(':
			raise ParserError("Expected '(', but found '{}'".format(lexemes[1].value))
		
		lexemes.pop(0)
		lexemes.pop(0) #double shift forward (function name and opening parenthesis)
		
		arguments = list()
		
		if lexemes[0].value != ')': #support arity of 0
			arguments.append(Sum.parse(lexemes))
			
			while len(lexemes) > 0 and lexemes[0].value == ',':
				lexemes.pop(0)
				arguments.append(Sum.parse(lexemes))
		
		if len(lexemes) == 0:
			raise ParserError("Expected ')', but found nothing.")
		if lexemes[0].value != ')':
			raise ParserError("Expected ')', but found '{}'".format(lexemes[0].value))
		
		lexemes.pop(0) #shift forward (closing parenthesis)
		
		return Function(name, arguments)
	
	def __str__(self):
		return "[{}: {}({})]".format(self.__class__.__name__, self.name, ", ".join(str(a) for a in self.arguments))

class Sum(FormulaElement):
	""" Addition or subtraction formula element """
	
	def __init__(self, value, additional):
		self.value = value
		self.additional = additional
	
	def evaluate(self, context):
		value = self.value.evaluate(context)
		
		for add in self.additional:
			if add.operator == '+':
				value += add.value.evaluate(context)
			elif add.operator == '-':
				value -= add.value.evaluate(context)
			else:
				#this. should. not. happen.
				raise ParserError("Expected operator '+' or '-', but found '{}'".format(add.value))
		
		return value
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Sum")
		
		value = Product.parse(lexemes)
		
		additional = list()
		while len(lexemes) > 1 and lexemes[0].value in ['+', '-']:
			operator = lexemes[0].value
			lexemes.pop(0)
			additional.append(AdditionalElement(operator, Product.parse(lexemes)))
		
		#NOTE: first return is incorrect according to the grammar - but simpler.
		if len(additional) == 0:
			return value #which is a Product
		else:
			return Sum(value, additional)
	
	def __str__(self):
		return "[{}: {} {}]".format(self.__class__.__name__, self.value, " ".join(str(a) for a in self.additional))

class Product(FormulaElement):
	""" Multiplication or division formula element """
	
	def __init__(self, value, additional):
		self.value = value
		self.additional = additional
	
	def evaluate(self, context):
		value = self.value.evaluate(context)
		
		for add in self.additional:
			if add.operator == '*':
				value *= add.value.evaluate(context)
			elif add.operator == '/':
				value /= add.value.evaluate(context)
			elif add.operator == '%':
				value %= add.value.evaluate(context)
			elif add.operator == '\\':
				value //= add.value.evaluate(context)
			else:
				raise ParserError("Expected operator '*', '/', '%' or '\\', but found '{}'".format(add.value))
		
		return value
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Product")
		
		value = Power.parse(lexemes)
		
		additional = list()
		while len(lexemes) > 1 and lexemes[0].value in ['*', '/', '%', '\\']:
			operator = lexemes[0].value
			lexemes.pop(0)
			additional.append(AdditionalElement(operator, Power.parse(lexemes)))
		
		#NOTE: first return is incorrect according to the grammar - but simpler.
		if len(additional) == 0:
			return value #which is a Power
		else:
			return Product(value, additional)
	
	def __str__(self):
		return "[{}: {} {}]".format(self.__class__.__name__, self.value, " ".join(str(a) for a in self.additional))

class Power(FormulaElement):
	""" Power formula element """
	
	def __init__(self, base, exponent):
		self.value = base
		self.exponent = exponent
	
	def evaluate(self, context):
		if self.exponent is not None:
			return self.value.evaluate(context) ** self.exponent.evaluate(context)
		else:
			return self.value.evaluate(context)
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Power")
		
		base = Toplevel.parse(lexemes)
		exponent = None
		
		if len(lexemes) > 1 and lexemes[0].value == '^':
			lexemes.pop(0)
			exponent = Power.parse(lexemes)
		else:
			#NOTE: incorrect according to grammar, but shorter
			return base #which is Toplevel
		
		return Power(base, exponent)
	
	def __str__(self):
		return "[{}: {} ^ {}]".format(self.__class__.__name__, self.value, self.exponent)

class Toplevel(FormulaElement):
	""" Toplevel formula element (Can contain decimal value, variable, variable assignment,
		negated toplevel, Sum element in parentheses) """
	
	def __init__(self, value, additional):
		self.value = value
		self.additional = additional
	
	def evaluate(self, context):
		if isinstance(self.additional, AdditionalElement):
			if self.additional.operator == '=':
				#self.value is Variable instance, we need self.value.value which is name of variable
				return context.set_variable(self.value.value, self.additional.value.evaluate(context))
			elif self.additional.operator == '-':
				return - self.additional.value.evaluate(context)
			else:
				raise ParserError("Expected operator '-' or '=', but found '{}'".format(self.additional.operator))
		else:
			#decimal or ( base )
			return self.value.evaluate(context)
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Toplevel")
		
		if isinstance(lexemes[0], LexerValue):
			#NOTE: different from grammar for reasons of simplicity:
			#grammar would require Toplevel(Decimal.parse(lexemes), None)
			return Decimal.parse(lexemes)
		
		if lexemes[0].value == '-':
			lexemes.pop(0)
			#empty string is a trick to create a nice syntax tree
			return Toplevel("", AdditionalElement('-', Toplevel.parse(lexemes)))
		
		if lexemes[0].value == '(':
			lexemes.pop(0)
			#NOTE: different from grammar for reasons of simplicity:
			#grammar would require Toplevel(Sum.parse(lexemes), None)
			ret = Sum.parse(lexemes)
			if len(lexemes) == 0 or lexemes[0].value != ')':
				raise ParserError("Expected ')', but found '{}'".format(lexemes[0].value))
			lexemes.pop(0) #consume closing parenthesis
			return ret
		
		if len(lexemes) > 1 and isinstance(lexemes[0], LexerName):
			if lexemes[1].value == '(':
				#NOTE: grammar would require Sum(Function.parse(lexemes))
				return Function.parse(lexemes)
		
		if isinstance(lexemes[0], LexerName):
			value = Variable.parse(lexemes)
			additional = None
			
			if len(lexemes) > 1 and lexemes[0].value == '=':
				lexemes.pop(0)
				additional = AdditionalElement('=', Sum.parse(lexemes))
			else:
				#NOTE: incorrect according to the grammar - but simpler.
				return value #which is Variable
			
			return Toplevel(value, additional)
		
		raise ParserError("Expected Toplevel, but found '{}'".format(lexemes))
	
	def __str__(self):
		return "[{}: {} {}]".format(self.__class__.__name__, self.value, self.additional)

class Decimal(FormulaElement):
	""" Decimal value formula element """
	
	def __init__(self, value):
		self.value = value
	
	def evaluate(self, context):
		return float(self.value) #throws a ValueError if entered value is not a valid float.
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Decimal")
		
		if isinstance(lexemes[0], LexerValue):
			value = lexemes[0].value
			lexemes.pop(0)
			return Decimal(value)
		else:
			raise ParserError("Expected Decimal, but found '{}'".format(lexemes))

class Variable(FormulaElement):
	""" Variable formula element """
	
	def __init__(self, value):
		self.value = value
	
	def evaluate(self, context):
		return context.get_variable(self.value)
	
	def parse(lexemes):
		if len(lexemes) == 0:
			raise ParserError("Too few lexemes for Variable")
		
		if isinstance(lexemes[0], LexerName):
			value = lexemes[0].value
			lexemes.pop(0)
			return Variable(value)
		else:
			raise ParserError("Expected Variable, but found '{}'".format(lexemes))
