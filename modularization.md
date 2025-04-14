# What is Solaris?
A general framework for testing graph state verification protocols with different backends and integrating different protocols.

# What are the modules?
## Create graph state
Creates $N$ copies of the desired graph state as indicated by its adjacency matrix. Takes as input the adjacency matrix plus optionally the desired number of copies $N$ 

* Input : Adjacency matrix of desired graph state
* Output : A quantum circuit to prepare this state

** later : N outputs of the same graph? 

## Create stabilizers
All quantum verification protocols known to the authors rely on choosing stabilizers of the desired graph state at random and then preparing the circuit to measure them. This module takes in the adjacency matrix and generates the generator table of stabilisers, generates one stabilizer chosen at random or the entire set of $2^n$ stabilizers. $n$ denotes the number of nodes in the graph or qubits or number of parties in the network.

## Test protocol

Implementation of different protocols in quantum comunication to test them. Noise models and environmental conditions can be put in here.