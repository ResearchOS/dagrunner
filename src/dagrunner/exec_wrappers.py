from .import_function import import_function

EXEC_WRAPPERS = {}

def get_exec_wrapper(exec_ext: str):
    """Get the wrapper function to execute the node."""
    return EXEC_WRAPPERS[exec_ext]

def register_exec_wrapper(exec_ext: str):
    def decorator(fcn):
        EXEC_WRAPPERS[exec_ext] = fcn
    return decorator

@register_exec_wrapper("m")
def matlab_wrapper(node_dict: dict, data_object_batch: str):
    pass

@register_exec_wrapper("py")
def python_wrapper(node_dict: dict, data_object_batch: str):
    # Load the input variables
    input_vars = {}
    for input_var_name, input_var in node_dict.inputs:
        input_vars[input_var_name] = load_var(node, input_var, data_object_batch)            
    
    imported_function = import_function(exec_file_path, fcn_name)
    output_values = imported_function(**input_vars)

    if not isinstance(output_values, tuple):
        output_values = (output_values,)

    # Save the outputs
    output_names = tuple(node.outputs)
    outputs_dict = {n: v for n, v in zip(output_names, output_values)}