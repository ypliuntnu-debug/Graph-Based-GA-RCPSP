# Graph-Based-GA-RCPSP

Source code and experimental configuration for the Graph-Based Genetic Algorithm (GGA) for the Resource-Constrained Project Scheduling Problem (RCPSP).

### 1. Method Overview

The proposed GGA uses an Activity-on-Node (AON) graph representation in which time lags between activities form the primary chromosome. The precedence graph remains fixed, while lag values are modified during evolutionary search.

The algorithm integrates genetic operators operating on three related representations:

- **Lag representation:** Crossover and mutation of activity time lags.
- **Day-form representation:** Crossover and mutation of activity start times.
- **Activity-list representation:** Recombination and mutation of feasible activity sequences.

The representations are transformed into one another to support different search operations within a unified evolutionary framework.

A frozen-subgraph mechanism preserves selected activity relationships during genetic operations. Forward–backward improvement (FBI) is applied as an auxiliary schedule-improvement procedure.

Detailed descriptions of the algorithm and operators are provided in the accompanying manuscript.

### 2. Source Code

- `publication gga code.py`: Main GGA implementation, including evolutionary search and genetic operators.
- `schedule_improvement.py`: Auxiliary scheduling and improvement procedures.
- `j12031_8_output.txt`: Execution log of one illustrative experiment.

### 3. Scheduling Improvement Module

The `schedule_improvement.py` module contains auxiliary scheduling routines, including ACO-related functions. The proposed GGA uses its forward–backward improvement (FBI) routines, while the ACO pheromone-update mechanism is not employed in the reported experiments.

The original module is provided unchanged to ensure transparency and consistency with the implementation used in the study.

### 4. Experimental Configuration

The experiments use benchmark instances from the Project Scheduling Problem Library (PSPLIB).

PSPLIB: https://www.om-db.wi.tum.de/psplib/

The main source code includes the following settings for the supplied J120 example:

| Parameter | Setting |
|---|---|
| Benchmark family | PSPLIB J120 |
| Example instance | `j12031_8.sm` |
| Main search limit | 50,000 evaluated schedules |
| Stopping condition | Search limit reached or reference value attained |
| Auxiliary improvement | Forward–backward improvement |
| ACO pheromone updating | Not used |

The search is stochastic. Results may vary between independent executions.

### 5. Input Data and Execution

The original implementation reads benchmark instances from external PSPLIB files.

The input includes activity durations, precedence relationships, resource requirements, and resource capacities.

The main program also reads a reference-value file named `120cpm.txt`, which is used for evaluating the resulting makespan and determining whether the reference value has been reached.

To execute the original implementation, users must provide the required input files and configure their paths consistently with the source code.

### 6. Example Experiment Result

The file `j12031_8_output.txt` contains the execution log of a single experimental run on PSPLIB instance `j12031_8.sm`, using the implementation provided in publication gga code.py.

The log records the problem data, intermediate solution improvements, and the final scheduling result.

The final makespan obtained in this illustrative run was **201 time units**.

The example demonstrates the execution of the algorithm and is not intended to represent the average performance over multiple independent runs.

### 7. Reproducibility Notes

The original source code is provided to support independent examination and execution of the proposed algorithm.

The historical experiments did not retain all random seeds. Therefore, exact reproduction of individual stochastic trajectories cannot be guaranteed. Independent runs can be used to assess the algorithm's behavior and reported performance.
