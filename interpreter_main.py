expressions = [
"""
res = 7 + 5
res
""",

"""
res = 8 / 3
res
""",

"""
res = 8 - 3
res
""",

"""
res = 8 * 3
res
""",

"""
res = 8 % 3
res
""",

"""
num1 = 5
num2 = 6
res = num1 + num2
res
""",

"""
def foo(arg1, arg2):
    return arg1 * arg2
res = foo(6, 7)
res
""",

"""
def f_to_celsius(f):
    c = (f - 32) * (5/9)
    return c

ftemp = 68
res = f_to_celsius(ftemp)
""",

"""
def foo():
    return 25
res = foo()
res
""",

"""
def foo(arg1, arg2):
    return arg1 * arg2

def bar(x, y):
    return x + y

res = foo(6, 7) + bar(3,4)
res
""",

"""
num1 = 5
num2 = 16
def foo(arg1, arg2):
   return arg1 * arg2

res = foo(num1, num2 + 6)
res
""",

"""
num1 = 5
num2 = 6

def bar(x):
    return 20 + x

def foo(arg1, arg2):
    return arg1 * arg2

res = foo(num1, bar(num2))
res
""",

"""
def foo():
    def bar(x):
        return 20 + x
    return bar
res = foo()(3)
res
"""
]

expected_vals = [12, 8/3, 8-3, 8*3, 8%3, 11, 6*7, 5 * (16 + 6), 5 * 26, 23]
if __name__ == '__main__':
    import ast
    import interpreter

    i = 0
    for expression in expressions:
        print("\n")
        print(' '*6 + "expr" + str(i + 1) + "\n" + '-'*20)
        print(expression)
        tree = ast.parse(expression)
        expr_val = interpreter.eval_tree(tree)
        print("expected: {}\nactual: {}".format(expected_vals[i], expr_val[0]))
        print('-'*20 + "\n")
        i += 1
