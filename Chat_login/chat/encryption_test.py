import random
from qiskit import execute, Aer, IBMQ
from qiskit.tools import *
from qiskit.visualization import *
from qiskit import *

def key_basis_generation(num_qubits, p):
    random.seed(p)
    key = str('{0:008b}'.format(random.getrandbits(num_qubits)))
    bases = str('{0:008b}'.format(random.getrandbits(num_qubits)))
    return key, bases

def gen_q(circuit, k, b):
    for i in range(len(k)):
        if k[i] == '0' and b[i] == '1':
            circuit.h(i)
        elif k[i] == '1' and b[i] == '0':
            circuit.x(i)
        elif k[i] == '1' and b[i] == '1':
            circuit.x(i)
            circuit.h(i)
    return circuit 

def recip_measurement(circuit, b):
    for i in range(len(b)):
        if b[i] == '0':
            circuit.measure(i,i)
        else:
            circuit.h(i)
            circuit.measure(i,i)
    return circuit

def recip_meas_qubit(circ):
    # Use Aer's qasm_simulator
    
    backend_sim = Aer.get_backend('qasm_simulator')
    
    # Execute the circuit on the qasm simulator.
    # The number of repeats on the circuit is one, which is default
    # Depending on the amount of noise in a real system, this may increase
    job_sim = execute(circ, backend_sim, shots=1)

    # Grab the results from the job.
    result_sim = job_sim.result()
    counts = result_sim.get_counts(circ)
    output = list(counts.keys())[0] 
           
    return output

def recip_generates_key(a_b, b_b, output):
    key = ''
    for i in range(len(b_b)):
        if a_b[i] == b_b[i]:
            key+=str(output[i])            
    return key

def to_binary(text):
    return " ".join(f"{ord(i):08b}" for i in text)

# Sender generates encoded key and basis
Sender_en_key, Sender_basis = key_basis_generation(8,1020)

# Recipient generates the basis
Truncate, Recip_basis = key_basis_generation(8, 200)

# Create circuit with 8 quantum bits and 8 classical bits
circuit = QuantumCircuit(8,8)

# Sender creates quantum circuit according key & basis
circuit = gen_q(circuit, Sender_en_key, Sender_basis)
circuit.barrier()

# Recipient creates measurement setting for the qubit according to basis
circuit = recip_measurement(circuit, Recip_basis)

# Recipient recieves the qubits and performs measurement 
output = recip_meas_qubit(circuit)

# Recipient compares the output with sender's basis and generates the key
key = recip_generates_key(Sender_basis, Recip_basis, output)

# Sender creates message to encrypt
message = "Encrpyted and whatnot and such"
mess_binary = to_binary(message)
mess_binary = mess_binary.split(' ')
mess_binary = [i for i in mess_binary if i]
encrypted = ""
# padding key string
key = key.rjust(len(mess_binary[0]), "0")
for k in range(len(mess_binary)):
    n = int(len(mess_binary[k])/len(key))
    j = 0
    for i in mess_binary[k]:
        p = int(i)^int(key[j])
        encrypted += str(p) 
        j+=1
        if len(key) == j:
            j=0
    encrypted += ' '

# Split encrypted bits
c = encrypted.split(' ')
c = [i for i in c if i]

# Recipient gets encoded bits
decrypted = ""
# padding key string
key = key.rjust(len(c[0]), "0")
for k in range(len(c)):
    n = int(len(c[k])/len(key))
    j = 0
    for i in c[k]:
        p = int(i)^int(key[j])
        decrypted += str(p) 
        j+=1
        if len(key) == j:
            j=0
    decrypted += ' '

# Converting the bit string to a text
binary_values = decrypted.split()
ascii_string = ""
for binary_value in binary_values:
    an_integer = int(binary_value, 2)
    ascii_character = chr(an_integer)
    ascii_string += ascii_character
print('The message: ', ascii_string)