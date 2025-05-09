import javalang

def detect_raw_exception_types(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.ThrowStatement):
        expr = node.expression
        if isinstance(expr, javalang.tree.ClassCreator):
            if hasattr(expr, 'type') and hasattr(expr.type, 'name'):
                raw_types = {'RuntimeException', 'Throwable', 'Exception', 'Error'}
                if expr.type.name in raw_types:
                    start_line = node.position.line if node.position else 1
                    return {
                        "codeSmellType": "Throwing Raw Exception Types",
                        "filename": filename,
                        "filepath": filepath,
                        "startline": start_line,
                        "endline": start_line,
                        "code": "RWD",
                        "category": "design",
                        "weight": 3
                    }
    return None
