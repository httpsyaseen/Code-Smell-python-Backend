import javalang

def detect_excessive_imports(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.CompilationUnit):
        import_decls = node.imports
        import_count = len(import_decls)

        if import_count > 30:
            # Collect line numbers for all imports that have position info
            import_lines = [imp.position.line for imp in import_decls if imp.position]

            if import_lines:
                start_line = min(import_lines)
                end_line = max(import_lines)
            else:
                start_line = 1
                end_line = 1

            return {
                "codeSmellType": "Excessive Imports",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "code": "EXI",
                "category": "Design",
                "weight": 3
            }
    return None
