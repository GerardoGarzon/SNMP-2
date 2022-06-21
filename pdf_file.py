from fpdf import FPDF

TITLES_OID = [
    "Total de segmentos recibidos \nincluyendo los que tienen errores",
    "Total de segmentos enviados \nincluyendo los que tienen errores",
]

GRAPH_IMAGES = [
    "detection_tcpInSegs.png",
    "detection_tcpOutSegs.png"
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
