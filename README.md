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
- `j12031_8_output.txt.docx`: Execution log of one illustrative experiment.
-  `colab results from github experiment.py.docx`: Complete execution log of the standalone Google Colab example.

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

Additional algorithmic parameters, including those controlling population initialization, genetic operations, and evolutionary search, are defined directly in the source code and described in the accompanying manuscript. The search is stochastic. Results may vary between independent executions.

### 5. Input Data and Execution

The original implementation reads benchmark instances from external PSPLIB files.

The input includes activity durations, precedence relationships, resource requirements, and resource capacities.

The main program also reads a reference-value file named `120cpm.txt`, which is used for evaluating the resulting makespan and determining whether the reference value has been reached.

To execute the original implementation, users must provide the required input files and configure their paths consistently with the source code.

### 6. Example Experiment Result from local computer

The file `j12031_8_output.txt.docx` contains the execution log of a single experimental run on PSPLIB instance `j12031_8.sm`, using the implementation provided in publication gga code.py.

The log records the problem data, intermediate solution improvements, and the final scheduling result.

The final makespan obtained in this illustrative run was **201 time units**.

The example demonstrates the execution of the algorithm and is not intended to represent the average performance over multiple independent runs.

### 7. Reproducibility Notes
The original source code is provided to support independent examination and execution of the proposed algorithm.

The historical experiments did not retain all random seeds. Therefore, exact reproduction of individual stochastic trajectories cannot be guaranteed.

Because the algorithm involves stochastic evolutionary operations, independent executions using the same benchmark instance and experimental settings may produce different final makespans. The original local execution achieved a makespan of 201, while an independent Google Colab execution of the standalone example achieved a makespan of 198. These results illustrate stochastic variation between executions and are not guaranteed outcomes.

Independent executions can be used to assess the algorithm's behavior and reported performance.



### 8. Standalone Runnable Example

The file `github experiment.py` provides a self-contained, executable implementation of the proposed Graph-Based Genetic Algorithm (GGA) for the PSPLIB instance `j12031_8.sm`, which is also used in the ablation case study presented in the manuscript.

**Consistency with the original implementation**

The standalone example retains the same GGA functions, genetic operators, and algorithmic parameter settings as the original research implementation (`publication gga code.py`), as described in Section 4. It is not a simplified version of the algorithm, and the underlying genetic search procedure remains unchanged.

**Self-contained execution**

The original research implementation requires external PSPLIB benchmark files, reference-value data, and appropriate file-path configuration.

To eliminate these external dependencies for the illustrative experiment, the standalone version embeds the `j12031_8.sm` benchmark data and the scheduling-improvement module, including the forward–backward improvement (FBI) procedures, directly within a single Python file. The corresponding input/output arrangements have also been adapted.

Consequently, readers can independently execute and examine the GGA on this benchmark instance without downloading separate PSPLIB files or configuring additional scheduling modules.

**Execution requirements**

- Python 3
- NumPy
- pandas

The example can be executed in a local Python environment or Google Colab using:

```bash
python "github experiment.py"
```

The program prepares the embedded benchmark instance data, executes the GGA, and reports the best schedule, makespan, and computational time.

**Supporting execution records**

Two illustrative execution records are provided in the repository:

- **Local computer:** An execution of the original research implementation (`publication gga code.py`) achieved a makespan of **201**.
- **Google Colab:** An independent execution of the standalone implementation (`github experiment.py`) achieved a makespan of **198**.

The corresponding execution logs are documented in Sections 6 and 9. These records provide concrete examples of the algorithm's execution in different computing environments. As the GGA is stochastic, identical makespans are not guaranteed across independent runs.

### 9. Standalone Example Results in Google Colab

The file `colab results from github experiment.py.docx` contains the complete execution record of an independent run of `github experiment.py` in Google Colab.

The experiment used PSPLIB instance `j12031_8.sm` with a search limit of approximately 50,000 evaluated schedules.

**Recorded results:**

| Item | Result |
|---|---|
| Benchmark instance | `j12031_8.sm` |
| Execution environment | Google Colab |
| Best makespan | **198** |
| Evaluated schedules | 50,009 |
| Computational time | Approximately 3,458 seconds |
| Termination | Search evaluation limit |

During execution, the algorithm progressively improved its best makespan, including improvements from 201 to 200, 199, and finally 198.

The complete execution record includes intermediate search results and the final scheduling solution.

The standalone example and its execution record are provided primarily to demonstrate that the implementation can be executed independently. This single stochastic run is not intended to establish the overall solution quality or statistical performance of the proposed method. Comprehensive experimental evaluation is presented in the accompanying manuscript.


### 10. Benchmark Data Loading for J30, J60, and J120

The experimental evaluation includes benchmark instances from the PSPLIB J30, J60, and J120 families.

The original GGA implementation uses different data-loading functions for different benchmark families. In particular, the J30 and J60 instances require their corresponding loading functions ('load function for j30' and 'load function for j60') rather than directly using the J120 loading procedure.

The standalone executable example (`github experiment.py`) is configured specifically for the J120 instance `j12031_8.sm`, whose benchmark data are embedded in the source code.

The supplied implementation is configured for J120 instances. Reproducing experiments on J30 and J60 requires the corresponding benchmark data-loading functions, PSPLIB instance files and relevant reference-value files, while the core GGA search framework remains unchanged. the data-loading procedure must be adapted to the selected benchmark family.

The standalone J120 example is intended to demonstrate the implementation and execution of the proposed algorithm, rather than to reproduce the complete benchmark evaluation across all instance families.
