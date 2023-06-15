from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx

# Define number of nodes
nodes = int(input("Nodes Amount: "))

# Create graph matrix
graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)]

# Create edges between nodes based on quantum circuit result
bitsUsed = int(((nodes * nodes) - nodes) / 2)
qr = QuantumRegister(bitsUsed)
cr = ClassicalRegister(bitsUsed)
circuit = QuantumCircuit(qr, cr)

#Tuple & Def implementaion

for i in range(0, bitsUsed, 2):
    circuit.h(qr[i])

for i in range(0, bitsUsed, 2):
    if i + 1 <bitsUsed:
        circuit.cx(qr[i], qr[i + 1])

circuit.measure(qr, cr)

circuit.draw()
print(circuit)

simulator = Aer.get_backend('qasm_simulator')
job = execute(circuit, simulator, shots=1)
job_monitor(job)
counts = job.result().get_counts()

listOfBits = [int(str(counts)[int(i + 2)]) for i in range(bitsUsed)]

# Create graph from matrix and edges
F = nx.Graph()
for i in range(nodes):
    F.add_node(i)

counter = 0
for i in range(nodes):
    for j in range(i):
        graphMatrix[j][i] = listOfBits[counter]
        if listOfBits[counter] == 1:
            F.add_edge(i, j)
        counter += 1

for x in range(nodes):
    for y in range(nodes):
        print(graphMatrix[x][y], end=" ")
    print()

print("Number of edges:", listOfBits.count(1), "| Percent: ", (int)((listOfBits.count(1) / len(listOfBits)) * 100), "%")
print("Number of non-edges:", listOfBits.count(0), "| Percent: ", (int)((listOfBits.count(0) / len(listOfBits))  * 100), "%")

# Draw graph
plt.figure()
pos = nx.spring_layout(F)
labels = nx.get_edge_attributes(F,'weight')
nx.draw(F, pos, with_labels=True)
nx.draw_networkx_edge_labels(F, pos, edge_labels=labels)
plt.show()