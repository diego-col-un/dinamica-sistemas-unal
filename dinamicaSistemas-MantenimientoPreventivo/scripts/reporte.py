"""
Genera ../reporte_analisis.pdf a partir de resultados.json y las imágenes de ../diagramas.
Uso: python analisis.py && python diagramas.py && python reporte.py   (desde scripts/)
"""
import json
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)
from PIL import Image as PILImage

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, ".."))
DIAG = os.path.join(RAIZ, "diagramas")
R = json.load(open(os.path.join(AQUI, "resultados.json"), encoding="utf-8"))

AZUL = colors.HexColor("#2b5fa8")
GRIS = colors.HexColor("#555555")
ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=14.2,
                      alignment=TA_JUSTIFY, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19,
                    textColor=AZUL, spaceBefore=12, spaceAfter=6, keepWithNext=1)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                    textColor=colors.HexColor("#222222"), spaceBefore=8, spaceAfter=4, keepWithNext=1)
CAP = ParagraphStyle("cap", parent=BODY, fontSize=8.5, leading=11, textColor=GRIS, alignment=0, spaceAfter=10)
EQ = ParagraphStyle("eq", parent=BODY, fontName="Courier", fontSize=8.3, leading=11.2, alignment=0,
                    leftIndent=8, spaceAfter=1)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.6, leading=11, alignment=0, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("title", parent=BODY, fontName="Helvetica-Bold", fontSize=22, leading=27,
                       textColor=AZUL, alignment=0, spaceAfter=6)
SUB = ParagraphStyle("sub", parent=BODY, fontSize=12.5, leading=17, textColor=GRIS, alignment=0)


def P(t, st=BODY):
    return Paragraph(t, st)


def img(nombre, ancho=6.9 * inch):
    ruta = os.path.join(DIAG, nombre)
    w, h = PILImage.open(ruta).size
    return Image(ruta, width=ancho, height=ancho * h / w)


def tabla(datos, anchos, cabecera=True, zebra=True):
    filas = [[Paragraph(str(c), CELLB if (i == 0 and cabecera) else CELL) for c in fila]
             for i, fila in enumerate(datos)]
    t = Table(filas, colWidths=anchos, repeatRows=1 if cabecera else 0)
    est = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if cabecera:
        est.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce9f9")))
    if zebra:
        for i in range(2, len(datos), 2):
            est.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f6f8fc")))
    t.setStyle(TableStyle(est))
    return t


def k(v):
    return f"{v / 1e3:,.0f} k"


E = R["escenarios"]
sin, baja, inter, inten = (E[n] for n in E)
ahorro = sin["costo_total"] - inter["costo_total"]
extra_inten = inten["costo_total"] - inter["costo_total"]
sens = {s["parametro"]: s for s in R["sensibilidad"]}
V = R["validacion"]
opt = R["barrido_intervalo"]

story = []

# ---------------------------------------------------------------- Portada
story += [Spacer(1, 0.6 * inch),
          P("Dinámica de sistemas aplicada a la gestión de un parque de equipos tecnológicos", TITLE),
          P("Mantenimiento preventivo vs. correctivo: simulación a 60 meses de cuatro políticas", SUB),
          Spacer(1, 0.25 * inch),
          P("Proyecto 1 - Reporte de análisis de resultados y conclusiones", SUB),
          Spacer(1, 0.2 * inch),
          P("Integrantes: ______________________________________________", BODY),
          P("Curso / Profesor: ________________________________________", BODY),
          P("Fecha: noviembre de 2026", BODY),
          Spacer(1, 0.3 * inch)]

