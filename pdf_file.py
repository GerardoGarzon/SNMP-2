from fpdf import FPDF

TITLES_OID = [
    "Paquetes unicast que ha recibido una interfaz",
    "Paquetes recibidos a protocolos ipv4 incluyendo los que tienen errores",
    "Mensajes ICMP echo que ha enviado el agente",
    "Segmentos recibidos incluyendo los que se han recibido con errores",
    "Datagramas entregados a usuarios UDP",
    "Paquetes multicast que ha recibido una interfaz",
    "Paquetes recibidos exitosamente entregados a protocolos IPV4",
    "Mensajes de respuesta ICMP que ha enviado el agente",
    "Segmentos enviados, incluyendo los de las conexiones actuales pero excluyendo los que contienen solamente octetos retransmitidos",
    "Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicacion en el puerto destino",
    "Paquetes multicast que ha enviado una interfaz",
    "Paquetes IPV4 que los protocolos locales de usuarios de IPV4 suministraron a IPV4 en las solicitudes de transmisión",
    "Mensajes ICMP que ha recibido el agente",
    "Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente.",
    "Datagramas enviados por el dispositivo."
]

GRAPH_IMAGES = [
    "detection_ifInUcastPkts.png",
    "detection_ipInReceives.png",
    "detection_icmpOutEchos.png",
    "detection_tcpInSegs.png",
    "detection_udpOutDatagrams.png",
    "detection_ifInNUcastPkts.png",
    "detection_ipInDelivers.png",
    "detection_icmpOutEchoReps.png",
    "detection_tcpOutSegs.png",
    "detection_udpNoPorts.png",
    "detection_ifOutNUcastPkts.png",
    "detection_ipOutRequests.png",
    "detection_icmpEchoReq.png",
    "detection_tcpRetransSegs.png",
    "detection_udpOutDatDevice.png",
]


def create_report(nombre, version, logo, ubicacion, numero_interfaces, tiempo_activo, comunidad, ip, device_path):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    # Encabezados
    add_title(pdf, 'Reporte de agente')
    pdf.set_font('Arial', '', 12)
    pdf.image(logo, 10, 30, 70, 70)
    add_cell(pdf, 90, 'Nombre: ', nombre, 1)
    add_cell(pdf, 90, 'Version de SO: ', version, 1)
    add_cell(pdf, 90, 'Ubicacion: ', ubicacion, 1)
    add_cell(pdf, 90, 'Num de interfaces: ', numero_interfaces, 1)
    add_cell(pdf, 90, 'Tiempo activo: ', tiempo_activo, 1)
    add_cell(pdf, 90, 'Comunidad: ', comunidad, 1)
    add_cell(pdf, 90, 'IP: ', ip, 1)
    # Graficas, 3 por pagina
    pdf.ln()
    add_graph(pdf, 0, 10, 120, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 1, 10, 210, device_path)
    # Nueva pagina
    pdf.add_page()
    add_graph(pdf, 2, 10, 20, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 3, 10, 110, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 4, 10, 200, device_path)
    # Nueva pagina
    pdf.add_page()
    add_graph(pdf, 5, 10, 20, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 6, 10, 110, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 7, 10, 200, device_path)
    # Nueva pagina
    pdf.add_page()
    add_graph(pdf, 8, 10, 30, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 9, 10, 130, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 10, 10, 220, device_path)
    # Nueva pagina
    pdf.add_page()
    add_graph(pdf, 11, 10, 30, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 12, 10, 120, device_path)
    add_spaces_between_graphs(pdf, 6)
    add_graph(pdf, 13, 10, 220, device_path)
    # Nueva pagina
    pdf.add_page()
    add_graph(pdf, 14, 10, 20, device_path)
    add_spaces_between_graphs(pdf, 22)
    add_cell(pdf, 10, 'Creado por: ', 'Gerardo Gonzalez Garzon', 0)
    pdf.output(device_path + 'reporte_' + ip + '.pdf', 'F')


def add_cell(pdf, start_x, txt_1, txt_2, border):
    pdf.set_x(start_x)
    pdf.cell(40, 10, txt_1, border)
    pdf.cell(0, 10, txt_2, border)
    pdf.ln()


def add_title(pdf, text):
    pdf.set_font('Arial', 'B', 16)
    pdf.set_x(0)
    pdf.cell(0, 10, text, border=0, align='C')
    pdf.ln()
    pdf.ln()


def add_subtitle(pdf, text):
    pdf.set_font('Arial', 'B', 12)
    pdf.set_x(0)
    pdf.multi_cell(0, 10, text, border=0, align='C')
    pdf.ln()
    pdf.ln()


def add_graph(pdf, id, x, y, device_path):
    add_subtitle(pdf, TITLES_OID[id])
    pdf.image(device_path + GRAPH_IMAGES[id], x, y, 190, 70)


def add_spaces_between_graphs(pdf, lines):
    for i in range(lines):
        pdf.ln()


# create_report('algo', 'algo', 'data/logos/macos_logo.png', 'algo', 'algo', 'algo', 'algo', 'algo')
