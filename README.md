Math parser and Calculator
==========================

Mathematical formula/expression parser and evaluator written in Python.

Parses mathematical terms as defined by grammar.ebnf.

I don't know what else to write about it, it's not that powerful, but it was created as a small exercise.
Maybe someone has any use for it, feel free to modify the code under no conditions, see it as public domain.

Here's some output:
```
Welcome to Calculator.py v0.7

Note: Not every function will work with complex numbers.
Note: use debug command to toggle debug mode (syntax tree output).
Note: this version does not (yet?) support function definitions at runtime.

Built-in commands:
exit, debug, help, vars, functions

>>> debug
Debug mode turned on

>>> vars
There are currently 5 known variables:
(Constants are marked with [*])
ans:    0.0
answer: 42 [*]
e:      2.718281828459045 [*]
i:      1i [*]
pi:     3.141592653589793 [*]

>>> functions
There are currently 24 supported functions:
abs(a) => absolute value
acos(a) => arccosine
asin(a) => arcsine
atan(a) => arctangent
atan2(a, b) => arctangent(a/b)
ceil(a) => ceil
conj(a) => complex conjugate
cos(a) => cosine
degrees(a) => radians to degrees
exp(a) => e^a
floor(a) => floor
imag(a) => imaginary part of complex number
ld(a) => logarithmus dualis
ln(a) => logarithmus naturalis
log(a, b) => logarithm to base b
log10(a) => logarithmus decadis
max(a, b, *) => maximum of arguments
min(a, b, *) => minimum of arguments
pow(a, b) => a^b
radians(a) => degrees to radians
real(a) => real part of complex number
sin(a) => sine
sqrt(a) => square root
tan(a) => tangent

>>> sin(3 * pi / 2) ^ 3 % 2
Input was parsed as this simplified syntax tree:
[Product:
    [Power:
        [Function:
            sin(
                [Product:
                    [Decimal:
                        3
                    ]
                    *
                    [Variable:
                        pi
                    ]
                    /
                    [Decimal:
                        2
                    ]
                ]
            )
        ]
        ^
        [Decimal:
            3
        ]
    ]
    %
    [Decimal:
        2
    ]
]
1.0

>>> 
```