import glob
import os
from datetime import datetime

from dagpiler.dag.organizer import get_dag_of_runnables

def compare_dags(current_dag, prior_dag):
    """Compare two DAGs and return a list of nodes from the current DAG that have changed compared to the prior DAG.
    The nodes are returned in a topologically sorted order according to the current DAG."""

    current_dag_runnables = get_dag_of_runnables(current_dag)
    prior_dag_runnables = get_dag_of_runnables(prior_dag)
    
    # Hash the nodes, including their descendants.
    current_hashes = {current_dag_runnables.hash(node): node for node in current_dag_runnables.nodes}
    prior_hashes = {prior_dag_runnables.hash(node): node for node in prior_dag_runnables.nodes}

    changed_nodes = []
    for hash, node in current_hashes.items():
        if hash not in prior_hashes:
            changed_nodes.append(node)

    current_dag_topo_sort = current_dag_runnables.topological_sort()
    changed_nodes_sorted = [node for node in current_dag_topo_sort if node in changed_nodes]

    return changed_nodes_sorted

def get_most_recent_filename(folder_path: str) -> str:
    # Check if folder_path exists and is a directory
    if not os.path.isdir(folder_path):
        return None
    
    # Get a list of all {datetime}.json files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    # Check if there are any JSON files in the folder
    if not json_files:
        return None
    
    # Extract datetime from each filename and find the most recent one
    most_recent_file = max(json_files, key=lambda f: datetime.strptime(os.path.basename(f).split('.')[0], "%Y-%m-%d_%H-%M-%S"))
    
    return most_recent_file
