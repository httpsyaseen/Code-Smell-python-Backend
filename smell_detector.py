import zipfile
import javalang
from detectors import (
    ncss_detector,
    utility_class_detector,
    useless_overriding_detector,
    too_many_methods_detector,
    too_many_fields_detector,
    switch_density_detector,
    excessive_public_counts_detector,
    excessive_parameter_list_detector,
    excessive_imports_detector,
    cyclomatic_complexity_detector,
    coupling_between_objects_detector,
    private_constructors_final_detector,
    unchecked_exceptions_detector,
    raw_exception_types_detector,
    null_pointer_exception_detector,
    nested_if_detector,
    abstract_class_no_methods_detector
)

def analyze_code(content, filepath):
    smells = []
    source_lines = content.splitlines()
    filename = filepath.split('/')[-1]

    # AST-based analysis
    try:
        tree = javalang.parse.parse(content)
        detectors = [
            ncss_detector.detect_ncss,
            utility_class_detector.detect_utility_class,
            useless_overriding_detector.detect_useless_overriding,
            too_many_methods_detector.detect_too_many_methods,
            too_many_fields_detector.detect_too_many_fields,
            switch_density_detector.detect_switch_density,
            excessive_public_counts_detector.detect_excessive_public_counts,
            excessive_parameter_list_detector.detect_excessive_parameter_list,
            excessive_imports_detector.detect_excessive_imports,
            cyclomatic_complexity_detector.detect_cyclomatic_complexity,
            coupling_between_objects_detector.detect_coupling_between_objects,
            private_constructors_final_detector.detect_private_constructors_final,
            unchecked_exceptions_detector.detect_unchecked_exceptions,
            raw_exception_types_detector.detect_raw_exception_types,
            null_pointer_exception_detector.detect_null_pointer_exception,
            nested_if_detector.detect_nested_if,
            abstract_class_no_methods_detector.detect_abstract_class_no_methods
        ]
        for path, node in javalang.ast.walk_tree(tree):
            for detector in detectors:
                result = detector(node, source_lines, filepath, filename)
                if result:
                    smells.extend(result if isinstance(result, list) else [result])
    except javalang.parser.JavaSyntaxError:
        pass  # Skip unparsable files



    return smells

def traverse_zip(zip_data):
    detected_smells = {}
    with zipfile.ZipFile(zip_data, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.java'):
                with zip_ref.open(file_info) as java_file:
                    try:
                        content = java_file.read().decode('utf-8')
                        smells = analyze_code(content, file_info.filename)
                        if smells:
                            detected_smells[file_info.filename] = smells
                    except UnicodeDecodeError:
                        continue  # Skip files that can't be decoded
    return detected_smells