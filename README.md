# Bink-Chat

A Django messaging app with end-to-end encryption using the BB84 quantum key distribution protocol and AES.

---

## Overview

Bink-Chat lets users send encrypted messages over a web interface. Encryption keys are generated using the BB84 quantum key distribution (QKD) protocol, simulated locally with IBM's Qiskit library. Messages are then encrypted with those keys before being sent.

This was a high school project built to learn how quantum cryptography works in practice and to see if it could be wired into a real web application.

---

## How It Works

**Key Generation (BB84)**
1. The sender generates a random bit string and a random basis string, then encodes each bit as a qubit in either the computational or Hadamard basis.
2. The recipient independently picks a random basis and measures each incoming qubit.
3. The two parties compare their bases (not the bits themselves) and keep only the bits where they matched. That subset becomes the shared key.
4. The quantum circuit runs on Qiskit's `qasm_simulator` backend.

**Message Encryption**
- Messages are XOR-encrypted with the key produced by BB84.
- A separate AES module (EAX mode, via PyCryptodome) is also included as a more production-ready encryption option.

**Web App**
- Django backend with user accounts, login/logout, and a real-time chat interface.
- Vercel deployment config is included in `chat-test/`.

---

## Tech Stack

- **Python / Django** - backend and web framework
- **Qiskit** - quantum circuit simulation for BB84
- **PyCryptodome** - AES encryption
- **SQLite** - database
- **Django REST Framework** - API layer
- **Websockets** - real-time messaging
- **HTML/CSS** - frontend templates

---

## Project Structure

```
Bink-Chat/
├── Chat_login/          # Main Django app with auth and chat
│   ├── accounts/        # User registration and login
│   ├── chat/            # Messaging logic and views
│   └── templates/       # HTML templates
├── encryption/
│   ├── aes_encryption.py        # AES-EAX encryption/decryption
│   └── quant_test/
│       └── encryption_test.py   # BB84 QKD implementation (Qiskit)
├── chat-test/           # Earlier prototype
└── Django_Login_Test/   # Auth prototype
```

---

## Setup

**Requirements:** Python 3.9+, pip

```bash
git clone https://github.com/Broden-Connolly/Bink-Chat.git
cd Bink-Chat/chat-test
pip install django qiskit pycryptodome djangorestframework websockets
python manage.py migrate
python manage.py runserver
```

To run the BB84 key generation on its own:

```bash
cd encryption/quant_test
pip install qiskit
python encryption_test.py
```

---

## Notes

The BB84 simulation uses seeded random values, so the key is deterministic rather than truly random. On real quantum hardware or via the IBM Quantum cloud API, you would draw that randomness from actual quantum measurements instead.

The `requirements.txt` is a full system pip freeze from a Linux environment and pulls in a lot of unrelated packages. The install command above lists the only dependencies this project actually needs.
