import importlib.util
import os

def import_function(file_path: str, function_name: str):
    # Ensure the file path is absolute and valid
    if not os.path.isabs(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError("The provided file path is not valid.")
    
    # Load the module from the file path
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Retrieve the function
    if not hasattr(module, function_name):
        raise AttributeError(f"The function '{function_name}' is not found in {file_path}.")
    
    return getattr(module, function_name)