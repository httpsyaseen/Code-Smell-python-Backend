import javalang
import logging

# Configure logging


def get_max_if_depth(statement, current_depth=0):
    if isinstance(statement, javalang.tree.IfStatement):
      
        then_depth = get_max_if_depth(statement.then_statement, current_depth + 1) if statement.then_statement else current_depth + 1
        else_depth = get_max_if_depth(statement.else_statement, current_depth + 1) if statement.else_statement else current_depth + 1
        return max(then_depth, else_depth)
    elif hasattr(statement, 'statements') and isinstance(statement.statements, list):
        return max([get_max_if_depth(s, current_depth) for s in statement.statements] or [current_depth])
    elif isinstance(statement, list):
        return max([get_max_if_depth(s, current_depth) for s in statement] or [current_depth])
    return current_depth

def detect_nested_if(node, source_lines, filepath, filename):
    if isinstance(node, javalang.tree.MethodDeclaration):
 
        max_depth = get_max_if_depth(node.body)

        
        if max_depth > 3:
            start_line = node.position.line if node.position else 1
            brace_count = 0
            end_line = start_line
            for i, line in enumerate(source_lines[start_line-1:], start=start_line):
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0 and '}' in line:
                    end_line = i
                    break
            return {
                "codeSmellType": "Nested If Statements",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": end_line,
                "code": "NED"
            }

    return None
