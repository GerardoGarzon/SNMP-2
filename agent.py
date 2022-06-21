import time
from os.path import exists
from rrd_database import *
from snmp_requests import *
from pdf_file import create_report
import os

INTERFACE_NAMES = '1.3.6.1.2.1.2.2.1.2'
# BLOQUE 1
TCP_IN_SEGS = '1.3.6.1.2.1.6.10.0'
TCP_OUT_SEGS = '1.3.6.1.2.1.6.11.0'

TITLES_OID = [
    "Total de segmentos recibidos \nincluyendo los que tienen errores",
    "Total de segmentos enviados \nincluyendo los que tienen errores",
]


def start_agent(host_name, ip_address, community, port):
    databases(ip_address, community)
    update_agent(ip_address, community)


def update_agent(ip_address, community):
    while exists(os.getcwd() + "/data/devices_files/" + ip_address):
        update_database(ip_address, "tcpInSegs", "N:" + snmp_get(community, ip_address, TCP_IN_SEGS))
        update_database(ip_address, "tcpOutSegs", "N:" + snmp_get(community, ip_address, TCP_OUT_SEGS))

        time.sleep(1)


def databases(ip_address, community):
    create_database(ip_address, "tcpInSegs", 0)
    create_database(ip_address, "tcpOutSegs", 0)


def generate_report(ip_address, community, minutos, device_name, ssh_client_ip):
    interfaces_name = snmp_walk(community, ip_address,'1.3.6.1.2.1.2.2.1.2')
    num_interfaces = len(interfaces_name)
    sys_location = snmp_walk(community, ip_address, '1.3.6.1.2.1.1.6')[0]
    seconds = snmp_get(community, ip_address, '1.3.6.1.2.1.1.3.0')
    up_time = str(datetime.timedelta(seconds=int(seconds)))
    version = snmp_walk(community, ip_address, '1.3.6.1.2.1.1.1')[0]

    last_input = graph_detection(ip_address, "tcpInSegs", 0, minutos, TITLES_OID[0], ['Segmentos recibidos'])['print[0]']
    last_output = graph_detection(ip_address, "tcpOutSegs", 0, minutos, TITLES_OID[1], ['Segmentos enviados'])['print[0]']

    logo = 'linux_logo.png'
    if version.split(' ')[0] == 'Darwin':
        logo = 'data/logos/macos_logo.png'
    elif version.split(' ')[0] == 'Windows':
        logo = 'data/logos/windows_logo.png'
    else:
        logo = 'data/logos/linux_logo.png'

    create_report(version.split(' ')[0], version.split(' ')[2], logo, sys_location, str(num_interfaces), up_time, community, ip_address, 'data/devices_files/' + ip_address + '/')
    create_accounting_report(version.split(' ')[0], 'Accounting server', datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Radius', community, ip_address, 'data/devices_files/' + ip_address + '/', ssh_client_ip, last_input, last_output)
    os.system('open data/devices_files/' + ip_address + '/reporte_' + ip_address + '.pdf')
    os.system('open data/devices_files/' + ip_address + '/accounting_report_' + ip_address + '.txt')


def create_accounting_report(name, description, date, defaultProtocol, community, ip_address, device_path, ssh_client_ip, last_input, last_output):
    f = open(device_path + "accounting_report_" + ip_address + ".txt", "w")
    f.write('Version: 1\n')
    f.write('Device: ' + name + '\n')
    f.write('Description: ' + description + '\n')
    f.write('Date: ' + date + '\n')
    f.write('Default protocol: ' + defaultProtocol + '\n')
    f.write('\n\n')
    f.write('RDate: ' + date + '\n')
    f.write('# NAS-IP-ADDRESS\n')
    f.write('4: ' + ssh_client_ip + '\n')
    f.write('# NAS-PORT' + '\n')
    f.write('5: ' + get_nas_port(community, ip_address, ssh_client_ip) + '\n')
    f.write('# LOGIN-IP-HOST' + '\n')
    f.write('14: ' + ip_address + '\n')
    f.write('# LOGIN-TCP-PORT' + '\n')
    f.write('16: 22' + '\n')
    # Acct-Input-Packets
    f.write('# Acct-Input-Packets' + '\n')
    f.write('47: ' + last_input + '\n')
    f.write('# Acct-Output-Packets' + '\n')
    f.write('48: ' + last_output + '\n')
    f.close()


def get_nas_port(community, ip_address, ssh_client):
    list_ip = snmp_walk(community, ip_address, '1.3.6.1.2.1.6.13.1.4')
    index = list_ip.index(ssh_client)
    list_ports = snmp_walk(community, ip_address, '1.3.6.1.2.1.6.13.1.5')
    return list_ports[index]