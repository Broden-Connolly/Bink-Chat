from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from chat.models import Message, Room
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


# Create your views here.
def home(request):
    return render(request, 'home.html')  

def room(request, room): 
    
    username = request.GET.get('username') 
    room_details = Room.objects.get(name=room) 
    return render(request, 'room.html', {
        'username': username,  
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.user.username
    password = request.POST['password']  # Use get() method to avoid MultiValueDictKeyError
    if Room.objects.filter(name=room, passw=password).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        return HttpResponse('Incorrect Password or Room does not exist')

def createRoom(request):
    room_name = request.POST['room_name']
    password = request.POST['password']  # Retrieve the password from request.POST dictionary

    if Room.objects.filter(name=room_name).exists():
        return HttpResponse('Room already exists')
    else:
        chat_room = Room.objects.create(name=room_name, passw=password)  # Save the password to the database
        chat_room.save()
        return checkview(request)
    
def send(request):
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


    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

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

    
    new_message = Message.objects.create(value=encrypted, user=username, room=room_id, bits = key)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    print(messages)
    if messages.exists():
        for i in range(len(messages)):
            print(messages.values_list('value')[i])
        encrypted = messages.values_list('value')[0]
        key = messages.values_list('bits')[0]
        key = key[0]
        c = encrypted[0].split(' ')
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
        print (ascii_string)
        # messages.update(value = ascii_string)
        messages = list(messages.values())
        print (messages)
        messages[0]['value'] = ascii_string
    return JsonResponse({"messages":messages})