story.append(P("<b>Resumen.</b> Se construyó un modelo de dinámica de sistemas (niveles y flujos de Forrester) de un "
               "parque de 100 equipos tecnológicos para responder: <i>¿con qué frecuencia conviene hacer mantenimiento "
               "preventivo (MP) para equilibrar disponibilidad y costo?</i> El modelo se simuló 60 meses bajo cuatro "
               f"políticas. Sin MP, la disponibilidad media es {sin['disp_media']:.0f} % y el taller de reparación se "
               f"satura; con MP cada 6 meses la disponibilidad media sube a {inter['disp_media']:.0f} % y el costo total "
               f"baja de USD {k(sin['costo_total'])} a USD {k(inter['costo_total'])} "
               f"({100 * ahorro / sin['costo_total']:.0f} % menos). El MP más intensivo (cada 3 meses) gana apenas "
               f"{inten['disp_media'] - inter['disp_media']:.1f} puntos de disponibilidad pero cuesta "
               f"USD {k(extra_inten)} más. El barrido de intervalos ubica el costo mínimo entre "
               f"{opt['0.4']['intervalo_optimo']:.1f} y {opt['0.8']['intervalo_optimo']:.1f} meses según la efectividad "
               "del MP. <b>Los valores numéricos de los parámetros son supuestos del equipo</b> (no hay datos reales "
               "del parque); las conclusiones son sobre la estructura y el orden de magnitud, no predicciones.", BODY))
story.append(PageBreak())

# ---------------------------------------------------------------- 1. Planteamiento
story.append(P("1. Planteamiento del problema", H1))
story.append(P("Un parque de equipos tecnológicos (computadores, servidores, equipos de red) se degrada con el uso. "
               "Si no se hace mantenimiento preventivo, la salud de los equipos cae, las fallas aumentan, los equipos "
               "fallados se acumulan esperando reparación y la carga sobre los que siguen operando acelera su propio "
               "desgaste. El enfoque endógeno de la dinámica de sistemas es adecuado porque el comportamiento del parque "
               "(disponibilidad, costos) surge de la estructura de realimentación y de los retrasos, no de causas externas."))
story.append(P("<b>Pregunta.</b> ¿Cómo evolucionan la salud del parque, el tiempo de inactividad y los costos acumulados en "
               "60 meses, y qué frecuencia de MP equilibra disponibilidad y costo?"))
story.append(P("<b>Hipótesis dinámica.</b> (1) Sin MP aparece un círculo vicioso de degradación que satura el taller; "
               "(2) el MP crea un bucle estabilizador que sostiene la salud, pero con rendimientos decrecientes y "
               "costo creciente; (3) por eso debe existir una frecuencia intermedia de costo mínimo."))
story.append(P("<b>Alcance y supuestos.</b> Parque fijo de 100 equipos (sin compras ni bajas); un solo taller con capacidad "
               "limitada; el MP se aplica a equipos operativos y no consume capacidad del taller; la política se introduce "
               "en t = 0; costos en USD con valores hipotéticos."))

# ---------------------------------------------------------------- 2. Conceptualización
story.append(P("2. Conceptualización", H1))
story.append(P("2.1 Variables del sistema (lenguaje de Forrester)", H2))
story.append(tabla([
    ["Tipo", "Variable", "Descripción"],
    ["Nivel", "Equipos operativos", "Equipos en servicio activo (inicia en 96)."],
    ["Nivel", "Equipos en falla", "Equipos fuera de servicio, en espera o reparación (inicia en 4). Operativos + en falla = 100."],
    ["Nivel", "Salud del parque", "Índice acumulado de condición (0-1); inicia en 0.85."],
    ["Nivel", "Costo acumulado de mantenimiento", "Gasto acumulado en MP y MC."],
    ["Nivel", "Costo acumulado de inactividad", "Pérdida acumulada por equipos parados."],
    ["Flujo", "Fallas", "Operativos que pasan a falla = operativos x tasa de fallas."],
    ["Flujo", "Reparación", "Equipos que regresan a operar = MIN(en falla / tiempo de reparación, capacidad del taller)."],
    ["Flujo", "Degradación", "Pérdida de salud; crece con la fracción de equipos parados (sobrecarga)."],
    ["Flujo", "Recuperación por MP", "Salud recuperada = (1 - salud) x efectividad x MP efectivo."],
    ["Flujo", "Costo MP / Costo MC / Costo inactividad", "Gastos por mes que alimentan los niveles de costo."],
    ["Auxiliar", "Tasa de fallas", "Tasa base x (1 + sensibilidad x (1 - salud))."],
    ["Auxiliar", "MP efectivo", "Frecuencia de MP con retraso de primer orden (DELAY1)."],
    ["Parámetro", "Intervalo MP (escenario)", "0, 12, 6 o 3 meses entre intervenciones por equipo."],
], [0.8 * inch, 2.2 * inch, 3.9 * inch]))
story.append(Spacer(1, 8))
story.append(P("2.2 Estructura de realimentación", H2))
story.append(img("diagrama_causal.png", 6.9 * inch))
story.append(P("Figura 1. Diagrama de bucles causales.", CAP))
story.append(P("<b>R1 - Círculo vicioso de degradación (reforzador).</b> Menos salud aumenta la tasa de fallas; más fallas "
               "dejan más equipos parados; con más equipos parados los operativos soportan más carga y se degradan más "
               "rápido; esto reduce aún más la salud. Es la dinámica que domina cuando no hay MP."))
