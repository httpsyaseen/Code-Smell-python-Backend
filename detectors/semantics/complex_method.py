import javalang
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model once
model_path = "trained_model"  
tokenizer = AutoTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def detect_complex_method(code):
    inputs = tokenizer(code, truncation=True, max_length=512, padding=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return prediction == 1

def extract_method_code(source_lines, start_line):
    code = []
    brace_count = 0
    started = False

    for line in source_lines[start_line - 1:]:
        stripped = line.strip()
        if "{" in stripped:
            brace_count += stripped.count("{")
            started = True
        if "}" in stripped:
            brace_count -= stripped.count("}")
        code.append(line)
        if started and brace_count == 0:
            break

    return "\n".join(code)

def detect_complex_method_smell(node, source_lines, filepath, filename):
    import javalang.tree

    if isinstance(node, javalang.tree.MethodDeclaration) and node.position:
        # Skip main method
        if node.name == "main":
            return None

        start_line = node.position.line
        code_snippet = extract_method_code(source_lines, start_line)

        if detect_complex_method(code_snippet):
            return {
                "codeSmellType": "Complex Method",
                "filename": filename,
                "filepath": filepath,
                "startline": start_line,
                "endline": start_line + code_snippet.count('\n'),  # approx
                "code": "CM",
                "category": "Sematic Based",
                "weight": 3
            }

    return None
