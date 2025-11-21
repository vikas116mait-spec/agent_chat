import ast
import operator

def safe_eval(expr):
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.BinOp):
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return allowed_ops[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.Constant):
            return node.value
        raise ValueError("Unsupported expression")

    return _eval(ast.parse(expr, mode="eval"))

def calculator_tool(expr):
    expr = expr.replace("^", "**")
    try:
        return {"tool_result": safe_eval(expr)}
    except Exception as e:
        return {"tool_result": f"Error: {e}"}
