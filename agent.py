import time
from os.path import exists
from rrd_database import *
from snmp_requests import *
from pdf_file import create_report
import os
import subprocess


INTERFACE_NAMES = '1.3.6.1.2.1.2.2.1.2'
# BLOQUE 1
IF_IN_UCAST_PKTS = '1.3.6.1.2.1.2.2.1.11'
IP_IN_RECEIVES = '1.3.6.1.2.1.4.3.0'
ICMP_OUT_ECHO = '1.3.6.1.2.1.5.21.0'
TCP_IN_SEGS = '1.3.6.1.2.1.6.10.0'
UDP_OUT_DATAGRAMS = '1.3.6.1.2.1.7.4.0'
# BLOQUE 2
IF_IN_NUCAST_PKTS = '1.3.6.1.2.1.2.2.1.12'
IP_IN_DELIVERS = '1.3.6.1.2.1.4.9.0'
ICMP_OUT_ECHO_REPS = '1.3.6.1.2.1.5.22.0'
TCP_OUT_SEGS = '1.3.6.1.2.1.6.11.0'
UDP_NO_PORTS = '1.3.6.1.2.1.7.2.0'
# BLOQUE 3
IF_OUT_NUCAST_PKTS = '1.3.6.1.2.1.2.2.1.18'
IP_OUT_REQUESTS = '1.3.6.1.2.1.4.10.0'
ICMP_ECHO_REQ = '1.3.6.1.2.1.5.1.0'
TCP_RETRANS_SEGS = '1.3.6.1.2.1.6.12.0'
UDP_OUT_DATAGRAMS_DEVICE = '1.3.6.1.2.1.7.4.0'

TITLES_OID = [
    "Paquetes unicast que ha recibido una interfaz\n",
    "Paquetes recibidos a protocolos ipv4 \nincluyendo los que tienen errores\n",
    "Mensajes ICMP echo que ha enviado el agente\n",
    "Segmentos recibidos incluyendo los \nque se han recibido con errores\n",
    "Datagramas entregados a usuarios UDP\n",
    "Paquetes multicast que ha recibido una interfaz\n",
    "Paquetes recibidos exitosamente entregados a protocolos IPV4\n",
    "Mensajes de respuesta ICMP que ha enviado el agente\n",
    "Segmentos enviados, incluyendo los de las \nconexiones actuales pero excluyendo los \nque contienen solamente octetos retransmitidos\n",
    "Datagramas recibidos que no pudieron \nser entregados por cuestiones \ndistintas a la falta de aplicacion en el puerto destino\n",
    "Paquetes multicast que ha enviado una interfaz\n",
    "Paquetes IPV4 que los protocolos locales de usuarios de IPV4 \nsuministraron a IPV4 en las solicitudes de transmisión\n",
    "Mensajes ICMP que ha recibido el agente\n",
    "Segmentos retransmitidos; es decir, el número \nde segmentos TCP transmitidos que contienen \nuno o más octetos transmitidos previamente.\n",
    "Datagramas enviados por el dispositivo.\n"
]


def start_agent(host_name, ip_address, community, port):
    databases(ip_address, community)
    update_agent(ip_address, community)


def update_agent(ip_address, community):
    while exists(os.getcwd() + "/data/devices_files/" + ip_address):
        # ifInUcastPkts
        in_ucast = snmp_walk(community, ip_address, IF_IN_UCAST_PKTS)
        in_ucast_value = "N"
        for value in in_ucast:
            in_ucast_value += ":" + value
        update_database(ip_address, "ifInUcastPkts", in_ucast_value)
        # ifInNUcastPkts
        in_nucast = snmp_walk(community, ip_address, IF_IN_NUCAST_PKTS)
        in_nucast_value = "N"
        for value in in_nucast:
            in_nucast_value += ":" + value
        update_database(ip_address, "ifInNUcastPkts", in_nucast_value)
        # ifOutNUcastPkts
        out_nucast = snmp_walk(community, ip_address, IF_OUT_NUCAST_PKTS)
        out_nucast_value = "N"
        for value in out_nucast:
            out_nucast_value += ":" + value
        update_database(ip_address, "ifInNUcastPkts", out_nucast_value)

        update_database(ip_address, "ipInReceives", "N:" + snmp_get(community, ip_address, IP_IN_RECEIVES))
        update_database(ip_address, "icmpOutEchos", "N:" + snmp_get(community, ip_address, ICMP_OUT_ECHO))
        update_database(ip_address, "tcpInSegs", "N:" + snmp_get(community, ip_address, TCP_IN_SEGS))
        update_database(ip_address, "udpOutDatagrams", "N:" + snmp_get(community, ip_address, UDP_OUT_DATAGRAMS))
        update_database(ip_address, "ipInDelivers", "N:" + snmp_get(community, ip_address, IP_IN_DELIVERS))
        update_database(ip_address, "icmpOutEchoReps", "N:" + snmp_get(community, ip_address, ICMP_OUT_ECHO_REPS))
        update_database(ip_address, "tcpOutSegs", "N:" + snmp_get(community, ip_address, TCP_OUT_SEGS))
        update_database(ip_address, "udpNoPorts", "N:" + snmp_get(community, ip_address, UDP_NO_PORTS))
        update_database(ip_address, "ipOutRequests", "N:" + snmp_get(community, ip_address, IP_OUT_REQUESTS))
        update_database(ip_address, "icmpEchoReq", "N:" + snmp_get(community, ip_address, ICMP_ECHO_REQ))
        update_database(ip_address, "tcpRetransSegs", "N:" + snmp_get(community, ip_address, TCP_RETRANS_SEGS))
        update_database(ip_address, "udpOutDatDevice", "N:" + snmp_get(community, ip_address, UDP_OUT_DATAGRAMS_DEVICE))

        time.sleep(1)


