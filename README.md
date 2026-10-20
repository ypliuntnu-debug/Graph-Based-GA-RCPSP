# Graph-Based-GA-RCPSP
Source code and configuration for the graph-based genetic algorithm for the Resource-Constrained Project Scheduling Problem (RCPSP).
### Scheduling Improvement Module
The schedule_improvement.py module contains auxiliary scheduling routines, including ACO-related functions. The proposed GGA uses its forward–backward improvement (FBI) routines, while the ACO pheromone-update mechanism is not employed in the reported experiments.
### Example Experiment Result

The file `j12031_8_output.txt` contains the execution log of a single experimental run of the proposed Graph-Based Genetic Algorithm (GGA) on the PSPLIB instance `j12031_8.sm`, which contains 120 non-dummy activities.

The log records the problem data, intermediate improvements in solution quality, and the final scheduling result. In this run, the algorithm obtained a final project makespan of **201 time units**.

This example is provided to illustrate the execution and optimization process of the proposed algorithm. It represents one stochastic run rather than an average result over multiple independent experiments. Consequently, the exact optimization trajectory may differ between executions.

Readers can use the provided source code and the corresponding PSPLIB instance to conduct independent experiments.
