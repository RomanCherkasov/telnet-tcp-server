#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket

SERVER_ADDRESS = ('localhost', 8687)
MAX_CONN = 10

INPUTS = list()
OUTPUTS = list()

def nb_socket():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONN)
    return server

def handle_readables(readables, server):
    for resource in readables:
        # проверяем от сервера ли событие
        if resource is server:
            connection, client_addres = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
            print(f'New connection from {client_addres}')
        else:
            data = ''
            try:
                data = resource.recv(1024)
            except ConnectionResetError:
                pass

            if data:
                print(f'data: {str(data)}')
                if resource not in OUTPUTS:
                    OUTPUTS.append(resource)
            else:
                clear_resource(resource)

def clear_resource(resource):
    # чистим ресурсы
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)

    resource.close()

    # print(f'connection closing {str(resource)}')

def handle_writables(writables):
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

