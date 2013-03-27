#!/usr/bin/env python3 

""" Calculator class """

from Evaluator import EvaluationError, EvaluationFunction, EvaluationContext
from FormulaStructure import ParserError, FormulaElement, Sum
from Lexer import LexerLexeme, LexerParenthesis, LexerSymbol, LexerName, LexerValue, LexerError, Lexer

class Calculator:
	""" Very cool calculator class using all the other cool classes """
	
	def __init__(self):
		self.lexer = Lexer()
		self.context = EvaluationContext()
		self.builtins = ["exit", "debug", "help", "vars", "functions"]
		self.debug = False
	
	def main(self):
		""" Main function. Who would have expected this? """
		
		print("Welcome to {}.py v0.7".format(self.__class__.__name__))
		print()
		print("Note: Not every function will work with complex numbers.")
		print("Note: use debug command to toggle debug mode (syntax tree output).")
		print("Note: this version does not (yet?) support function definitions at runtime.")
		#TODO: some mechanism to insert lambda function definitions at runtime?
		print()
		self.handle_builtin("help")
		
		while True:
			try:
				print()
				formula = input(">>> ")
				
				if formula in self.builtins:
					self.handle_builtin(formula)
					continue
				
				lexemes = self.lexer.lexe(formula)
				parsed = Sum.parse(lexemes)
				if len(lexemes) != 0:
					raise ParserError("Formula did not parse completely," +
										"remaining lexemes are: {}".format(lexemes))
				
				if (self.debug):
					print("Input was parsed as this simplified syntax tree:")
					self.pretty_print(str(parsed))
				
				result = parsed.evaluate(self.context)
				self.context.set_variable("ans", result)
				
				print(self.format_result(result))
			
			except ParserError as e:
				print("ParserError:", e)
				continue
			except LexerError as e:
				print("LexerError:", e)
				continue
			except (EvaluationError, ValueError, TypeError) as e:
				print("EvaluationError:", e)
				continue
			except (KeyboardInterrupt, EOFError):
				print("Exiting.")
				break	
	
	def pretty_print(self, tree, indent=4):
		""" Very, very, very bad pretty print function.
			I couldn't imagine a clean way to pretty print these syntax tree strings... """
		cur_indent = 0
		cur_line = ""
		for i in range(len(tree) - 1):
			if tree[i] in [":", "("]:
				cur_line += tree[i]
				cur_indent += indent
				print(cur_line)
				cur_line = " " * cur_indent
				continue
			if tree[i] == " ":
				if cur_line == " " * len(cur_line):
					continue #don't print empty lines
				print(cur_line)
				cur_line = " " * cur_indent
				continue
			if tree[i] in ["]", ")"]:
				print(cur_line)
				cur_indent -= indent
				cur_line = " " * cur_indent + tree[i]
				continue
			cur_line += tree[i]
		
		print(cur_line)
		print(tree[-1])
	
	def handle_builtin(self, builtin):
		if builtin == "help":
			print("Built-in commands:")
			print(*self.builtins, sep=", ")
		
		elif builtin == "exit":
			raise EOFError
		
		elif builtin == "vars":
			variables = sorted(self.context.variables)
			max_length = max([len(v) for v in variables]) + 1
			
			print("There are currently {} known variables:".format(len(variables)))
			print("(Constants are marked with [*])")
			for key in variables:
				print("{}:{}{}{}".format(key, " " * (max_length - len(key)),
										self.format_result(self.context.get_variable(key)),
										" [*]" if self.context.is_variable_constant(key) else ""))
		
		elif builtin == "functions":
			functions = sorted(self.context.functions)
			
			print("There are currently {} supported functions:".format(len(functions)))
			for key in functions:
				string = "{}(".format(key)
				
				function = self.context.functions[key]
				maximum = function.arity if function.arity >= 0 else abs(function.arity) - 1
				
				for i in range(maximum):
					if i != 0:
						string += ", "
					
					string += chr(ord("a") + i)
				
				if function.arity < -1:
					string += ", *"
				elif function.arity == -1:
					string += "*"
				
				string += ") => {}".format(self.context.functions[key].description)
				print(string)
		
		elif builtin == "debug":
			self.debug = not self.debug
			print("Debug mode turned {}".format("on" if self.debug else "off"))
	
	def format_result(self, result):
		if isinstance(result, complex):
			string = str(result)
			if string[0] == '(': #format: (a+bj)
				return string[1:-1].replace('j', 'i')
			else: #format: bj
				return string.replace('j', 'i')
		else:
			return '{}'.format(result)

if __name__ == '__main__':
	Calculator().main()
