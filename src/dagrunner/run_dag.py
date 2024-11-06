import os

from base_dag import DAG
# from dagpiler.dag.printer import load_dag
from dagpiler.nodes.runnables.runnables import Runnable
from dagpiler.read_and_compile_dag import get_package_folder_path

from .compare_dags import compare_dags, get_most_recent_filename
from .exec_wrappers import get_exec_wrapper

DEFAULT_DELIMITER = "::"

class DagRunner:

    def __init__(self, dag: DAG, dataset):
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

    def run_node(self, node: Runnable, run_deps: bool = True):
        "Run the node for all Data Objects in the subset."        
        ordered_data_object_batches = get_data_objects_in_subset(node.subset, self.dataset)
        for data_object_batch in ordered_data_object_batches:
            self.run_node_one_data_object(node, data_object_batch)

    def run_node_one_data_object(self, node: Runnable, data_object_batch):
        "Load the data, run the executable, and save the data for one Data Object."
        package_name = node.package_name()
        exec = str(node.exec)
        exec_parts = exec.split(DEFAULT_DELIMITER)
        exec_file_path = exec_parts[0]
        fcn_name = exec_parts[1]

        package_folder_path = get_package_folder_path(package_name)
        abs_exec_file_path = os.path.join(package_folder_path, "src", package_name, exec_file_path)

        # Import the code
        if not os.path.exists(abs_exec_file_path):
            raise FileExistsError(f"The executable file does not exist: {exec_file_path}")

        # Run the wrapper to execute the code in the preferred language
        exec_ext = exec_file_path.split('.')[-1]
        exec_wrapper = get_exec_wrapper(exec_ext)
        status = exec_wrapper(node.to_dict(), data_object_batch, abs_exec_file_path, fcn_name)

        if not status:
            raise Exception(f"Node {node.name} failed to execute.")