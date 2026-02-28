# import ast
# import operator


# _ALLOWED_OPERATORS = {
#     ast.Add: operator.add,
#     ast.Sub: operator.sub,
#     ast.Mult: operator.mul,
#     ast.Div: operator.truediv,
#     ast.Mod: operator.mod,
# }


# def _evaluate(node):
#     if isinstance(node, ast.Constant):  # Python 3.8+
#         return node.value

#     if isinstance(node, ast.BinOp):
#         left = _evaluate(node.left)
#         right = _evaluate(node.right)
#         op_type = type(node.op)

#         if op_type in _ALLOWED_OPERATORS:
#             return _ALLOWED_OPERATORS[op_type](left, right)

#     raise ValueError("Invalid expression")


# def calculator(expression: str) -> str:
#     try:
#         parsed = ast.parse(expression, mode="eval")
#         result = _evaluate(parsed.body)
#         return str(result)
#     except Exception:
#         return "Tool Error: Invalid expression"



