import threading

from termcolor import colored, cprint
from agent import start_agent, generate_report
from snmp_requests import *
from database import DataBase
import os


def print_colored(description, text, color, args):
    print('\t', description, ': ', end='')
    cprint(text, color, attrs=args)


class Devices:

    def __init__(self):
        self.devices_database = DataBase()

    def list_devices(self):
        devices_status = {}
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            for device in devices:
                response = snmp_get(devices[device]['community'], devices[device]['ip_address'], '1.3.6.1.2.1.1.1.0')
                devices_status[device] = response

            counter = 0

            for device in devices:
                print("_______________________________________________________________")
                print(str(counter) + ".-")
                counter += 1
                print_colored('Dispositivo', devices[device]['host_name'], 'green', ['bold'])
                print_colored('Dirección IP', devices[device]['ip_address'], 'green', ['bold'])
                if devices_status[device] is not None:
                    print_colored('Estado', 'UP', 'green', ['bold'])
                    num_interfaces = snmp_get(devices[device]['community'], devices[device]['ip_address'],
                                              '1.3.6.1.2.1.2.1.0')
                    print_colored('No. interfaces', num_interfaces, 'green', ['bold'])
                    active_connections = snmp_walk(devices[device]['community'], devices[device]['ip_address'],
                                                '1.3.6.1.2.1.6.13.1.4')
                    active_connections_ports = snmp_walk(devices[device]['community'], devices[device]['ip_address'],
                                                  '1.3.6.1.2.1.6.13.1.3')
                    for i in range(len(active_connections)):
                        if active_connections[i] != "127.0.0.1" and active_connections[i] != "0.0.0.0":
                            if active_connections_ports[i] == "22":
                                print_colored('\tSSH cliente: ', active_connections[i], 'green', ['bold'])
                else:
                    print_colored('Estado', 'DOWN', 'red', ['bold'])
                    print_colored('No. interfaces', 'Desconocido', 'red', ['bold'])

    def add_devices(self):
        print()
        host_name = input('Ingresa el nombre del dispositivo: ')
        ip_address = input('Ingresa la dirección ip del dispositivo: ')
        snmp_version = input('Ingresa la version de SNMP configurada en el dispositivo: ')
        community = input('Ingresa la comunidad configurada en el dispositivo: ')
        port = input('Ingresa el puerto configurado en el dispositivo (161 default): ' or '161')

        os.system('mkdir data/devices_files/' + ip_address)

        self.devices_database.insert(host_name, ip_address, snmp_version, community, port)

        new_agent = threading.Thread(target=start_agent, args=(host_name, ip_address, community, port))
        new_agent.start()

        print(colored('\nDispositivo agregado exitosamente.', 'green'))

    def delete_devices(self):
        ip_address = input('Ingresa la dirección ip del dispositivo que desea eliminar: ')
        self.devices_database.delete(ip_address)
        os.system('rm -r data/devices_files/' + ip_address)
        print(colored('\nDispositivo eliminado exitosamente.', 'green'))

    def generate_report(self):
        ip_address = input('Ingresa la dirección ip del servidor SSH: ')
        ssh_ip_address = input('Ingresa la dirección ip del cliente SSH que desea obtener su reporte: ')
        minutos = input('Ingrese el rango de minutos sobre el cual desea generar el reporte: ')
        generate_report(self.devices_database.read(ip_address)["ip_address"],
                        self.devices_database.read(ip_address)["community"],
                        minutos,
                        self.devices_database.read(ip_address)["host_name"],
                        ssh_ip_address)

# number of interfaces: 1.3.6.1.2.1.2.1.0
# interfaces name:      1.3.6.1.2.1.2.2.1.2.#
# multicast packages:   1.3.6.1.2.1.2.2.1.12.#
# ipv4 datagrams:       1.3.6.1.2.1.4.10.0
# mensajes icmp:        1.3.6.1.2.1.5.1.0
# retransmitted:        1.3.6.1.2.1.6.12.0
# retransmitted:        1.3.6.1.2.1.6.12.0
# output datagrams:     1.3.6.1.2.1.4.10.0