story.append(P("<b>B1 - Efecto del MP (estabilizador).</b> El MP recupera una fracción de la brecha de salud (1 - salud); a "
               "mayor salud, menor recuperación adicional. Por eso la salud tiende a un equilibrio y cada intervención "
               "extra rinde menos (rendimientos decrecientes)."))
story.append(P("<b>B2 - Reparación (estabilizador con tope).</b> Más equipos en falla generan más reparaciones, pero el "
               "taller tiene capacidad máxima. Si las fallas superan esa capacidad, B2 se satura y R1 toma el control."))
story.append(P("<b>Retraso.</b> El MP actúa sobre la salud a través de un retraso de primer orden (3 meses en el caso base): "
               "al introducir la política, la salud sigue cayendo un tiempo antes de que el efecto aparezca."))

# ---------------------------------------------------------------- 3. Formulación
story.append(P("3. Formulación del modelo", H1))
story.append(img("diagrama_forrester.png", 6.9 * inch))
story.append(P("Figura 2. Diagrama de Forrester (niveles, flujos, auxiliares y parámetros).", CAP))
story.append(P("3.1 Ecuaciones", H2))
eqs = [
    "d(Operativos)/dt   = Reparacion - Fallas              ; Operativos(0) = 100 - 4",
    "d(En_falla)/dt     = Fallas - Reparacion              ; En_falla(0) = 4",
    "d(Salud)/dt        = Recuperacion_MP - Degradacion    ; Salud(0) = 0.85",
    "d(Costo_mant)/dt   = Costo_MP + Costo_MC              ; Costo_mant(0) = 0",
    "d(Costo_inact)/dt  = Costo_inactividad                ; Costo_inact(0) = 0",
    "Tasa_fallas   = 0.02 * (1 + 4 * (1 - Salud))",
    "Fallas        = Operativos * Tasa_fallas",
    "Reparacion    = MIN(En_falla / 1.5, 4)",
    "Degradacion   = Salud * 0.025 * (1 + 2 * En_falla / 100)",
    "Recuperacion_MP = (1 - Salud) * 0.6 * MP_efectivo",
    "MP_efectivo   = DELAY1(Frecuencia_MP, 3 meses), valor inicial 0",
    "Frecuencia_MP = 1 / Intervalo_MP  (0 si no hay MP)",
    "Costo_MP = Frecuencia_MP * Operativos * 120 ; Costo_MC = Reparacion * 900",
    "Costo_inactividad = En_falla * 600",
]
for e in eqs:
    story.append(Paragraph(e.replace("&", "&amp;"), EQ))