def databases(ip_address, community):
    create_database(ip_address, "ifInUcastPkts", len(snmp_walk(community, ip_address, IF_IN_UCAST_PKTS)))
    create_database(ip_address, "ifInNUcastPkts", len(snmp_walk(community, ip_address, IF_IN_NUCAST_PKTS)))
    create_database(ip_address, "ifOutNUcastPkts", len(snmp_walk(community, ip_address, IF_OUT_NUCAST_PKTS)))
    create_database(ip_address, "ipInReceives", 0)
    create_database(ip_address, "icmpOutEchos", 0)
    create_database(ip_address, "tcpInSegs", 0)
    create_database(ip_address, "udpOutDatagrams", 0)
    create_database(ip_address, "ipInDelivers", 0)
    create_database(ip_address, "icmpOutEchoReps", 0)
    create_database(ip_address, "tcpOutSegs", 0)
    create_database(ip_address, "udpNoPorts", 0)
    create_database(ip_address, "ipOutRequests", 0)
    create_database(ip_address, "icmpEchoReq", 0)
    create_database(ip_address, "tcpRetransSegs", 0)
    create_database(ip_address, "udpOutDatDevice", 0)


def generate_report(ip_address, community, minutos, device_name):
    interfaces_name = snmp_walk(community, ip_address,'1.3.6.1.2.1.2.2.1.2')
    num_interfaces = len(interfaces_name)
    sys_location = snmp_walk(community, ip_address, '1.3.6.1.2.1.1.6')[0]
    seconds = snmp_get(community, ip_address, '1.3.6.1.2.1.1.3.0')
    up_time = str(datetime.timedelta(seconds=int(seconds)))
    version = snmp_walk(community, ip_address, '1.3.6.1.2.1.1.1')[0]

    graph_detection(ip_address, "ifInUcastPkts", len(snmp_walk(community, ip_address, IF_IN_UCAST_PKTS)), minutos, TITLES_OID[0], interfaces_name)
    graph_detection(ip_address, "ipInReceives", 0, minutos, TITLES_OID[1], ['Paquetes recibidos'])
    graph_detection(ip_address, "icmpOutEchos", 0, minutos, TITLES_OID[2], ['ICMP echo enviados'])
    graph_detection(ip_address, "tcpInSegs", 0, minutos, TITLES_OID[3], ['Segmentos recibidos'])
    graph_detection(ip_address, "udpOutDatagrams", 0, minutos, TITLES_OID[4], ['Datagramas entregados'])
    graph_detection(ip_address, "ifInNUcastPkts", len(snmp_walk(community, ip_address, IF_IN_NUCAST_PKTS)), minutos, TITLES_OID[5], interfaces_name)
    graph_detection(ip_address, "ipInDelivers", 0, minutos, TITLES_OID[6], ['Paquetes recibidos exitosamente'])
    graph_detection(ip_address, "icmpOutEchoReps", 0, minutos, TITLES_OID[7], ['ICMP de respuesta enviados'])
    graph_detection(ip_address, "tcpOutSegs", 0, minutos, TITLES_OID[8], ['Segmentos enviados'])
    graph_detection(ip_address, "udpNoPorts", 0, minutos, TITLES_OID[9], ['Datagramas recibidos'])
    graph_detection(ip_address, "ifOutNUcastPkts", len(snmp_walk(community, ip_address, IF_OUT_NUCAST_PKTS)), minutos, TITLES_OID[10], interfaces_name)
    graph_detection(ip_address, "ipOutRequests", 0, minutos, TITLES_OID[11], ['Paquetes IPV4 enviados'])
    graph_detection(ip_address, "icmpEchoReq", 0, minutos, TITLES_OID[12], ['ICMP recibidos'])
    graph_detection(ip_address, "tcpRetransSegs", 0, minutos, TITLES_OID[13], ['Segmentos retransmitidos'])
    graph_detection(ip_address, "udpOutDatDevice", 0, minutos, TITLES_OID[14], ['Datagramas enviados'])
    logo = 'linux_logo.png'
    if version.split(' ')[0] == 'Darwin':
        logo = 'data/logos/macos_logo.png'
    elif version.split(' ')[0] == 'Windows':
        logo = 'data/logos/windows_logo.png'
    else:
        logo = 'data/logos/linux_logo.png'

    create_report(version.split(' ')[0], version.split(' ')[2], logo, sys_location, str(num_interfaces), up_time, community, ip_address, 'data/devices_files/' + ip_address + '/')
    os.system('open data/devices_files/' + ip_address + '/reporte_' + ip_address + '.pdf')

