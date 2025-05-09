import javalang

def detect_ncss(node, source_lines, filepath, filename):
    import re
    smells = []

    if isinstance(node, (javalang.tree.MethodDeclaration, javalang.tree.ClassDeclaration)):
        start_line = node.position.line if node.position else 1
        brace_count = 0
        end_line = start_line
        found_opening = False

        # Start scanning from the line where the node starts
        for i in range(start_line - 1, len(source_lines)):
            line = source_lines[i]
            brace_count += line.count('{')
            brace_count -= line.count('}')

            if '{' in line:
                found_opening = True

            if found_opening and brace_count == 0:
                end_line = i + 1
                break

        # Count NCSS: skip comments, blank lines, and import statements
        ncss = 0
        for line in source_lines[start_line - 1:end_line]:
            line = line.strip()
            if not line or re.match(r'^\s*(//|/\*|\*|\*/)', line) or line.startswith("import "):
                continue
            ncss += 1

        if isinstance(node, javalang.tree.MethodDeclaration) and ncss > 60:
            smells.append({
                "codeSmellType": "Long Method (NCSS)",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "ncss": ncss,
                "code": "NSD",
                "category": "design",
                "weight": 3
            })

        elif isinstance(node, javalang.tree.ClassDeclaration) and ncss > 1500:
            smells.append({
                "codeSmellType": "God Class (NCSS)",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "code":"GOD",
                "endline": end_line,
                "ncss": ncss,
                "category": "design",
                "weight": 3
            })

    return smells
