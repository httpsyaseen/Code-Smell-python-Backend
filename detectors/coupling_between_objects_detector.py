import javalang

def detect_coupling_between_objects(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.ClassDeclaration):
        coupled_types = set()
        # Fields
        for field in node.fields:
            if field.type:
                if isinstance(field.type, javalang.tree.ReferenceType):
                    coupled_types.add(field.type.name)
                elif isinstance(field.type, str):
                    coupled_types.add(field.type)
        # Local variables and return types in methods
        for method in node.methods:
            if method.return_type:
                if isinstance(method.return_type, javalang.tree.ReferenceType):
                    coupled_types.add(method.return_type.name)
                elif isinstance(method.return_type, str):
                    coupled_types.add(method.return_type)
            for path, child in javalang.ast.walk_tree(method):
                if isinstance(child, javalang.tree.LocalVariableDeclaration):
                    if child.type:
                        if isinstance(child.type, javalang.tree.ReferenceType):
                            coupled_types.add(child.type.name)
                        elif isinstance(child.type, str):
                            coupled_types.add(child.type)
        if len(coupled_types) > 20:
            start_line = node.position.line if node.position else 1
            brace_count = 0
            end_line = start_line
            for i, line in enumerate(source_lines[start_line-1:], start=start_line):
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0 and '}' in line:
                    end_line = i
                    break
            return {
                "codeSmellType": "Coupling Between Objects",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line
            }
    return None