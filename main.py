from devices import Devices
from datetime import datetime
import os

# BLOQUE 1
# 1.- Paquetes unicast que ha recibido una interfaz | 1156 p18 | 1.3.6.1.2.1.2.2.1.11
# 2.- Paquetes recibidos a protocolos ipv4 incluyendo los que tienen errores | 1156 p27 | 1.3.6.1.2.1.4.3.0
# 3.- Mensajes ICMP echo que ha enviado el agente | 1156 p50 | 1.3.6.1.2.1.5.21.0
# 4.- Segmentos recibidos incluyendo los que se han recibido con errores | 1156 p57 | 1.3.6.1.2.1.6.10.0
# 5.- Datagramas entregados a usuarios UDP | 1156 p63 | 1.3.6.1.2.1.7.4.0
#
# BLOQUE 2
# 1.- Paquetes multicast que ha recibido una interfaz | 1156 p18 | 1.3.6.1.2.1.2.2.1.12
# 2.- Paquetes recibidos exitosamente entregados a protocolos IPV4 | 1156 p29 | 1.3.6.1.2.1.4.9.0
# 3.- Mensajes de respuesta ICMP que ha enviado el agente | 1156 p51 | 1.3.6.1.2.1.5.22.0
# 4.- Segmentos enviados, incluyendo los de las conexiones actuales pero excluyendo los que contienen solamente octetos
#     retransmitidos | 1156 p57 | 1.3.6.1.2.1.6.11.0
# 5.- Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicacion en el puerto
#     destino | 1156 p62 | 1.3.6.1.2.1.7.2.0
#
# BLOQUE 3
# 1.- Paquetes multicast que ha enviado una interfaz | 1156 p20 | 1.3.6.1.2.1.2.2.1.18
# 2.- Paquetes IPV4 que los protocolos locales de usuarios de IPV4 suministraron a IPV4 en las solicitudes de
#     transmisión | 1156 p29 | 1.3.6.1.2.1.4.10.0
# 3.- Mensajes ICMP que ha recibido el agente | 1156 p43 | 1.3.6.1.2.1.5.1.0
# 4.- Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos
#     transmitidos previamente. | 1156 p57 | 1.3.6.1.2.1.6.12.0
# 5.- Datagramas enviados por el dispositivo. | 1156 p63 | 1.3.6.1.2.1.7.4.0


def main():
    devices = Devices()

    while True:
        os.system('clear')
        selection = 0

        while selection < 1 or selection > 5:
            print("Adquisición de información usando SNMP \n"
                  "\t1.- Listar dispositivos.\n"
                  "\t2.- Agregar dispositivo.\n"
                  "\t3.- Eliminar dispositivo.\n"
                  "\t4.- Generar reporte de contabilidad.\n"
                  "\t5.- Salir.\n")
            selection = int(input("Ingrese la opción seleccionada: "))

        if selection == 1:
            devices.list_devices()
        elif selection == 2:
            devices.add_devices()
        elif selection == 3:
            devices.list_devices()
            devices.delete_devices()
        elif selection == 4:
            devices.list_devices()
            devices.generate_report()
        elif selection == 5:
            break

        input()


def days_burn():
    burn = datetime(1998, 8, 14, 0, 0, 0)
    date = datetime(2022, 2, 23, 0, 0, 0)

    days = (date - burn).days

    return (days % 3) + 1


if __name__ == '__main__':
    main()
