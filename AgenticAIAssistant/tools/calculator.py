import math, re
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
SAFE.update({'abs': abs, 'round': round})
def calculate(expr: str) -> str:
    if not isinstance(expr, str):
        expr = str(expr)
    expr = expr.strip().replace('^', '**')
    print("***expr***:{}",expr)
    expr = re.sub(r"\bsqrt\(([^)]+)\)", r"math.sqrt(\1)", expr)
    try:
        return str(eval(expr, {'__builtins__': {}}, SAFE))
    except Exception as e:
        return f"Error evaluating expression: {e}"
