
import pytest

from dagpiler import compile_dag
from dag_dataset.examples import load_test_table

from dagrunner.run_dag import DagRunner

def create_dagrunner():
    package_name = "frame_range_no_nan"
    dag = compile_dag(package_name)
    dataset = load_test_table()
    dagrunner = DagRunner(dag, dataset)  
    return dagrunner  

def test_dagrunner():
    dagrunner = create_dagrunner()
    dag = dagrunner.dag
    nodes = dag.nodes
    runnable_nodes = [n for n in nodes if n.__class__.__name__ == "Process"]
    data_object_batch = ''
    dagrunner.run_node_one_data_object(runnable_nodes[0], data_object_batch)
    print(dagrunner)

if __name__ == '__main__':
    # pytest.main([__file__])
    test_dagrunner()

