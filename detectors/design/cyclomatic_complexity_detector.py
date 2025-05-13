import javalang

def detect_cyclomatic_complexity(node, source_lines, filepath, filename):
    smells = []
    if isinstance(node, (javalang.tree.MethodDeclaration, javalang.tree.ClassDeclaration)):
        complexity = 1
        for path, child in javalang.ast.walk_tree(node):
            if isinstance(child, (
                javalang.tree.IfStatement,
                javalang.tree.ForStatement,
                javalang.tree.WhileStatement,
                javalang.tree.DoStatement,
                javalang.tree.SwitchStatement,
                javalang.tree.TernaryExpression
            )) or (
                isinstance(child, javalang.tree.BinaryOperation) and child.operator in ['&&', '||']
            ):
                complexity += 1
        start_line = node.position.line if node.position else 1
        brace_count = 0
        end_line = start_line
        for i, line in enumerate(source_lines[start_line-1:], start=start_line):
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0 and '}' in line:
                end_line = i
                break
        if isinstance(node, javalang.tree.MethodDeclaration) and complexity > 10:
            smells.append({
                "codeSmellType": "High Cyclomatic Complexity (Method)",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "code": "CYC",
                "category": "Design",
                "weight": 3
            })
        elif isinstance(node, javalang.tree.ClassDeclaration) and complexity > 80:
            smells.append({
                "codeSmellType": "High Cyclomatic Complexity (Class)",
                "filename": filename,
                "filepath": filepath,
                "code": "CYC",
                "startline": start_line,
                "category": "Design",
                "endline": end_line,
                "weight": 3
            })
    return smells