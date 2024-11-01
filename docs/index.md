# dagrunner

## Overview
This package serves to run and manage DAGs (Directed Acyclic Graphs) in a flexible and efficient manner, specifically geared towards scientists and others doing data analysis. It provides tools for executing tasks in a DAG. 

This package provides several key functionalities that are intended to facilitate data analysis:

1. Automatically keep track of which nodes need to be executed, and which nodes have already been run. Changes to a node's settings result in that node and all of the nodes that depend on it being marked as outdated. In this way, you can always be certain that your changes have been properly applied to your entire project.

2. Rule-based data subsetting ensures that your code is running only on the data that it's supposed to.

3. The outcome of each run is logged to gain insight into how the pipeline is performing.

### Dependencies
For defining DAG's as Python packages, see the [dagpiler](https://github.com/ResearchOS/dagpiler) package.

For defining the dataset for the DAG to operate on, see the [dataset-builder](https://github.com/ResearchOS/dataset-builder) package.