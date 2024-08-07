import socket
import threading
import time

# Definindo a porta de comunicação e o formato de codificação das mensagens
PORT = 5050
FORMATO = 'utf-8'
# Endereço IP do servidor
SERVER = "192.168.88.12"
# Endereço completo (IP e porta) do servidor
ADDR = (SERVER, PORT)

# Criando o socket do cliente usando IPv4 (AF_INET) e TCP (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectando o cliente ao servidor especificado
client.connect(ADDR)

# Função para lidar com as mensagens recebidas do servidor
def handle_mensagens():
    while True:
        # Recebe a mensagem do servidor
        msg = client.recv(1024).decode()
        # Divide a mensagem em partes usando "=" como delimitador
        mensagem_splitada = msg.split("=")
        # Imprime a mensagem no formato "nome: mensagem"
        print(mensagem_splitada[1] + ": " + mensagem_splitada[2])

# Função para enviar uma mensagem codificada para o servidor
def enviar(mensagem):
    client.send(mensagem.encode(FORMATO))

# Função para ler uma mensagem do usuário e enviá-la ao servidor
def enviar_mensagem():
    mensagem = input()
    enviar("msg=" + mensagem)

# Função para ler o nome do usuário e enviá-lo ao servidor
def enviar_nome():
    nome = input('Digite seu nome: ')
    enviar("nome=" + nome)

# Função para iniciar o envio de mensagens
def iniciar_envio():
    enviar_nome()  # Primeiro, envia o nome do usuário
    while True:
        enviar_mensagem()  # Em seguida, envia mensagens continuamente

# Função principal para iniciar o cliente
def iniciar():
    # Cria e inicia uma thread para lidar com as mensagens recebidas
    thread1 = threading.Thread(target=handle_mensagens)
    # Cria e inicia uma thread para lidar com o envio de mensagens
    thread2 = threading.Thread(target=iniciar_envio)
    thread1.start()
    thread2.start()

# Inicia o cliente
iniciar()
