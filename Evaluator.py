""" Evaluator classes """

import math

class EvaluationError(RuntimeError):
	pass

class EvaluationFunction:
	""" Function wrapper that can be used by EvaluationContext """
	
	def __init__(self, arity, function, description):
		self.arity = arity
		self.function = function
		self.description = description
	
	def __call__(self, arguments):
		return self.function(*arguments)

class EvaluationContext:
	""" EvaluationContext stores variables and functions to be used to evaluate formulas """
	
	def __init__(self):
		self.variables = {  "pi":		math.pi,
							"e":		math.e,
							"i":		1j,
							"ans":		0.0,
							"answer":	42,
						 }
		self.constants = ["pi", "e", "i", "answer"]
		
		#negative arity means variable argument count:
		#arity of -1 means: 0 or more arguments
		#arity of -2 means: 1 or more arguments
		#arity of -n means: n-1 or more arguments
		self.functions = {	"abs":		EvaluationFunction(1, math.fabs, "absolute value"),
							"exp":		EvaluationFunction(1, math.exp, "e^a"),
							"ln":		EvaluationFunction(1, math.log, "logarithmus naturalis"),
							"log":		EvaluationFunction(2, math.log, "logarithm to base b"),
							"log10":	EvaluationFunction(1, math.log10, "logarithmus decadis"),
							"ld":		EvaluationFunction(1, math.log2, "logarithmus dualis"),
							"sqrt":		EvaluationFunction(1, math.sqrt, "square root"),
							"pow":		EvaluationFunction(2, math.pow, "a^b"),
							"sin":		EvaluationFunction(1, math.sin, "sine"),
							"cos":		EvaluationFunction(1, math.cos, "cosine"),
							"tan":		EvaluationFunction(1, math.tan, "tangent"),
							"asin":		EvaluationFunction(1, math.asin, "arcsine"),
							"acos":		EvaluationFunction(1, math.acos, "arccosine"),
							"atan":		EvaluationFunction(1, math.atan, "arctangent"),
							"atan2":	EvaluationFunction(2, math.atan2, "arctangent(a/b)"),
							"degrees":	EvaluationFunction(1, math.degrees, "radians to degrees"),
							"radians":	EvaluationFunction(1, math.radians, "degrees to radians"),
							"min":		EvaluationFunction(-3, min, "minimum of arguments"),
							"max":		EvaluationFunction(-3, max, "maximum of arguments"),
							"floor":	EvaluationFunction(1, math.floor, "floor"),
							"ceil":		EvaluationFunction(1, math.ceil, "ceil"),
							"conj":		EvaluationFunction(1, lambda x : complex.conjugate(complex(x)), "complex conjugate"),
							"real":		EvaluationFunction(1, lambda x : complex(x).real, "real part of complex number"),
							"imag":		EvaluationFunction(1, lambda x : complex(x).imag, "imaginary part of complex number"),
						 }
		
		#self.register_function("answertolife", 0, lambda : 42, "answer to life, the universe and everything")
	
	def get_variable(self, name):
		if name in self.variables:
			return self.variables[name]
		else:
			raise EvaluationError("Unknown variable '{}'".format(name))
	
	def set_variable(self, name, value):
		if name in self.constants:
			raise EvaluationError("Assignment to constant '{}' not allowed".format(name))
		self.variables[name] = value
		return value
	
	def is_variable_constant(self, name):
		if name in self.variables:
			return name in self.constants
		else:
			raise EvaluationError("Unknown variable '{}'".format(name))
	
	def unregister_function(self, name):
		if name in self.functions:
			del(self.functions[name])
		else:
			raise EvaluationError("Function '{}' not currently registered.")
	
	def register_function(self, name, arity, function, description):
		if name in self.functions:
			raise EvaluationError("Function '{}' already registered.")
		
		self.functions[name] = EvaluationFunction(arity, function, description)
	
	def call_function(self, name, arguments):
		if name in self.functions:
			function = self.functions[name]
			if ((function.arity < 0 and abs(function.arity) - 1 <= len(arguments)) or
				function.arity == len(arguments)):
				return function(arguments)
			else:
				arity = function.arity if function.arity >= 0 else abs(function.arity) - 1
				raise EvaluationError("Function '{}' has arity {}, but got {} arguments.".format(name, arity, len(arguments)))
		else:
			raise EvaluationError("Function '{}' not found.".format(name))