story.append(Spacer(1, 6))
story.append(P("3.2 Parámetros (supuestos del equipo)", H2))
story.append(tabla([
    ["Parámetro", "Valor", "Unidad", "Interpretación"],
    ["Tasa base de fallas", "0.02", "1/mes", "2 % mensual con salud perfecta"],
    ["Sensibilidad falla-salud", "4", "adim.", "Con salud 0 la tasa es 5 veces la base"],
    ["Tasa base de degradación", "0.025", "1/mes", "Desgaste natural"],
    ["Factor de sobrecarga", "2", "adim.", "Degradación extra por equipos parados"],
    ["Efectividad del MP", "0.6", "adim.", "Fracción de la brecha de salud recuperada"],
    ["Retraso del efecto del MP", "3", "meses", "Retraso de primer orden"],
    ["Tiempo de reparación", "1.5", "meses", "Tiempo medio de reparación"],
    ["Capacidad del taller", "4", "equipos/mes", "Tope de reparaciones"],
    ["Costo unitario MP / MC", "120 / 900", "USD", "Por intervención / por reparación"],
    ["Costo de inactividad", "600", "USD/equipo-mes", "Pérdida por equipo parado"],
], [2.0 * inch, 0.8 * inch, 1.1 * inch, 3.0 * inch]))
story.append(P("Integración por el método de Euler con paso de 0.25 meses (igual que en Vensim). El modelo está escrito "
               "en <font face='Courier'>documento.mdl</font> (Vensim) y en <font face='Courier'>scripts/modelo_mantenimiento.py</font>; "
               "los resultados de este reporte provienen de la versión en Python.", BODY))

# ---------------------------------------------------------------- 4. Resultados
story.append(PageBreak())
story.append(P("4. Resultados de la simulación (60 meses)", H1))
filas = [["Escenario", "Salud final", "Disponibilidad final", "Disponibilidad media", "Inactividad media",
          "Costo mant. (USD)", "Costo inact. (USD)", "Costo total (USD)"]]
for n, r in E.items():
    filas.append([n, f"{r['salud_final']:.2f}", f"{r['disp_final']:.1f} %", f"{r['disp_media']:.1f} %",
                  f"{r['inact_media']:.1f} %", k(r["costo_mant"]), k(r["costo_inact"]), k(r["costo_total"])])
story.append(tabla(filas, [1.55 * inch, 0.6 * inch, 0.85 * inch, 0.85 * inch, 0.8 * inch, 0.75 * inch, 0.75 * inch,
                           0.75 * inch]))
story.append(P("Tabla 1. Indicadores por escenario (k = miles).", CAP))
story.append(img("resultados_trayectorias.png", 6.9 * inch))
story.append(P("Figura 3. Trayectorias de salud, disponibilidad, inactividad y costo total acumulado.", CAP))
story.append(P("<b>Lectura de los resultados.</b>"))
story.append(P(f"<b>Sin MP</b> el sistema entra en el círculo vicioso R1: la salud cae a {sin['salud_final']:.2f} y la "
               f"disponibilidad a {sin['disp_final']:.0f} % al final. El taller opera a tope la mayor parte del horizonte "
               "(unos 52 de los 60 meses) y la cola de equipos en falla llega a más de 50 equipos. Es el peor escenario "
               f"en costo total (USD {k(sin['costo_total'])}), dominado por la inactividad."))
story.append(P(f"<b>MP baja (cada 12 meses)</b> frena la caída pero no la evita del todo: la salud se estabiliza cerca de "
               f"{baja['salud_final']:.2f}, el taller sigue saturado cerca de 48 meses y la inactividad media es "
               f"{baja['inact_media']:.0f} %. Reduce el costo total a USD {k(baja['costo_total'])}."))
story.append(P(f"<b>MP intermedia (cada 6 meses)</b> es el punto de quiebre: la salud se sostiene en {inter['salud_final']:.2f}, "
               "las fallas quedan por debajo de la capacidad del taller (nunca se satura) y R1 deja de operar. Tiene el "
               f"costo total más bajo, USD {k(inter['costo_total'])}, un {100 * ahorro / sin['costo_total']:.0f} % menos que sin MP."))
story.append(P(f"<b>MP intensiva (cada 3 meses)</b> logra la mejor disponibilidad ({inten['disp_media']:.1f} %), pero el "
               f"gasto preventivo sube lo suficiente para que el costo total (USD {k(inten['costo_total'])}) supere al del "
               f"escenario intermedio en USD {k(extra_inten)}. Es el efecto de los rendimientos decrecientes de B1."))
