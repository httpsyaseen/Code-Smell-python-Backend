import javalang

def detect_too_many_fields(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.ClassDeclaration):
        field_count = len(node.fields)
        if field_count > 15:
            start_line = node.position.line if node.position else 1
            brace_count = 0
            end_line = start_line
            for i, line in enumerate(source_lines[start_line-1:], start=start_line):
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0 and '}' in line:
                    end_line = i
                    break
            return {
                "codeSmellType": "Too Many Fields",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "code": "TMF",
                "category": "design",
                "weight": 3
            }
    return None