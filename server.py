import socket
import threading
import time

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# Listas para armazenar conexões e mensagens
conexoes = []
mensagens = []
clientes = {}

# Função para enviar mensagens antigas para um cliente específico
def enviar_mensagem_individual(cliente):
    for mensagem in mensagens:
        if mensagem['dst'] == cliente['id']:
            cliente['conn'].send(mensagem['data'].encode())

# Função para enviar uma mensagem para todos os clientes
def enviar_mensagem_todos():
    for cliente in conexoes:
        for mensagem in mensagens:
            cliente['conn'].send(mensagem['data'].encode())

# Função para lidar com clientes
def handle_clientes(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    nome = conn.recv(1024).decode()
    
    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            break
        
        # Registro de cliente
        if msg.startswith("01"):
            cliente_id = str(len(clientes) + 1).zfill(13)
            clientes[cliente_id] = conn
            conn.send(f"02{cliente_id}".encode())
        
        # Conexão de cliente
        elif msg.startswith("03"):
            cliente_id = msg[2:15]
            if cliente_id in clientes:
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "id": cliente_id,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao)
                enviar_mensagem_individual(mapa_da_conexao)
        
        # Envio de mensagem
        elif msg.startswith("05"):
            src = msg[2:15]
            dst = msg[15:28]
            timestamp = msg[28:38]
            data = msg[38:]
            mensagem = {
                "src": src,
                "dst": dst,
                "timestamp": timestamp,
                "data": data
            }
            mensagens.append(mensagem)
            for cliente in conexoes:
                if cliente['id'] == dst:
                    cliente['conn'].send(f"06{src}{dst}{timestamp}{data}".encode())
                    break
        
        # Mensagem de chat (antigo)
        elif msg.startswith("msg="):
            mensagem_separada = msg.split("=")
            mensagem = nome + "=" + mensagem_separada[1]
            mensagens.append(mensagem)
            enviar_mensagem_todos()

# Função para iniciar o servidor
def start():
    print("[INICIANDO] Sockets com python")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

# Inicia o servidor
start()