story.append(img("resultados_costos.png", 5.6 * inch))
story.append(P("Figura 4. Composición del costo: lo que se ahorra en inactividad compensa el gasto preventivo hasta "
               "el escenario intermedio; después no.", CAP))

# ---------------------------------------------------------------- 5. Sensibilidad
story.append(P("5. Análisis de sensibilidad", H1))
story.append(img("resultados_sensibilidad.png", 6.0 * inch))
story.append(P("Figura 5. Cambio del costo total al variar cada parámetro +/-25 % (MP cada 6 meses).", CAP))
cap = sens["Capacidad del taller"]
tf = sens["Tasa base de fallas"]
story.append(P(f"<b>La capacidad del taller es el parámetro más crítico y su efecto es asimétrico.</b> Reducirla 25 % "
               f"(de 4 a 3 reparaciones/mes) sube el costo total en USD {k(cap['costo_m25'])} (+{100 * cap['costo_m25'] / R['base_intermedia']['costo_total']:.0f} %) "
               "porque el taller se satura y R1 se activa; aumentarla 25 % no cambia nada porque ya no era la restricción. "
               "Es un efecto umbral: no lineal, típico de sistemas con bucles reforzadores."))
story.append(P(f"<b>La tasa base de fallas</b> también pesa: +25 % agrega USD {k(tf['costo_p25'])} y -25 % ahorra USD "
               f"{k(-tf['costo_m25'])}; también es asimétrica porque acerca o aleja las fallas del tope del taller. "
               "Los costos unitarios producen cambios lineales y moderados (USD 28-47 k). El retraso del MP y el factor "
               "de sobrecarga casi no mueven el costo total en el escenario intermedio (menos de USD 3 k)."))
story.append(img("resultados_intervalo_optimo.png", 6.9 * inch))
story.append(P("Figura 6. Costo total y disponibilidad media según el intervalo entre MP, para tres valores de efectividad.", CAP))
story.append(P(f"El costo total mínimo aparece en un intervalo de {opt['0.4']['intervalo_optimo']:.1f} meses si la efectividad es 0.4, "
               f"{opt['0.6']['intervalo_optimo']:.1f} meses si es 0.6 y {opt['0.8']['intervalo_optimo']:.1f} meses si es 0.8. "
               "La curva es plana cerca del mínimo (con efectividad 0.6, de 5 a 8 meses el costo total queda a menos de 1 % del mínimo) "
               "y sube con fuerza hacia intervalos largos: con MP cada 3 meses el costo es 10 % mayor que el mínimo, "
               "pero con MP cada 12 meses es 32 % mayor. Equivocarse por exceso de frecuencia sale más barato que por defecto."))

# ---------------------------------------------------------------- 6. Validación
story.append(P("6. Pruebas de validación", H1))
pasos = V["paso_integracion"]
var_dt = 100 * (max(pasos.values()) - min(pasos.values())) / pasos["0.25"]
story.append(tabla([
    ["Prueba", "Resultado", "Veredicto"],
    ["Conservación de equipos (operativos + en falla = 100)", f"Error máximo {V['conservacion_max_error']:.1e}", "Cumple"],
    ["Sin fallas (tasa base = 0)", f"Equipos en falla al final = {V['sin_fallas_en_falla_final']:.0e}", "Cumple"],
    ["Sin degradación ni sobrecarga, sin MP", f"Salud final = {V['sin_degradacion_salud_final']:.2f} (igual a la inicial)", "Cumple"],
    ["Rango de la salud en todos los escenarios", f"Entre {V['salud_min_max'][0]:.2f} y {V['salud_min_max'][1]:.2f}", "Cumple"],
    ["Paso de integración (0.5 a 0.0625 meses)", f"Costo total varía {var_dt:.2f} %", "Cumple"],
    ["Taller sin límite de capacidad, sin MP", f"Inactividad media {V['taller_ilimitado_inact_media']:.1f} % vs. {V['sin_mp_inact_media']:.1f} % con el taller real", "Coherente: la saturación explica la mayor parte del deterioro"],
], [2.6 * inch, 2.7 * inch, 1.6 * inch]))
story.append(P("<b>Qué no se validó.</b> No se contrastó con datos reales de un parque; los parámetros son supuestos. "
               "Por eso se hizo el análisis de sensibilidad: las conclusiones cualitativas (existencia del umbral de "
               "saturación, rendimientos decrecientes del MP, intervalo intermedio de costo mínimo) se mantienen al "
               "variar los parámetros +/-25 %, pero las cifras exactas dependen de ellos.", BODY))

