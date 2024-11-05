
import pytest

from dagpiler import compile_dag
from dag_dataset.examples import load_test_table

from dagrunner.run_dag import DagRunner

def test_dagrunner():
    package_name = "frame_range_no_nan"
    dag = compile_dag(package_name)
    dataset = load_test_table()
    dagrunner = DagRunner(dag, dataset)
    print(dagrunner)

if __name__ == '__main__':
    pytest.main([__file__])

