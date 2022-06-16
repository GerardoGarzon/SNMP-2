from devices import Devices
from datetime import datetime
import os


# 1.- Paquetes multicast que ha enviado una interfaz
# 2.- Paquetes IPV4 que los protocolos locales de usuarios de IPV4 suministraron a IPV4 en las solicitudes de
#     transmisión
# 3.- Mensajes ICMP que ha recibido el agente
# 4.- Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos
#     transmitidos previamente.
# 5.- Datagramas enviados por el dispositivo.

def main():
    devices = Devices()

    while True:
        os.system('clear')
        selection = 0

        while selection < 1 or selection > 4:
            print("Adquisición de información usando SNMP \n"
                  "\t1.- Listar dispositivos.\n"
                  "\t2.- Agregar dispositivo.\n"
                  "\t3.- Eliminar dispositivo.\n"
                  "\t4.- Generar reporte de dispositivo.\n"
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
