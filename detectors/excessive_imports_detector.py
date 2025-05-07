import javalang

def detect_excessive_imports(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.CompilationUnit):
        import_count = len(node.imports)
        if import_count > 30:
            start_line = 1
            end_line = len(source_lines)
            return {
                "codeSmellType": "Excessive Imports",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line
            }
    return None