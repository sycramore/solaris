import numpy as np
import qiskit
from itertools import product


print(qiskit.__version__)



def generate_graph_state(adjacency_matrix):
    """
    Generate a graph state based on the given adjacency matrix.

    Args:
        adjacency_matrix (np.ndarray): A square matrix where a non-zero entry (i, j) indicates an edge between qubit i and qubit j.

    Returns:
        QuantumCircuit: A quantum circuit representing the graph state.
    """
    num_qubits = len(adjacency_matrix)
    qc = qiskit.QuantumCircuit(num_qubits)

    # Apply Hadamard gates to all qubits
    for i in range(num_qubits):
        qc.h(i)

    # Apply controlled-phase gates based on the adjacency matrix
    for i in range(num_qubits):
        for j in range(num_qubits):
            if adjacency_matrix[i, j] != 0:
                qc.cz(i, j)

    return qc

def generate_stabilizer_generators(adjacency_matrix):
    """
    Generate the stabilizers for a graph state based on the given adjacency matrix.

    Args:
        adjacency_matrix (np.ndarray): A square matrix where a non-zero entry (i, j) indicates an edge between qubit i and qubit j.

    Returns:
        list: A list of stabilizer strings.
    """
    num_qubits = len(adjacency_matrix)
    generators = []

    for i in range(num_qubits):
        generator = ['I'] * num_qubits
        generator[i] = 'X'
        for j in range(num_qubits):
            if adjacency_matrix[i, j] != 0:
                generator[j] = 'Z' if generator[j] == 'I' else 'I'
        generators.append(''.join(generator))

    return generators


# Pauli group multiplication table with phases
pauli_mul_with_phase = {
    ('I', 'I'): ('I', 1),
    ('I', 'X'): ('X', 1),
    ('I', 'Y'): ('Y', 1),
    ('I', 'Z'): ('Z', 1),
    ('X', 'I'): ('X', 1),
    ('X', 'X'): ('I', 1),
    ('X', 'Y'): ('Z', 1j),
    ('X', 'Z'): ('Y', -1j),
    ('Y', 'I'): ('Y', 1),
    ('Y', 'X'): ('Z', -1j),
    ('Y', 'Y'): ('I', 1),
    ('Y', 'Z'): ('X', 1j),
    ('Z', 'I'): ('Z', 1),
    ('Z', 'X'): ('Y', 1j),
    ('Z', 'Y'): ('X', -1j),
    ('Z', 'Z'): ('I', 1),
}

def pauli_string_multiply_with_phase(p1, p2):
    """Multiply two Pauli strings with phase consideration."""
    phase = 1
    result = []
    for a, b in zip(p1, p2):
        r, p = pauli_mul_with_phase[(a, b)]
        result.append(r)
        phase *= p
    return ''.join(result), phase

def generate_stabilizer_group_with_phase(generators):
    """Creates entire stabilizer group from generators."""
    n = len(generators)
    group = dict()
    for coeffs in product([0, 1], repeat=n):
        if all(c == 0 for c in coeffs):
            result = 'I' * len(generators[0])
            phase = 1
        else:
            result = 'I' * len(generators[0])
            phase = 1
            for i, c in enumerate(coeffs):
                if c:
                    result, p = pauli_string_multiply_with_phase(result, generators[i])
                    phase *= p
        group[result, phase] = True  # Set nutzen via dict keys
    return sorted(group.keys())

def main():
    # Example adjacency matrix for a 3-qubit graph state
    adjacency_matrix = np.array([[0, 1, 1],
                                  [1, 0, 1],
                                  [1, 1, 0]])

    # Generate the graph state circuit
    qc = generate_graph_state(adjacency_matrix)
    print("Quantum Circuit for Graph State:")
    print(qc)

    # Generate the stabilizers
    generators = generate_stabilizer_generators(adjacency_matrix)
    print("Stabilizers:")
    for g in generators:
        print(g)

if __name__ == "__main__":
    main()
# The code generates a graph state based on an adjacency matrix and computes the stabilizers for that graph state.
# The adjacency matrix is a square matrix where a non-zero entry (i, j) indicates an edge between qubit i and qubit j.
# The graph state is generated using Hadamard gates and controlled-phase gates.
# The stabilizers are generated based on the adjacency matrix, where each stabilizer corresponds to a qubit in the graph state.
# The stabilizers are represented as strings of 'X', 'Z', and 'I' (identity) operators.

# The adjacency matrix can be modified to generate different graph states.
# The code uses the Qiskit library to create quantum circuits and manipulate qubits.
# The generated quantum circuit can be executed on a quantum simulator or a real quantum computer using Qiskit.
# The stabilizers can be used to analyze the properties of the graph state and perform measurements.
# The code is structured into functions for better organization and reusability.
# The main function serves as the entry point for the script, allowing for easy testing and execution.
# The adjacency matrix is defined as a NumPy array for efficient numerical operations.
# The code is compatible with Python 3 and requires the Qiskit library to be installed.
# The Qiskit library provides a comprehensive set of tools for quantum computing, including circuit creation, simulation, and execution.
# The code can be extended to include additional features, such as visualizing the quantum circuit or analyzing the stabilizers in more detail.
# The generated quantum circuit can be visualized using Qiskit's built-in visualization tools, such as the circuit drawer.
# The stabilizers can be analyzed to understand the symmetries and properties of the graph state.
# The code can be integrated into larger quantum computing projects or used as a standalone tool for generating and analyzing graph states.

