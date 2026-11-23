"""
Genera el documento formal en PDF de la Formulación Matemática y Ecuaciones de Balance
para el modelo de Dinámica de Sistemas (Mantenimiento Preventivo vs. Correctivo).
Guarda la salida en: ../formulacionMatematica/Formulacion_Matematica_Dinamica_Sistemas.pdf
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# Directorios
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, ".."))
OUT_DIR = os.path.join(RAIZ, "formulacionMatematica")
DIAG_DIR = os.path.join(RAIZ, "diagramas")
PDF_PATH = os.path.join(OUT_DIR, "Formulacion_Matematica_Dinamica_Sistemas.pdf")

os.makedirs(OUT_DIR, exist_ok=True)

# Paleta de colores profesional
C_PRIMARY = colors.HexColor("#1e3d59")      # Azul marino profundo institucional
C_SECONDARY = colors.HexColor("#17b978")    # Verde bosque balance
C_ACCENT = colors.HexColor("#ff6e40")       # Naranja reforzador
C_DARK = colors.HexColor("#222831")         # Texto principal casi negro
C_MUTED = colors.HexColor("#555555")        # Texto secundario
C_LIGHT_BG = colors.HexColor("#f5f7fa")     # Fondo suave para tablas y cajas
C_BORDER = colors.HexColor("#dcdfe6")       # Bordes
C_CODE_BG = colors.HexColor("#eef2f7")      # Fondo para cajas de ecuaciones
C_BLUE_BG = colors.HexColor("#e8f0fe")      # Cabeceras de tabla

# Estilos tipográficos
styles = getSampleStyleSheet()

STYLE_TITLE = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    textColor=C_PRIMARY,
    alignment=TA_LEFT,
    spaceAfter=4
)

STYLE_SUBTITLE = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    textColor=C_MUTED,
    alignment=TA_LEFT,
    spaceAfter=12
)

STYLE_H1 = ParagraphStyle(
    "SectionH1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=C_PRIMARY,
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True
)

STYLE_H2 = ParagraphStyle(
    "SectionH2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14,
    textColor=C_DARK,
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

STYLE_BODY = ParagraphStyle(
    "BodyJustified",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=12.8,
    textColor=C_DARK,
    alignment=TA_JUSTIFY,
    spaceAfter=5
)

STYLE_BODY_BOLD = ParagraphStyle(
    "BodyBold",
    parent=STYLE_BODY,
    fontName="Helvetica-Bold"
)

STYLE_EQ = ParagraphStyle(
    "EquationBox",
    parent=styles["Normal"],
    fontName="Courier-Bold",
    fontSize=8.5,
    leading=12,
    textColor=C_PRIMARY,
    alignment=TA_LEFT,
    spaceBefore=2,
    spaceAfter=2
)

STYLE_EQ_DESC = ParagraphStyle(
    "EquationDesc",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=8,
    leading=10.5,
    textColor=C_MUTED,
    alignment=TA_LEFT,
    spaceAfter=4
)

STYLE_CAPTION = ParagraphStyle(
    "FigureCaption",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=8,
    leading=10.5,
    textColor=C_MUTED,
    alignment=TA_CENTER,
    spaceBefore=3,
    spaceAfter=8
)

STYLE_CELL = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=10.5,
    textColor=C_DARK,
    alignment=TA_LEFT
)

STYLE_CELL_BOLD = ParagraphStyle(
    "TableCellBold",
    parent=STYLE_CELL,
    fontName="Helvetica-Bold",
    textColor=C_PRIMARY
)

STYLE_CELL_CODE = ParagraphStyle(
    "TableCellCode",
    parent=STYLE_CELL,
    fontName="Courier",
    fontSize=7.8,
    leading=9.5
)


class NumberedCanvas(canvas.Canvas):
    """Genera cabecera y pie de página con número total de páginas (dos pasadas)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#666666"))
        page_w = 8.5 * 72
        page_h = 11.0 * 72
        margin = 36  # 0.5 pulgada

        # Encabezado (desde la página 2)
        if self._pageNumber > 1:
            self.drawString(margin, page_h - 26, "Universidad Nacional de Colombia — Dinámica de Sistemas")
            self.drawRightString(page_w - margin, page_h - 26, "Formulación Matemática y Ecuaciones de Balance")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.6)
            self.line(margin, page_h - 30, page_w - margin, page_h - 30)

        # Pie de página (todas las páginas)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(margin, 30, page_w - margin, 30)
        self.drawString(margin, 20, "Modelo Forrester: Mantenimiento Preventivo vs. Correctivo | Horizonte: 60 meses, dt = 0.25")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(page_w - margin, 20, page_text)
        self.restoreState()


