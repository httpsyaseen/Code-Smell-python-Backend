import javalang

def detect_excessive_public_counts(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.ClassDeclaration):
        public_count = sum(
            1 for method in node.methods if 'public' in method.modifiers
        ) + sum(
            1 for field in node.fields if 'public' in field.modifiers
        )
        if public_count > 45:
            start_line = node.position.line if node.position else 1
            brace_count = 0
            end_line = start_line
            for i, line in enumerate(source_lines[start_line-1:], start=start_line):
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0 and '}' in line:
                    end_line = i
                    break
            return {
                "codeSmellType": "Excessive Public Counts",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "code": "EPC"
            }
    return None