# ---------------------------------------------------------------- 7. Conclusiones
story.append(P("7. Conclusiones y recomendaciones", H1))
for t in [
    f"<b>El mantenimiento preventivo vale la pena.</b> Pasar de no hacer MP a hacerlo cada 6 meses reduce el costo total "
    f"{100 * ahorro / sin['costo_total']:.0f} % y sube la disponibilidad media de {sin['disp_media']:.0f} % a {inter['disp_media']:.0f} %.",
    "<b>El riesgo principal es el umbral del taller.</b> Mientras las fallas queden bajo su capacidad, el sistema es estable; "
    "al superarla, el círculo vicioso R1 se dispara y el deterioro es rápido. Vigilar la relación fallas / capacidad es "
    "más importante que ajustar finamente la frecuencia del MP.",
    "<b>Existe un intervalo razonable de MP</b> entre 5 y 8 meses en el rango de efectividad evaluado. Más intensivo "
    "mejora poco la disponibilidad y encarece; menos frecuente es mucho más costoso.",
    "<b>El retraso del MP importa poco en costo</b> en este modelo, pero explica por qué la salud sigue cayendo unos meses "
    "después de introducir la política: conviene no juzgar el MP antes de 3 a 6 meses.",
]:
    story.append(P(t))

story.append(P("8. Limitaciones y trabajo futuro", H1))
for t in [
    "El retraso es de primer orden y la política de MP es fija, por eso el modelo muestra una caída transitoria pero "
    "<b>no oscilaciones</b>. Para que el retraso genere oscilaciones haría falta una decisión que realimente (por ejemplo, "
    "aumentar el MP cuando la salud percibida baja, con retraso de información).",
    "No hay renovación de equipos, obsolescencia ni presupuesto limitado; el MP no consume capacidad del taller. "
    "Añadir una política de reposición y presupuesto sería la extensión natural.",
    "Calibrar con datos reales (historial de fallas, tiempos de reparación, costos) y repetir la sensibilidad "
    "con rangos observados.",
]:
    story.append(P("- " + t))

story.append(P("Anexo: cadena de búsqueda para antecedentes", H1))
story.append(P("Plataformas en inglés: <font face='Courier' size='8'>(\"system dynamics\" OR \"stock and flow\") AND (\"preventive "
               "maintenance\" OR \"maintenance policy\") AND (\"equipment fleet\" OR \"technological assets\" OR \"machinery "
               "fleet\") AND (\"failure rate\" OR downtime OR \"equipment health\" OR \"maintenance costs\") AND (\"scenario "
               "simulation\" OR \"policy testing\")</font>. Bases sugeridas: IEEE Xplore, ScienceDirect, SpringerLink, Wiley y "
               "System Dynamics Review. Criterios de inclusión: uso de diagramas causales y de Forrester, interacción MP-MC "
               "y horizontes de 24 a 60 meses o más. Las referencias bibliográficas concretas deben agregarse tras la búsqueda."))


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(0.8 * inch, 0.5 * inch, "Dinámica de sistemas - Proyecto 1 - Parque de equipos tecnológicos")
    canvas.drawRightString(letter[0] - 0.8 * inch, 0.5 * inch, f"Pág. {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(os.path.join(RAIZ, "reporte_analisis.pdf"), pagesize=letter, leftMargin=0.8 * inch,
                        rightMargin=0.8 * inch, topMargin=0.75 * inch, bottomMargin=0.8 * inch,
                        title="Reporte de análisis - Parque de equipos tecnológicos", author="")
doc.build(story, onFirstPage=pie, onLaterPages=pie)
print("PDF generado")
