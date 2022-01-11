import select
import socket
from parsing_and_output import parse

SERVER_ADDRESS = ('localhost', 8686)
MAX_CONN = 10

INPUTS = list()
OUTPUTS = list()

def nb_socket() -> classmethod:

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONN)
    return server

def handle_readables(readables, server) -> None:
    for resource in readables:
        # проверяем от сервера ли событие
        if resource is server:
            connection, client_addres = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
        else:
            data = ''
            try:
                data = resource.recv(1024)
            except ConnectionResetError:
                pass

            if data:
                parse(data)
                if resource not in OUTPUTS:
                    OUTPUTS.append(resource)
            else:
                clear_resource(resource)

def clear_resource(resource) -> None:
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)
    resource.close()

def handle_writables(writables) -> None:
    for resource in writables:
        try:
            resource.send(bytes('Data accepted!\n', encoding='UTF-8'))
            clear_resource(resource)
        except OSError:
            clear_resource(resource)

if __name__ == '__main__':
    server_socket = nb_socket()
    INPUTS.append(server_socket)
    print('Server is running')
    try:
        while INPUTS:
            readables, writables, exceptoinal = select.select(INPUTS, OUTPUTS, INPUTS)
            handle_readables(readables, server_socket)
            handle_writables(writables)
    except KeyboardInterrupt:
        clear_resource(server_socket)
        print('Server stoped!')

