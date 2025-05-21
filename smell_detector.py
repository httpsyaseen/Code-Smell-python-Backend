import zipfile
import javalang
from detectors.design import (
    utility_class_detector,
    too_many_methods_detector,
    too_many_fields_detector,
    switch_density_detector,
    excessive_parameter_list_detector,
    excessive_imports_detector,
    cyclomatic_complexity_detector,
    private_constructors_final_detector,
    unchecked_exceptions_detector,
    raw_exception_types_detector,
    null_pointer_exception_detector,
    nested_if_detector,
)
from detectors.semantics import complex_method

from detectors.best_practices import (
    reassigning_catch_variables_detector,
    reassigning_loop_variables_detector,
    reassigning_parameters_detector,
    result_set_check_detector,
    expensive_log_statement_detector,
    # implicit_functional_interface_detector,
    literals_first_in_comparison_detector,
    # unused_local_variable_detector
) 

def analyze_code(content, filepath):
    smells = []
    source_lines = content.splitlines()
    filename = filepath.split('/')[-1]

    # AST-based analysis
    try:
        tree = javalang.parse.parse(content)
        detectors = [
            complex_method.detect_complex_method_smell,
            utility_class_detector.detect_utility_class,
            too_many_methods_detector.detect_too_many_methods,
            too_many_fields_detector.detect_too_many_fields,
            switch_density_detector.detect_switch_density,
            excessive_parameter_list_detector.detect_excessive_parameter_list,
            excessive_imports_detector.detect_excessive_imports,
            cyclomatic_complexity_detector.detect_cyclomatic_complexity,
            private_constructors_final_detector.detect_private_constructors_final,
            unchecked_exceptions_detector.detect_unchecked_exceptions,
            raw_exception_types_detector.detect_raw_exception_types,
            null_pointer_exception_detector.detect_null_pointer_exception,
            nested_if_detector.detect_nested_if,
            # abstract_class_no_methods_detector.detect_abstract_class_no_methods,
            reassigning_catch_variables_detector.detect_reassigning_catch_variables,
            reassigning_loop_variables_detector.detect_reassigning_loop_variables,
            reassigning_parameters_detector.detect_reassigning_parameters,
            result_set_check_detector.detect_result_set_check,
            expensive_log_statement_detector.detect_expensive_log_statement,
            # implicit_functional_interface_detector.detect_implicit_functional_interface,
            literals_first_in_comparison_detector.detect_literals_first_in_comparison,
            # unused_local_variable_detector.detect_unused_local_variable
        ]
        for path, node in javalang.ast.walk_tree(tree):
            for detector in detectors:
                result = detector(node, source_lines, filepath, filename)
                if result:
                    smells.extend(result if isinstance(result, list) else [result])
    except javalang.parser.JavaSyntaxError:
        pass  # Skip unparsable files



    return smells

import zipfile

def traverse_zip(zip_data):
    detected_smells = {}
    with zipfile.ZipFile(zip_data, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            # Skip if the file is in a 'test' directory
            if 'test/' in file_info.filename.lower():
                continue
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
