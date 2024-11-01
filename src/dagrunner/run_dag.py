import os

import networkx as nx

from dagpiler.dag.organizer import order_nodes
from dagpiler.dag.printer import load_dag
from dagpiler.runnables.runnables import Runnable
from .compare_dags import compare_dags, get_most_recent_filename
from .import_function import import_function

DEFAULT_DELIMITER = "::"

class DagRunner:

    def __init__(self, dag: nx.MultiDiGraph, dataset):
        self.dag = dag
        self.dataset = dataset    

    def run(self):
        """Run the directional graph. Involves loading data, running the associated executable code, and saving the data."""        

        # 1. Isolate only the nodes that have been changed since last run (or whose ancestors changed)
        folder_path = os.path.join(os.getcwd(), ".dagpiler")
        file_path = get_most_recent_filename(folder_path)
        if file_path:
            prior_dag = load_dag(file_path)
            sorted_nodes = compare_dags(self.dag, prior_dag)
        else:
            sorted_nodes = self.dag.topological_sort()

        # 2. Run the nodes in topological order
        for node in sorted_nodes:            
            self.run_node(node, run_deps=False)

    def run_node(self, node: Runnable, run_deps=True):
        "Run the node for all Data Objects in the subset."        
        ordered_data_object_batches = get_data_objects_in_subset(node.subset, self.dataset)
        for data_object_batch in ordered_data_object_batches:
            self.run_node_one_data_object(node, data_object_batch)

    def run_node_one_data_object(self, node: Runnable, data_object_batch):
        "Load the data, run the executable, and save the data for one Data Object."
        # Load the input variables
        input_vars = {}
        for input_var_name, input_var in node.inputs:
            input_vars[input_var_name] = load_var(node, input_var, data_object_batch)

        # Run the executable code.
        exec = str(node.exec)
        exec_parts = exec.split(DEFAULT_DELIMITER)
        exec_file_path = exec_parts[0]
        fcn_name = exec_parts[1]

        # Import the code
        if not os.path.exists(exec_file_path):
            raise FileExistsError(f"The executable file does not exist: {exec_file_path}")
        
        imported_function = import_function(exec_file_path, fcn_name)
        output_values = imported_function(**input_vars)

        if not isinstance(output_values, tuple):
            output_values = (output_values,)

        # Save the outputs
        output_names = tuple(node.outputs)
        outputs_dict = {n: v for n, v in zip(output_names, output_values)}

        # Tell the successor nodes that this node has been run.