def eq_box(math_text, description=None):
    """Crea una celda de ecuación destacada tipo bloque de fórmula matemática."""
    content = [Paragraph(f"&nbsp;&nbsp;<b>{math_text}</b>", STYLE_EQ)]
    if description:
        content.append(Paragraph(f"&nbsp;&nbsp;&bull; {description}", STYLE_EQ_DESC))
    t = Table([[content]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e0")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def construir_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []

    # =========================================================================
    # PORTADA / ENCABEZADO
    # =========================================================================
    banner_data = [
        [
            Paragraph("<b>UNIVERSIDAD NACIONAL DE COLOMBIA</b><br/>"
                      "Facultad de Minas / Ingeniería — Curso de Dinámica de Sistemas",
                      ParagraphStyle("HeadL", parent=STYLE_CELL, fontName="Helvetica", fontSize=8.5, textColor=C_PRIMARY, leading=11)),
            Paragraph("<b>DOCUMENTO TÉCNICO FORMAL</b><br/>Noviembre de 2026",
                      ParagraphStyle("HeadR", parent=STYLE_CELL, alignment=TA_RIGHT, fontSize=8, textColor=C_MUTED, leading=11))
        ]
    ]
    t_banner = Table(banner_data, colWidths=[380, 160])
    t_banner.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_banner)
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceBefore=4, spaceAfter=10))

    story.append(Paragraph("Formulación Matemática y Ecuaciones de Balance", STYLE_TITLE))
    story.append(Paragraph("Modelo de Dinámica de Sistemas para la Gestión de un Parque Tecnológico: Mantenimiento Preventivo vs. Correctivo", STYLE_SUBTITLE))

    # Caja de metadatos del proyecto
    meta_data = [
        [Paragraph("<b>Tipo de Sistema:</b> Parque cerrado (N = 100 equipos)", STYLE_CELL),
         Paragraph("<b>Horizonte Temporal:</b> T = 60 meses", STYLE_CELL),
         Paragraph("<b>Paso de Integración:</b> dt = 0.25 meses", STYLE_CELL)],
        [Paragraph("<b>Método de Solución:</b> Euler Explícito / Runge-Kutta 4", STYLE_CELL),
         Paragraph("<b>Variables de Estado (Stocks):</b> 5 niveles + 1 retardo", STYLE_CELL),
         Paragraph("<b>Entornos:</b> Vensim (.mdl), Python, Simulador Web", STYLE_CELL)]
    ]
    t_meta = Table(meta_data, colWidths=[180, 180, 180])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 1: FUNDAMENTACIÓN TEÓRICA
    # =========================================================================
    story.append(Paragraph("1. Fundamentación Teórica: Principio de Balance en Dinámica de Sistemas", STYLE_H1))
    story.append(Paragraph(
        "En el paradigma de modelado de Jay W. Forrester, un sistema físico o socio-técnico se describe como un conjunto "
        "acoplado de <b>Variables de Nivel (Stocks)</b> interconectadas mediante <b>Variables de Flujo (Rates)</b>. "
        "Las variables de nivel representan acumulaciones físicas, humanas, financieras o de información que caracterizan el "
        "estado del sistema en cualquier instante <i>t</i>, y confieren inercia y memoria dinámica.",
        STYLE_BODY
    ))
    story.append(Paragraph(
        "La <b>Ecuación de Balance</b> (o ecuación de continuidad/acumulación) gobierna la evolución de cada nivel. "
        "En el dominio del tiempo continuo, se expresa como una ecuación diferencial ordinaria de primer orden:",
        STYLE_BODY
    ))

    story.append(eq_box(
        "d Stock_i(t) / dt = &Sigma; Inflows_i(t) - &Sigma; Outflows_i(t)",
        "Forma diferencial continua: la derivada temporal del nivel es igual a la tasa neta de transferencia de masa, energía o valor."
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Equivalentemente, en su forma integral acumulativa entre el tiempo inicial <i>t<sub>0</sub></i> y el tiempo actual <i>t</i>:",
        STYLE_BODY
    ))
    story.append(eq_box(
        "Stock_i(t) = Stock_i(t_0) + &int; [ &Sigma; Inflows_i(&tau;) - &Sigma; Outflows_i(&tau;) ] d&tau;,   con Stock_i(t_0) = S_{i,0}",
        "Forma integral de Forrester: el nivel actual equivale a la condición inicial más la acumulación histórica neta."
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Para su solución computacional en simuladores como Vensim, Python y JavaScript, se discretiza el horizonte temporal "
        "en pasos uniformes <i>&Delta;t</i> mediante el método de integración de Euler (o Runge-Kutta 4):",
        STYLE_BODY
    ))
    story.append(eq_box(
        "Stock_i(t + &Delta;t) = Stock_i(t) + &Delta;t &middot; [ &Sigma; Inflows_i(t) - &Sigma; Outflows_i(t) ]",
        "Formulación en diferencias finitas (notación DYNAMO / Euler): Stock.K = Stock.J + DT * (Inflows.JK - Outflows.JK)."
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 2: ECUACIONES DE BALANCE DE LOS NIVELES
    # =========================================================================
    story.append(Paragraph("2. Ecuaciones de Balance de los Niveles del Modelo", STYLE_H1))
    story.append(Paragraph(
        "El modelo del parque de equipos tecnológicos consta de <b>5 niveles principales</b> y <b>1 nivel interno de retardo</b> "
        "que gobiernan la dinámica operativa, de confiabilidad física, financiera y de política:",
        STYLE_BODY
    ))

    # Nivel 1: Equipos Operativos
    story.append(Paragraph("2.1. Equipos Operativos [O(t)] &mdash; Unidades: equipos", STYLE_H2))
    story.append(Paragraph(
        "Representa la flota de equipos en servicio activo y productivo dentro de la organización. "
        "Se incrementa cuando los equipos averiados son restaurados por el taller (flujo <i>Reparación</i>) y disminuye cuando ocurre una avería (flujo <i>Fallas</i>).",
        STYLE_BODY
    ))
    story.append(eq_box(
        "dO(t)/dt = Reparacion(t) - Fallas(t),    O(0) = Equipos_totales - Equipos_falla_inicial = 96",
        "Forma continua: dO/dt = R(t) - F_{flujo}(t). Integración: O(t) = 96 + &int; (R - F_{flujo}) d&tau;"
    ))
    story.append(Spacer(1, 4))

    # Nivel 2: Equipos en Falla
    story.append(Paragraph("2.2. Equipos en Falla [F(t)] &mdash; Unidades: equipos", STYLE_H2))
    story.append(Paragraph(
        "Representa la cantidad de equipos fuera de servicio que están esperando o recibiendo atención en el taller de mantenimiento correctivo.",
        STYLE_BODY
    ))
    story.append(eq_box(
        "dF(t)/dt = Fallas(t) - Reparacion(t),    F(0) = Equipos_falla_inicial = 4",
        "Forma continua: dF/dt = F_{flujo}(t) - R(t). Integración: F(t) = 4 + &int; (F_{flujo} - R) d&tau;"
    ))
    story.append(Spacer(1, 4))

    # Demostración conservación
    caja_cons = [
        Paragraph("<b>Principio de Conservación de la Flota (Parque Cerrado):</b>", STYLE_CELL_BOLD),
        Paragraph("Sumando ambas ecuaciones diferenciales:<br/>"
                  "<b>dO(t)/dt + dF(t)/dt = [Reparacion(t) - Fallas(t)] + [Fallas(t) - Reparacion(t)] = 0</b><br/>"
                  "Al ser la derivada nula para todo <i>t</i>, se comprueba analíticamente que la suma de equipos es invariante:<br/>"
                  "<b>O(t) + F(t) = O(0) + F(0) = 96 + 4 = 100 equipos = N (Constante)</b>",
                  STYLE_CELL)
    ]
    t_cons = Table([[caja_cons]], colWidths=[540])
    t_cons.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eef9f5")),
        ('BOX', (0, 0), (-1, -1), 0.8, C_SECONDARY),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_cons)
    story.append(Spacer(1, 6))

    # Nivel 3: Salud del Parque
    story.append(Paragraph("2.3. Salud del Parque [S(t)] &mdash; Unidades: Adimensional [0, 1]", STYLE_H2))
    story.append(Paragraph(
        "Índice normalizado de condición físico-funcional global de los equipos. Un valor de 1 representa condición óptima de fábrica; "
        "un valor cercano a 0 representa estado crítico de degradación. Es alimentado por la acción preventiva y vaciado por el desgaste natural y operativo.",
        STYLE_BODY
    ))
    story.append(eq_box(
        "dS(t)/dt = Recuperacion_por_MP(t) - Degradacion(t),    S(0) = Salud_inicial = 0.85",
        "Forma continua: dS/dt = Rec_{MP}(t) - Deg(t). Integración: S(t) = 0.85 + &int; (Rec_{MP} - Deg) d&tau;"
    ))
    story.append(Spacer(1, 4))

    # Nivel 4: Costo Acumulado de Mantenimiento
    story.append(Paragraph("2.4. Costo Acumulado de Mantenimiento [C_m(t)] &mdash; Unidades: USD", STYLE_H2))
    story.append(Paragraph(
        "Nivel acumulador que registra el gasto financiero total erogado en intervenciones preventivas planificadas y reparaciones correctivas de averías.",
        STYLE_BODY
    ))
    story.append(eq_box(
        "dC_m(t)/dt = Costo_MP(t) + Costo_MC(t),    C_m(0) = 0 USD",
        "Forma continua: dC_m/dt = c_{mp}(t) + c_{mc}(t). Integración: C_m(t) = &int; [c_{mp}(\tau) + c_{mc}(\tau)] d&tau;"
    ))
    story.append(Spacer(1, 4))

    # Nivel 5: Costo Acumulado de Inactividad
    story.append(Paragraph("2.5. Costo Acumulado de Inactividad [C_i(t)] &mdash; Unidades: USD", STYLE_H2))
    story.append(Paragraph(
        "Nivel acumulador de pérdidas económicas derivadas de la improductividad y lucro cesante generado por los equipos detenidos en falla.",
        STYLE_BODY
    ))
    story.append(eq_box(
        "dC_i(t)/dt = Costo_inactividad(t),    C_i(0) = 0 USD",
        "Forma continua: dC_i/dt = c_{inact}(t). Integración: C_i(t) = &int; c_{inact}(\tau) d&tau;"
    ))
    story.append(Spacer(1, 4))

    # Nivel 6: Nivel Interno del Retardo de Política (DELAY1I)
    story.append(Paragraph("2.6. Esfuerzo de MP Efectivo [MP_e(t)] &mdash; Nivel del Retardo &mdash; Unidades: 1/mes", STYLE_H2))
    story.append(Paragraph(
        "En dinámica de sistemas, la función <i>DELAY1I(In, Delay, Init)</i> introduce una variable de estado oculta. "
        "Modela el tiempo que toma una directriz de mantenimiento preventivo en reflejarse efectivamente sobre la salud mecánica del parque.",
        STYLE_BODY
    ))
    story.append(eq_box(
        "d(MP_e(t))/dt = [ Frecuencia_MP(t) - MP_e(t) ] / Retraso_efecto_MP,    MP_e(0) = 0",
        "Ecuación diferencial del retardo exponencial de 1er orden: d(MP_e)/dt = (f_{mp} - MP_e) / &tau;_{mp}, con &tau;_{mp} = 3.0 meses."
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 3: ECUACIONES DE FLUJO
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Formulación de las Ecuaciones de Flujo (Rates)", STYLE_H1))
    story.append(Paragraph(
        "Las variables de flujo determinan la velocidad instantánea de cambio de los niveles en cada intervalo temporal. "
        "A continuación se detallan sus formulaciones algebraicas y su significado dentro del modelo:",
        STYLE_BODY
    ))

    flujos_tabla = [
        [Paragraph("<b>Flujo (Variable)</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Ecuación Matemática</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Unidades</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Interpretación Dinámica</b>", STYLE_CELL_BOLD)],

        [Paragraph("<b>Fallas</b> [F<sub>flujo</sub>]", STYLE_CELL_BOLD),
         Paragraph("Fallas = O(t) &middot; &lambda;(t)", STYLE_CELL_CODE),
         Paragraph("equipos / mes", STYLE_CELL),
         Paragraph("Tasa mensual de averías. Depende del número de equipos activos y de la tasa de fallas endógena influenciada por la salud.", STYLE_CELL)],

        [Paragraph("<b>Reparación</b> [R]", STYLE_CELL_BOLD),
         Paragraph("Reparacion = MIN( F(t) / T<sub>rep</sub> , C<sub>taller</sub> )", STYLE_CELL_CODE),
         Paragraph("equipos / mes", STYLE_CELL),
         Paragraph("Velocidad de restauración del taller. No lineal: si la demanda excede la capacidad máxima (4 eq/mes), el taller se satura y forma cola.", STYLE_CELL)],

        [Paragraph("<b>Degradación</b> [Deg]", STYLE_CELL_BOLD),
         Paragraph("Deg = S(t) &middot; &delta;<sub>0</sub> &middot; [ 1 + &alpha; &middot; (F(t) / N) ]", STYLE_CELL_CODE),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Pérdida de salud por envejecimiento base (&delta;<sub>0</sub>=0.025) amplificada por el factor de sobrecarga operativa (&alpha;=2.0) al haber equipos caídos.", STYLE_CELL)],

        [Paragraph("<b>Recuperación por MP</b> [Rec<sub>MP</sub>]", STYLE_CELL_BOLD),
         Paragraph("Rec<sub>MP</sub> = (1 - S(t)) &middot; &eta;<sub>mp</sub> &middot; MP<sub>e</sub>(t)", STYLE_CELL_CODE),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Restauración de salud por el preventivo. Proporcional a la brecha (1 - S): modela la ley de rendimientos marginales decrecientes.", STYLE_CELL)],

        [Paragraph("<b>Costo MP</b> [c<sub>mp</sub>]", STYLE_CELL_BOLD),
         Paragraph("c<sub>mp</sub> = f<sub>mp</sub> &middot; O(t) &middot; U<sub>mp</sub>", STYLE_CELL_CODE),
         Paragraph("USD / mes", STYLE_CELL),
         Paragraph("Tasa de gasto en preventivo: frecuencia de intervenciones por equipo activo por el costo unitario (U<sub>mp</sub> = 120 USD).", STYLE_CELL)],

        [Paragraph("<b>Costo MC</b> [c<sub>mc</sub>]", STYLE_CELL_BOLD),
         Paragraph("c<sub>mc</sub> = R(t) &middot; U<sub>mc</sub>", STYLE_CELL_CODE),
         Paragraph("USD / mes", STYLE_CELL),
         Paragraph("Tasa de gasto en correctivo: reparaciones ejecutadas por mes multiplicadas por el costo unitario de reparación (U<sub>mc</sub> = 900 USD).", STYLE_CELL)],

        [Paragraph("<b>Costo Inactividad</b> [c<sub>inact</sub>]", STYLE_CELL_BOLD),
         Paragraph("c<sub>inact</sub> = F(t) &middot; U<sub>inact</sub>", STYLE_CELL_CODE),
         Paragraph("USD / mes", STYLE_CELL),
         Paragraph("Pérdida mensual por lucro cesante y parada: equipos en falla multiplicados por el costo unitario mensual (U<sub>inact</sub> = 600 USD/eq-mes).", STYLE_CELL)]
    ]

    t_flujos = Table(flujos_tabla, colWidths=[105, 175, 75, 185])
    t_flujos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BLUE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_flujos)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 4: VARIABLES AUXILIARES Y POLÍTICA
    # =========================================================================
    story.append(Paragraph("4. Ecuaciones Auxiliares y Funciones de Política", STYLE_H1))
    story.append(Paragraph(
        "Las variables auxiliares procesan información instantánea sin acumular memoria propia. Expresan políticas, relaciones tecnológicas y KPIs:",
        STYLE_BODY
    ))

    aux_tabla = [
        [Paragraph("<b>Variable Auxiliar</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Formulación Matemática</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Unidades</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Descripción Funcional</b>", STYLE_CELL_BOLD)],

        [Paragraph("<b>Tasa de Fallas</b> [&lambda;(t)]", STYLE_CELL_BOLD),
         Paragraph("&lambda;(t) = &lambda;<sub>0</sub> &middot; [ 1 + &sigma; &middot; (1 - S(t)) ]", STYLE_CELL_CODE),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Con &lambda;<sub>0</sub>=0.02 y &sigma;=4. A salud perfecta (S=1), &lambda;=0.02 mensual. A salud degradada (S=0), &lambda; se quintuplica a 0.10 mensual.", STYLE_CELL)],

        [Paragraph("<b>Fracción en Falla</b> [&phi;<sub>F</sub>(t)]", STYLE_CELL_BOLD),
         Paragraph("&phi;<sub>F</sub>(t) = F(t) / N", STYLE_CELL_CODE),
         Paragraph("Adimensional", STYLE_CELL),
         Paragraph("Proporción del parque no operativo; alimenta directamente el término de sobrecarga sobre la flota remanente.", STYLE_CELL)],

        [Paragraph("<b>Frecuencia MP</b> [f<sub>mp</sub>]", STYLE_CELL_BOLD),
         Paragraph("f<sub>mp</sub> = 1 / I<sub>mp</sub>  (0 si I<sub>mp</sub> = 0)", STYLE_CELL_CODE),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Inverso del intervalo entre mantenimientos I<sub>mp</sub> &isin; {0, 12, 6, 3} meses según el escenario de política evaluado.", STYLE_CELL)],

        [Paragraph("<b>Disponibilidad</b> [Disp(t)]", STYLE_CELL_BOLD),
         Paragraph("Disp(t) = O(t) / N", STYLE_CELL_CODE),
         Paragraph("Adimensional (0 a 1)", STYLE_CELL),
         Paragraph("KPI operativo primario: porcentaje de la capacidad total del parque disponible para prestar servicio.", STYLE_CELL)],

        [Paragraph("<b>Inactividad %</b> [Inact(t)]", STYLE_CELL_BOLD),
         Paragraph("Inact(t) = 100 &middot; F(t) / N", STYLE_CELL_CODE),
         Paragraph("%", STYLE_CELL),
         Paragraph("Downtime porcentual del parque frente a la capacidad nominal total.", STYLE_CELL)],

        [Paragraph("<b>Costo Total Acumulado</b>", STYLE_CELL_BOLD),
         Paragraph("C<sub>total</sub>(t) = C<sub>m</sub>(t) + C<sub>i</sub>(t)", STYLE_CELL_CODE),
         Paragraph("USD", STYLE_CELL),
         Paragraph("KPI económico central: suma integral del costo directo de mantenimiento y el costo de inactividad durante los 60 meses.", STYLE_CELL)]
    ]

    t_aux = Table(aux_tabla, colWidths=[110, 170, 75, 185])
    t_aux.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BLUE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_aux)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 5: DIAGRAMAS ESTRUCTURALES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Diagramas Estructurales de Dinámica de Sistemas", STYLE_H1))
    story.append(Paragraph(
        "La correspondencia gráfica formal entre las ecuaciones de balance, flujos y auxiliares se plasma en los diagramas de Forrester y Causal:",
        STYLE_BODY
    ))

    # Diagrama de Forrester
    ruta_forrester = os.path.join(DIAG_DIR, "diagrama_forrester.png")
    if os.path.exists(ruta_forrester):
        w_img, h_img = PILImage.open(ruta_forrester).size
        ancho_deseado = 520
        alto_deseado = ancho_deseado * h_img / w_img
        story.append(Image(ruta_forrester, width=ancho_deseado, height=alto_deseado))
        story.append(Paragraph("<b>Figura 1. Diagrama de Forrester (Niveles, Flujos, Auxiliares y Retardo).</b> Nótese la conservación de equipos entre Operativos y En Falla, y la realimentación hacia la Salud.", STYLE_CAPTION))

    story.append(Spacer(1, 6))

    # Diagrama Causal
    ruta_causal = os.path.join(DIAG_DIR, "diagrama_causal.png")
    if os.path.exists(ruta_causal):
        w_img, h_img = PILImage.open(ruta_causal).size
        ancho_deseado = 480
        alto_deseado = ancho_deseado * h_img / w_img
        story.append(Image(ruta_causal, width=ancho_deseado, height=alto_deseado))
        story.append(Paragraph("<b>Figura 2. Diagrama de Bucles Causales.</b> Bucle reforzador R1 (círculo vicioso de falla), bucle balanceador B1 (control preventivo con retardo) y bucle B2 (reparación acotada).", STYLE_CAPTION))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 6: MATRIZ DE CONSISTENCIA DIMENSIONAL
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Matriz de Consistencia y Análisis Dimensional", STYLE_H1))
    story.append(Paragraph(
        "En dinámica de sistemas es mandatorio que las unidades dimensionales a ambos lados de toda ecuación de balance verifiquen la regla formal:<br/>"
        "<font face='Courier-Bold'>[ d(Stock) / dt ] = [ Inflows ] - [ Outflows ] = [ Unidades de Stock ] / [ Tiempo ]</font>",
        STYLE_BODY
    ))

    dim_tabla = [
        [Paragraph("<b>Ecuación de Balance</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Dimensión de Nivel [S]</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Dimensión Temporal [t]</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Unidad Flujos [dS/dt]</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Comprobación Dimensional de Términos</b>", STYLE_CELL_BOLD)],

        [Paragraph("<b>dO/dt = R - F<sub>flujo</sub></b>", STYLE_CELL_CODE),
         Paragraph("equipos", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("equipos / mes", STYLE_CELL),
         Paragraph("R [eq/mes] - F<sub>flujo</sub> [eq &middot; (1/mes) = eq/mes] &rArr; Consistente", STYLE_CELL)],

        [Paragraph("<b>dF/dt = F<sub>flujo</sub> - R</b>", STYLE_CELL_CODE),
         Paragraph("equipos", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("equipos / mes", STYLE_CELL),
         Paragraph("F<sub>flujo</sub> [eq/mes] - R [eq/mes] &rArr; Consistente", STYLE_CELL)],

        [Paragraph("<b>dS/dt = Rec<sub>MP</sub> - Deg</b>", STYLE_CELL_CODE),
         Paragraph("Dmnl (índice 0-1)", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Rec<sub>MP</sub> [Dmnl &middot; (1/mes) = 1/mes] - Deg [Dmnl &middot; (1/mes) = 1/mes] &rArr; Consistente", STYLE_CELL)],

        [Paragraph("<b>dC<sub>m</sub>/dt = c<sub>mp</sub> + c<sub>mc</sub></b>", STYLE_CELL_CODE),
         Paragraph("USD", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("USD / mes", STYLE_CELL),
         Paragraph("c<sub>mp</sub> [(1/mes) &middot; eq &middot; (USD/eq) = USD/mes] + c<sub>mc</sub> [(eq/mes) &middot; (USD/eq) = USD/mes] &rArr; Consistente", STYLE_CELL)],

        [Paragraph("<b>dC<sub>i</sub>/dt = c<sub>inact</sub></b>", STYLE_CELL_CODE),
         Paragraph("USD", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("USD / mes", STYLE_CELL),
         Paragraph("c<sub>inact</sub> [eq &middot; (USD/(eq &middot; mes)) = USD/mes] &rArr; Consistente", STYLE_CELL)],

        [Paragraph("<b>d(MP<sub>e</sub>)/dt = (f<sub>mp</sub> - MP<sub>e</sub>)/&tau;</b>", STYLE_CELL_CODE),
         Paragraph("1 / mes", STYLE_CELL),
         Paragraph("mes", STYLE_CELL),
         Paragraph("1 / mes<sup>2</sup>", STYLE_CELL),
         Paragraph("(f<sub>mp</sub> [1/mes] - MP<sub>e</sub> [1/mes]) / &tau; [mes] = 1/mes<sup>2</sup> &rArr; Consistente", STYLE_CELL)]
    ]

    t_dim = Table(dim_tabla, colWidths=[120, 95, 75, 95, 155])
    t_dim.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BLUE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_dim)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 7: PARÁMETROS DEL SISTEMA
    # =========================================================================
    story.append(Paragraph("7. Tabla Maestra de Parámetros y Condiciones Iniciales", STYLE_H1))
    story.append(Paragraph(
        "A continuación se consolidan todos los parámetros supuestos para la simulación base a 60 meses:",
        STYLE_BODY
    ))

    param_tabla = [
        [Paragraph("<b>Parámetro</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Símbolo</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Valor Base</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Unidad</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Justificación y Significado Físico / Económico</b>", STYLE_CELL_BOLD)],

        [Paragraph("Equipos totales", STYLE_CELL), Paragraph("N", STYLE_CELL_CODE), Paragraph("100.0", STYLE_CELL), Paragraph("equipos", STYLE_CELL),
         Paragraph("Inventario base de hardware; sistema cerrado sin reemplazos.", STYLE_CELL)],
        [Paragraph("Equipos en falla inicial", STYLE_CELL), Paragraph("F(0)", STYLE_CELL_CODE), Paragraph("4.0", STYLE_CELL), Paragraph("equipos", STYLE_CELL),
         Paragraph("Condición inicial de equipos averiados esperando taller en t = 0.", STYLE_CELL)],
        [Paragraph("Salud inicial del parque", STYLE_CELL), Paragraph("S(0)", STYLE_CELL_CODE), Paragraph("0.85", STYLE_CELL), Paragraph("Dmnl", STYLE_CELL),
         Paragraph("Condición física inicial promedio del parque tecnológico.", STYLE_CELL)],
        [Paragraph("Tasa base de fallas", STYLE_CELL), Paragraph("&lambda;<sub>0</sub>", STYLE_CELL_CODE), Paragraph("0.02", STYLE_CELL), Paragraph("1 / mes", STYLE_CELL),
         Paragraph("2% de falla mensual para un equipo en condición óptima.", STYLE_CELL)],
        [Paragraph("Sensibilidad falla-salud", STYLE_CELL), Paragraph("&sigma;", STYLE_CELL_CODE), Paragraph("4.0", STYLE_CELL), Paragraph("Dmnl", STYLE_CELL),
         Paragraph("Multiplicador de degradación: quintuplica la tasa de falla con S = 0.", STYLE_CELL)],
        [Paragraph("Tasa base de degradación", STYLE_CELL), Paragraph("&delta;<sub>0</sub>", STYLE_CELL_CODE), Paragraph("0.025", STYLE_CELL), Paragraph("1 / mes", STYLE_CELL),
         Paragraph("Desgaste físico natural mensual sin sobrecarga.", STYLE_CELL)],
        [Paragraph("Factor de sobrecarga", STYLE_CELL), Paragraph("&alpha;", STYLE_CELL_CODE), Paragraph("2.0", STYLE_CELL), Paragraph("Dmnl", STYLE_CELL),
         Paragraph("Agravamiento del desgaste cuando hay equipos parados.", STYLE_CELL)],
        [Paragraph("Efectividad del MP", STYLE_CELL), Paragraph("&eta;<sub>mp</sub>", STYLE_CELL_CODE), Paragraph("0.6", STYLE_CELL), Paragraph("Dmnl", STYLE_CELL),
         Paragraph("Fracción de la brecha de salud (1 - S) recuperable por ciclo.", STYLE_CELL)],
        [Paragraph("Retraso del efecto MP", STYLE_CELL), Paragraph("&tau;<sub>mp</sub>", STYLE_CELL_CODE), Paragraph("3.0", STYLE_CELL), Paragraph("meses", STYLE_CELL),
         Paragraph("Constante de tiempo de retraso de primer orden en el impacto del MP.", STYLE_CELL)],
        [Paragraph("Tiempo medio de reparación", STYLE_CELL), Paragraph("T<sub>rep</sub>", STYLE_CELL_CODE), Paragraph("1.5", STYLE_CELL), Paragraph("meses", STYLE_CELL),
         Paragraph("Duración estándar requerida para devolver un equipo al estado operativo.", STYLE_CELL)],
        [Paragraph("Capacidad del taller", STYLE_CELL), Paragraph("C<sub>taller</sub>", STYLE_CELL_CODE), Paragraph("4.0", STYLE_CELL), Paragraph("equipos / mes", STYLE_CELL),
         Paragraph("Restricción física de cuello de botella: máximo de reparaciones/mes.", STYLE_CELL)],
        [Paragraph("Costo unitario MP", STYLE_CELL), Paragraph("U<sub>mp</sub>", STYLE_CELL_CODE), Paragraph("120.0", STYLE_CELL), Paragraph("USD / interv.", STYLE_CELL),
         Paragraph("Costo por revisión y servicio preventivo programado.", STYLE_CELL)],
        [Paragraph("Costo unitario MC", STYLE_CELL), Paragraph("U<sub>mc</sub>", STYLE_CELL_CODE), Paragraph("900.0", STYLE_CELL), Paragraph("USD / repar.", STYLE_CELL),
         Paragraph("Costo promedio de repuestos y mano de obra por avería.", STYLE_CELL)],
        [Paragraph("Costo inactividad por equipo", STYLE_CELL), Paragraph("U<sub>inact</sub>", STYLE_CELL_CODE), Paragraph("600.0", STYLE_CELL), Paragraph("USD / (eq &middot; mes)", STYLE_CELL),
         Paragraph("Pérdida por parada o costo de alquiler de equipo contingente.", STYLE_CELL)],
        [Paragraph("Paso de integración", STYLE_CELL), Paragraph("&Delta;t", STYLE_CELL_CODE), Paragraph("0.25", STYLE_CELL), Paragraph("meses", STYLE_CELL),
         Paragraph("Discretización numérica (1 semana); asegura estabilidad &Delta;t &le; &tau;/4.", STYLE_CELL)],
        [Paragraph("Horizonte de simulación", STYLE_CELL), Paragraph("T<sub>final</sub>", STYLE_CELL_CODE), Paragraph("60.0", STYLE_CELL), Paragraph("meses", STYLE_CELL),
         Paragraph("Ventana de planificación estratégica a 5 años.", STYLE_CELL)]
    ]

    t_param = Table(param_tabla, colWidths=[110, 45, 45, 75, 265])
    t_param.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BLUE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_param)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 8: ESQUEMA VECTORIAL Y ALGORITMO NUMÉRICO
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("8. Formulación Matricial del Sistema y Algoritmo Numérico", STYLE_H1))
    story.append(Paragraph(
        "El modelo completo se formula computacionalmente como un sistema no lineal autónomo de ecuaciones diferenciales ordinarias:<br/>"
        "<font face='Courier-Bold'>d <b>y</b>(t) / dt = <b>f</b>(<b>y</b>(t), <b>p</b>)</font>, donde el vector de estado <b>y</b>(t) &isin; &real;<sup>6</sup> está definido por:",
        STYLE_BODY
    ))

    story.append(eq_box(
        "<b>y</b>(t) = [ O(t),  F(t),  S(t),  C_m(t),  C_i(t),  MP_e(t) ]<sup>T</sup>",
        "Vector de variables de nivel del sistema dinámico en cualquier instante t."
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "El vector de derivadas <b>f</b>(<b>y</b>, <b>p</b>) = d<b>y</b>/dt se evalúa en cada instante según:",
        STYLE_BODY
    ))

    derivadas_box = (
        "f_1 = dO/dt    =  Reparacion - Fallas<br/>"
        "f_2 = dF/dt    =  Fallas - Reparacion<br/>"
        "f_3 = dS/dt    =  Recuperacion_MP - Degradacion<br/>"
        "f_4 = dC_m/dt  =  Costo_MP + Costo_MC<br/>"
        "f_5 = dC_i/dt  =  Costo_inactividad<br/>"
        "f_6 = dMP_e/dt =  (f_mp - MP_e) / &tau;_mp"
    )
    story.append(eq_box(derivadas_box, "Sistema acoplado de derivadas temporales evaluado paso a paso."))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Algoritmo de Integración de Euler Explícito:</b><br/>"
        "Avanza el estado del sistema en pasos discretos de tiempo <i>k = 0, 1, ..., N<sub>steps</sub></i> con <i>t<sub>k</sub> = k &middot; &Delta;t</i>:<br/>"
        "&nbsp;&nbsp;&bull; <b>y</b><sub>k+1</sub> = <b>y</b><sub>k</sub> + &Delta;t &middot; <b>f</b>(<b>y</b><sub>k</sub>, <b>p</b>)<br/>"
        "Este esquema garantiza equivalencia exacta entre la simulación de Vensim (.mdl), el script de Python (NumPy) y el simulador interactivo en JavaScript.",
        STYLE_BODY
    ))
    story.append(Spacer(1, 6))

    concl_data = [
        Paragraph("<b>Conclusión Teórica del Balance Dinámico:</b>", STYLE_CELL_BOLD),
        Paragraph(
            "La formulación matemática demuestra por qué la política 'Sin MP' es estructuralmente inestable y conduce a un colapso "
            "operativo: al degradarse la salud <i>S</i>, la tasa de fallas <i>&lambda;(S)</i> excede la capacidad límite del taller "
            "(<i>C<sub>taller</sub> = 4</i>), activando el bucle reforzador R1 de bola de nieve. Por el contrario, un mantenimiento preventivo "
            "intermedio (cada 6 meses) sostiene la tasa de fallas por debajo del umbral crítico de congestión, minimizando el costo "
            "total acumulado mediante el equilibrio de los balances de estado.",
            STYLE_BODY
        )
    ]
    t_concl = Table([[concl_data]], colWidths=[540])
    t_concl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f4f8")),
        ('BOX', (0, 0), (-1, -1), 0.8, C_PRIMARY),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_concl)

    # Construir el documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {PDF_PATH}")


if __name__ == "__main__":
    construir_pdf()
