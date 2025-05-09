import javalang

def detect_useless_overriding(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.MethodDeclaration) and node.body:
        if len(node.body) == 1 and isinstance(node.body[0], javalang.tree.ReturnStatement):
            return_stmt = node.body[0]
            if isinstance(return_stmt.expression, javalang.tree.SuperMethodInvocation):
                if return_stmt.expression.member == node.name and len(return_stmt.expression.arguments) == len(node.parameters):
                    start_line = node.position.line if node.position else 1
                    brace_count = 0
                    end_line = start_line
                    for i, line in enumerate(source_lines[start_line-1:], start=start_line):
                        brace_count += line.count('{') - line.count('}')
                        if brace_count == 0 and '}' in line:
                            end_line = i
                            break
                    return {
                        "codeSmellType": "Useless Overriding Method",
                        "filename": filename,
                        "filepath": filepath,
                        "startline": start_line,
                        "endline": end_line,
                        "code": "USD",
                        "category": "design",
                        "weight": 3
                    }
    return None