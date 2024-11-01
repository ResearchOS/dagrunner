# Criteria to Run Nodes

For a node in the DAG to be executed, it must meet certain criteria. Essentially, if the node is outdated in any way, then it will be run, otherwise it will be skipped. 

A node is deemed to be up to date if it has already been run previously, none of its settings have changed, and none of the settings of the nodes it depends on have changed. If these three criteria are met, then the node will not be run, as it is not outdated.