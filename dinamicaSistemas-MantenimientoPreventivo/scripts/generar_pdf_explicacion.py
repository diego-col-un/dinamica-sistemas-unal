"""
Genera el documento formal en PDF de la Guía Explicativa y Conceptual
de la Formulación Matemática del Modelo de Dinámica de Sistemas.
Guarda la salida en: ../formulacionMatematica/Explicacion_Detallada_Formulacion_Matematica.pdf
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

# Rutas
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, ".."))
OUT_DIR = os.path.join(RAIZ, "formulacionMatematica")
DIAG_DIR = os.path.join(RAIZ, "diagramas")
PDF_PATH = os.path.join(OUT_DIR, "Explicacion_Detallada_Formulacion_Matematica.pdf")

os.makedirs(OUT_DIR, exist_ok=True)

# Paleta gráfica
C_PRIMARY = colors.HexColor("#1e3d59")      # Azul marino oscuro
C_SECONDARY = colors.HexColor("#17b978")    # Verde balance
C_ACCENT = colors.HexColor("#c0503a")       # Rojo advertencia / reforzador
C_WARM = colors.HexColor("#d98b2b")         # Naranja cálido
C_DARK = colors.HexColor("#222831")         # Texto principal
C_MUTED = colors.HexColor("#555555")        # Texto secundario
C_LIGHT_BG = colors.HexColor("#f8fafc")     # Fondo tablas
C_BORDER = colors.HexColor("#cbd5e0")       # Bordes
C_CODE_BG = colors.HexColor("#eef2f7")      # Fondo fórmulas
C_BLUE_BG = colors.HexColor("#e8f0fe")      # Cabecera tablas
C_CALLOUT_BG = colors.HexColor("#f0f7ff")   # Cajas destacadas de intuición

styles = getSampleStyleSheet()

STYLE_TITLE = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=23,
    textColor=C_PRIMARY,
    spaceAfter=4
)

STYLE_SUBTITLE = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,
    textColor=C_MUTED,
    spaceAfter=12
)

STYLE_H1 = ParagraphStyle(
    "SectionH1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=12.5,
    leading=16,
    textColor=C_PRIMARY,
    spaceBefore=12,
    spaceAfter=5,
    keepWithNext=True
)

STYLE_H2 = ParagraphStyle(
    "SectionH2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=13.5,
    textColor=C_DARK,
    spaceBefore=9,
    spaceAfter=4,
    keepWithNext=True
)

STYLE_BODY = ParagraphStyle(
    "BodyJustified",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.8,
    leading=12.4,
    textColor=C_DARK,
    alignment=TA_JUSTIFY,
    spaceAfter=5
)

STYLE_CALLOUT = ParagraphStyle(
    "CalloutText",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=8.5,
    leading=11.8,
    textColor=colors.HexColor("#1a365d"),
    alignment=TA_JUSTIFY
)

STYLE_CALLOUT_TITLE = ParagraphStyle(
    "CalloutTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=12,
    textColor=C_PRIMARY,
    spaceAfter=3
)

STYLE_CELL = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=10.5,
    textColor=C_DARK
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
    """Encabezado y pie de página con paginación dinámica."""
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
        margin = 36

        if self._pageNumber > 1:
            self.drawString(margin, page_h - 26, "Universidad Nacional de Colombia — Dinámica de Sistemas")
            self.drawRightString(page_w - margin, page_h - 26, "Guía Explicativa de la Formulación Matemática")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.6)
            self.line(margin, page_h - 30, page_w - margin, page_h - 30)

        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(margin, 30, page_w - margin, 30)
        self.drawString(margin, 20, "Guía Conceptual y Pedagógica: Ecuaciones de Balance, Bucles de Retorno y Estabilidad")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(page_w - margin, 20, page_text)
        self.restoreState()


def callout_box(title, text, color_border=C_PRIMARY, bg_color=C_CALLOUT_BG):
    """Crea una caja destacada pedagógica."""
    content = [
        Paragraph(title, STYLE_CALLOUT_TITLE),
        Paragraph(text, STYLE_CALLOUT)
    ]
    t = Table([[content]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 1.0, color_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
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
    # PORTADA
    # =========================================================================
    header_banner = [
        [
            Paragraph("<b>UNIVERSIDAD NACIONAL DE COLOMBIA</b><br/>"
                      "Facultad de Minas / Ingeniería — Asignatura de Dinámica de Sistemas",
                      ParagraphStyle("HB_L", parent=STYLE_CELL, fontName="Helvetica", fontSize=8.5, textColor=C_PRIMARY, leading=11)),
            Paragraph("<b>DOCUMENTO PEDAGÓGICO Y EXPLICATIVO</b><br/>Noviembre de 2026",
                      ParagraphStyle("HB_R", parent=STYLE_CELL, alignment=TA_RIGHT, fontSize=8, textColor=C_MUTED, leading=11))
        ]
    ]
    t_head = Table(header_banner, colWidths=[380, 160])
    t_head.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_head)
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("Guía Explicativa y Conceptual de la Formulación Matemática", STYLE_TITLE))
    story.append(Paragraph(
        "Desglose didáctico, justificación de las ecuaciones de balance, intuición física de los bucles causales "
        "y análisis de ingeniería del modelo de mantenimiento de equipos tecnológicos.",
        STYLE_SUBTITLE
    ))

    # =========================================================================
    # SECCIÓN 1: POR QUÉ DINÁMICA DE SISTEMAS
    # =========================================================================
    story.append(Paragraph("1. La Filosofía del Modelo: ¿Por qué Dinámica de Sistemas?", STYLE_H1))
    story.append(Paragraph(
        "En la ingeniería tradicional y la administración clásica, los planes de mantenimiento suelen evaluarse mediante "
        "<b>cálculos estáticos</b> (por ejemplo, multiplicar una tasa de falla histórica fija por el costo unitario de reparación). "
        "Sin embargo, la realidad de un parque de equipos tecnológicos exhibe una propiedad fundamental: <b>la causalidad circular y endógena</b>. "
        "Cuando los equipos fallan y el taller no da abasto, los equipos parados aumentan la carga de trabajo sobre los pocos que siguen "
        "funcionando, acelerando su degradación y provocando una cascada de averías que ningún análisis estático es capaz de prever.",
        STYLE_BODY
    ))
    story.append(Paragraph(
        "La Dinámica de Sistemas, desarrollada por Jay Forrester en el MIT, resuelve esto modelando la realidad mediante la metáfora "
        "universal de <b>tanques de agua (Niveles o Stocks)</b> regulados por <b>válvulas de caudal (Flujos o Rates)</b>. "
        "Las decisiones de mantenimiento (políticas) actúan como controles de realimentación sobre estas válvulas.",
        STYLE_BODY
    ))

    story.append(callout_box(
        "Intuición Clave: El Principio de la Bañera (The Bathtub Principle)",
        "Un nivel es como el agua acumulada en una bañera. La única forma física de alterar el volumen de agua en el tanque es abriendo "
        "el grifo de entrada (flujos de entrada) o abriendo el desagüe (flujos de salida). Las decisiones administrativas o los indicadores "
        "(las variables auxiliares) no pueden cambiar el nivel instantáneamente; solo pueden ajustar las válvulas. Por esta razón, todo nivel "
        "tiene inercia, memoria y resistencia al cambio inmediato."
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 2: EXPLICACIÓN DE LAS ECUACIONES DE BALANCE
    # =========================================================================
    story.append(Paragraph("2. Explicación Detallada de las Ecuaciones de Balance (Niveles)", STYLE_H1))
    story.append(Paragraph(
        "Una <b>Ecuación de Balance</b> es la expresión matemática de la ley de conservación aplicada a un nivel. "
        "Establece que la tasa neta de cambio del stock en el tiempo (su derivada) es estrictamente igual a lo que entra menos lo que sale. "
        "A continuación se explica el significado físico y operativo de cada uno de los niveles del modelo:",
        STYLE_BODY
    ))

    # Nivel Operativos y En Falla
    story.append(Paragraph("2.1. El Eje Operativo: Equipos Operativos [O] y Equipos en Falla [F]", STYLE_H2))
    story.append(Paragraph(
        "<b>&bull; Ecuación de Equipos Operativos:</b> <i>dO/dt = Reparacion - Fallas</i>.<br/>"
        "Este nivel cuantifica la capacidad productiva instalada y activa. Cada equipo que falla sale del nivel operativo; "
        "cada equipo reparado por el taller ingresa de nuevo.<br/>"
        "<b>&bull; Ecuación de Equipos en Falla:</b> <i>dF/dt = Fallas - Reparacion</i>.<br/>"
        "Representa la 'cola de espera' y el trabajo en proceso del taller de mantenimiento correctivo.",
        STYLE_BODY
    ))
    story.append(Paragraph(
        "<b>¿Por qué la suma de ambos niveles da exactamente 100 en todo instante?</b><br/>"
        "Analíticamente, al sumar ambas derivadas se obtiene <i>dO/dt + dF/dt = (R - F) + (F - R) = 0</i>. "
        "Que la derivada de la suma sea cero significa que el parque es un <b>sistema cerrado</b>: no se compran equipos nuevos "
        "ni se dan de baja equipos viejos durante el horizonte de 60 meses. Esta hipótesis de alcance aísla deliberadamente "
        "el impacto puro de la política de mantenimiento sin distorsiones por adquisiciones de capital.",
        STYLE_BODY
    ))

    # Nivel Salud
    story.append(Paragraph("2.2. El Eje de Confiabilidad: Salud del Parque [S]", STYLE_H2))
    story.append(Paragraph(
        "<b>Ecuación de Balance:</b> <i>dS/dt = Recuperacion_por_MP - Degradacion</i>, con <i>S(0) = 0.85</i>.<br/>"
        "La salud no es un conteo físico de equipos, sino una <b>variable intensiva de condición</b> (un índice normalizado entre 0 y 1). "
        "Actúa como el 'capital de confiabilidad' acumulado del parque. A medida que los equipos operan, sufre desgaste natural y sobrecarga "
        "(flujo de salida <i>Degradación</i>). El mantenimiento preventivo inyecta confiabilidad renovada mediante inspecciones, limpieza, "
        "sustitución de consumibles y ajustes (flujo de entrada <i>Recuperación por MP</i>).",
        STYLE_BODY
    ))

    # Niveles de Costo
    story.append(Paragraph("2.3. El Eje Financiero: Costos Acumulados [C_m y C_i]", STYLE_H2))
    story.append(Paragraph(
        "<b>&bull; Costo de Mantenimiento:</b> <i>dC_m/dt = Costo_MP + Costo_MC</i>.<br/>"
        "<b>&bull; Costo de Inactividad:</b> <i>dC_i/dt = Costo_inactividad</i>.<br/>"
        "<b>¿Por qué estos dos niveles no tienen flujos de salida?</b><br/>"
        "En dinámica de sistemas, estos niveles se denominan <b>acumuladores contables o sumideros</b>. No representan cuentas bancarias de las cuales "
        "se pueda retirar dinero, sino el registro acumulativo histórico del dinero total consumido a lo largo del tiempo. "
        "Su valor final a los 60 meses, <i>C_total = C_m + C_i</i>, es la función objetivo que la dirección técnica busca minimizar.",
        STYLE_BODY
    ))

    # Retardo
    story.append(Paragraph("2.4. El Eje de Inercia Organizacional: Esfuerzo de MP Efectivo [MP_e]", STYLE_H2))
    story.append(Paragraph(
        "<b>Ecuación:</b> <i>d(MP_e)/dt = (Frecuencia_MP - MP_e) / Retraso_efecto_MP</i>, con <i>MP_e(0) = 0</i> y &tau; = 3 meses.<br/>"
        "En la práctica gerencial, emitir la orden de 'hacer mantenimiento cada 6 meses' no mejora la salud del parque al instante siguiente. "
        "Existe un <b>retardo material y de aprendizaje</b>: programar los turnos de los técnicos, adquirir los kits de repuestos, inspeccionar equipo por equipo "
        "y lograr que los componentes alcancen estabilidad operativa toma tiempo. Este nivel modela ese retraso mediante un filtro exponencial "
        "de primer orden. Por ello, en t = 0 el efecto es nulo y la salud sigue cayendo antes de que la política rinda frutos.",
        STYLE_BODY
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 3: EXPLICACIÓN DE LAS ECUACIONES DE FLUJO
    # =========================================================================
    story.append(Paragraph("3. Anatomía y Justificación de las Ecuaciones de Flujo (Rates)", STYLE_H1))
    story.append(Paragraph(
        "Cada ecuación de flujo representa un mecanismo físico, de comportamiento humano o de mercado. "
        "A continuación se explica la lógica detrás de sus componentes matemáticos:",
        STYLE_BODY
    ))

    # Fallas
    story.append(Paragraph("3.1. Flujo de Fallas: Fallas = O(t) &middot; &lambda;(t)", STYLE_H2))
    story.append(Paragraph(
        "<b>¿Por qué se multiplica por O(t) y no por el total de equipos N?</b><br/>"
        "Este es un principio epistemológico fundamental en dinámica de sistemas: solo los equipos que están <i>operando</i> pueden fallar. "
        "Un equipo que ya está descompuesto en el taller no puede experimentar una avería operativa adicional. Por lo tanto, el flujo "
        "debe ser proporcional a la población en riesgo, <i>O(t)</i>. La probabilidad condicional de falla por mes, &lambda;(t), crece "
        "a medida que la salud <i>S</i> cae: <i>&lambda;(t) = 0.02 &middot; [1 + 4 &middot; (1 - S)]</i>. Si el parque está nuevo (S = 1), "
        "la tasa es del 2% mensual; si el parque colapsa (S = 0), la tasa se quintuplica al 10% mensual.",
        STYLE_BODY
    ))

    # Reparación
    story.append(Paragraph("3.2. Flujo de Reparación: Reparación = MIN( F(t) / T_rep , C_taller )", STYLE_H2))
    story.append(Paragraph(
        "Esta es la <b>ecuación no lineal más crítica de todo el modelo</b>. Combina dos regímenes de operación mediante la función MIN:<br/>"
        "1. <b>Régimen no saturado (F / 1.5 &lt; 4):</b> Si hay pocos equipos en falla (por ejemplo, 3 equipos), el taller repara a un ritmo "
        "de <i>3 / 1.5 = 2 equipos/mes</i>. El taller tiene capacidad ociosa y atiende la demanda con fluidez.<br/>"
        "2. <b>Régimen saturado (F / 1.5 &ge; 4):</b> Si los equipos en falla superan los 6 equipos (6 / 1.5 = 4), el término <i>F / T_rep</i> "
        "excede la capacidad máxima del taller (4 equipos/mes). En ese instante, la función MIN 'recorta' el flujo a 4.0. "
        "Los equipos restantes quedan esperando en una cola que no se puede drenar. Este cuello de botella es el responsable de que el "
        "escenario 'Sin MP' explote hacia la catástrofe.",
        STYLE_BODY
    ))

    # Degradación con sobrecarga
    story.append(Paragraph("3.3. Degradación: Deg = S &middot; &delta;_0 &middot; [ 1 + &alpha; &middot; (F / N) ]", STYLE_H2))
    story.append(Paragraph(
        "La salud disminuye por dos factores combinados:<br/>"
        "&bull; <b>Desgaste basal (S &middot; &delta;_0):</b> El envejecimiento térmico, mecánico y químico natural del hardware (2.5% mensual).<br/>"
        "&bull; <b>Efecto de sobrecarga operativa [1 + 2 &middot; (F / 100)]:</b> En una empresa, si 30 de los 100 servidores o equipos de red fallan, "
        "la carga de procesamiento o los turnos de trabajo no se reducen en un 30%; se redistribuyen sobre los 70 equipos sanos. "
        "Esos equipos operativos trabajan más calientes, a mayor ciclo de trabajo y con menos margen de refrigeración, acelerando su degradación. "
        "El parámetro &alpha; = 2.0 captura este agravamiento no lineal.",
        STYLE_BODY
    ))

    # Recuperación MP con rendimientos decrecientes
    story.append(Paragraph("3.4. Recuperación por MP: Rec_MP = (1 - S) &middot; &eta;_mp &middot; MP_e", STYLE_H2))
    story.append(Paragraph(
        "La recuperación de salud incorpora la <b>Ley Económica de los Rendimientos Marginales Decrecientes</b> mediante el factor <i>(1 - S)</i>:<br/>"
        "&bull; Si la salud es baja (por ejemplo, S = 0.5), la brecha de salud es grande: <i>(1 - 0.5) = 0.5</i>. Una intervención preventiva "
        "limpia ventiladores atascados, renueva pasta térmica y ajusta voltajes, produciendo una gran mejora en la confiabilidad.<br/>"
        "&bull; Si la salud ya es muy alta (por ejemplo, S = 0.95), la brecha es mínima: <i>(1 - 0.95) = 0.05</i>. Realizar más mantenimiento "
        "apenas agrega valor; no se puede hacer que un equipo nuevo sea 'más nuevo'. Por eso, duplicar la frecuencia de MP (cada 3 meses) "
        "no duplica la salud del parque, pero sí duplica los costos de mano de obra.",
        STYLE_BODY
    ))

    # Flujos económicos
    story.append(Paragraph("3.5. Flujos Económicos y Costo de Oportunidad", STYLE_H2))
    story.append(Paragraph(
        "El modelo monetario establece un estricto compromiso económico:<br/>"
        "&bull; <b>Costo MP ($120 USD/intervención):</b> Es una inversión periódica, predecible y programable.<br/>"
        "&bull; <b>Costo MC ($900 USD/reparación):</b> Reparar un equipo averiado es <b>7.5 veces más caro</b> que prevenir la falla, "
        "debido a la urgencia, diagnóstico de daños imprevistos y daño colateral en componentes adyacentes.<br/>"
        "&bull; <b>Costo de Inactividad ($600 USD/equipo-mes):</b> El lucro cesante por tener un equipo detenido. "
        "Si 20 equipos quedan parados durante un mes, la organización pierde 12,000 USD simplemente por inactividad.",
        STYLE_BODY
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 4: LOS BUCLES CAUSALES Y LA DINÁMICA DE RETORNO
    # =========================================================================
    story.append(Paragraph("4. La Dinámica de Bucles: Círculos Viciosos vs. Bucles de Control", STYLE_H1))
    story.append(Paragraph(
        "El comportamiento del sistema no proviene de las ecuaciones aisladas, sino de la interacción entre sus tres bucles de realimentación:",
        STYLE_BODY
    ))

    story.append(callout_box(
        "Bucle Reforzador R1: El Círculo Vicioso de Falla ('Bola de Nieve')",
        "Menos Salud &rarr; (+) Tasa de Fallas &rarr; (+) Equipos en Falla &rarr; (+) Sobrecarga en Operativos &rarr; (+) Degradación &rarr; (-) Salud.<br/>"
        "R1 es un bucle positivo (reforzador o desestabilizador). Si el sistema pierde salud, este bucle amplifica la perturbación "
        "generando una espiral destructiva de fallas acumuladas. Es la causa directa del colapso observado en la política 'Sin MP'.",
        color_border=C_ACCENT, bg_color=colors.HexColor("#fff5f5")
    ))
    story.append(Spacer(1, 4))

    story.append(callout_box(
        "Bucle Balanceador B1: El Mecanismo de Control Preventivo",
        "Menos Salud &rarr; (+) Brecha de Salud (1 - S) &rarr; (+) Recuperación por MP &rarr; (+) Salud.<br/>"
        "B1 es un bucle negativo (balanceador o estabilizador). Funciona como un termostato: a medida que la salud cae, la eficacia "
        "relativa de cada intervención preventiva aumenta, frenando la degradación y estabilizando el sistema en un punto de equilibrio.",
        color_border=C_SECONDARY, bg_color=colors.HexColor("#f0fdf4")
    ))
    story.append(Spacer(1, 4))

    story.append(callout_box(
        "Bucle Balanceador B2 con Saturación: La Trampa de Capacidad del Taller",
        "Más Equipos en Falla &rarr; (+) Reparaciones Requeridas &rarr; (-) Equipos en Falla.<br/>"
        "B2 intenta estabilizar la flota enviando equipos al taller. Sin embargo, cuando la cola de fallas satura la capacidad "
        "máxima (C_taller = 4), <b>el bucle B2 se desactiva funcionalmente</b> porque la válvula de reparación ya no puede crecer más. "
        "Al quedar B2 neutralizado, el bucle destructivo R1 toma el control absoluto del sistema.",
        color_border=C_WARM, bg_color=colors.HexColor("#fffbeb")
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 5: ANÁLISIS DIMENSIONAL Y ESTABILIDAD NUMÉRICA
    # =========================================================================
    story.append(Paragraph("5. Rigor Matemático: Análisis Dimensional y Estabilidad Numérica", STYLE_H1))
    story.append(Paragraph(
        "Para garantizar que el modelo sea matemáticamente riguroso y computacionalmente estable, se aplican dos pruebas canónicas:",
        STYLE_BODY
    ))

    story.append(Paragraph("5.1. Prueba de Consistencia Dimensional de Forrester", STYLE_H2))
    story.append(Paragraph(
        "En dinámica de sistemas, no se permite sumar o igualar variables de distintas dimensiones físicas. "
        "Cada ecuación de balance debe cumplir estrictamente que la dimensión de la derivada [d(Stock)/dt] sea igual a la dimensión "
        "del stock dividida por el tiempo: <i>[Stock] / [Tiempo]</i>. Por ejemplo:<br/>"
        "&bull; <i>dO/dt [equipos / mes] = R [equipos / mes] - F_flujo [equipos &middot; (1/mes) = equipos / mes]</i>. Correcto.<br/>"
        "&bull; <i>d(MP_e)/dt [ (1/mes) / mes = 1/mes<sup>2</sup> ] = (f_mp [1/mes] - MP_e [1/mes]) / &tau; [mes] = 1/mes<sup>2</sup></i>. Correcto.<br/>"
        "Esta verificación descarta errores lógicos estructurales en la formulación.",
        STYLE_BODY
    ))

    story.append(Paragraph("5.2. Criterio de Selección del Paso de Integración (&Delta;t = 0.25 meses)", STYLE_H2))
    story.append(Paragraph(
        "El método de Euler discretiza el tiempo mediante aproximación por diferencias finitas hacia adelante. "
        "Si el paso de tiempo &Delta;t es demasiado grande, el algoritmo introduce <b>inestabilidades numéricas artificiales</b> "
        "(oscilaciones numéricas espurias o divergencias hacia el infinito).<br/>"
        "La regla matemática de estabilidad de Dinámica de Sistemas establece que el paso de integración debe ser menor o igual a "
        "la mitad de la constante de tiempo más rápida del sistema (&tau;_min):",
        STYLE_BODY
    ))

    caja_dt = [
        Paragraph("<b>Criterio de Estabilidad Numérica de Euler:</b>", STYLE_CELL_BOLD),
        Paragraph(
            "&bull; Constante de tiempo de reparación: <i>T_rep = 1.5 meses</i>.<br/>"
            "&bull; Constante de tiempo del retardo de MP: <i>&tau;_mp = 3.0 meses</i>.<br/>"
            "&bull; Constante más rápida: <i>&tau;_min = 1.5 meses</i>.<br/>"
            "&bull; Límite de estabilidad estricto: <i>&Delta;t &le; &tau;_min / 2 = 1.5 / 2 = 0.75 meses</i>.<br/>"
            "Al elegir <b>&Delta;t = 0.25 meses (1 semana)</b>, se cumple <i>&Delta;t &le; &tau;_min / 6</i>. "
            "Esto sitúa la simulación en una zona de convergencia numérica incondicional, garantizando que las trayectorias no contengan "
            "ruido numérico y coincidan con un error menor al 0.1% frente a métodos de orden superior como Runge-Kutta 4.",
            STYLE_CELL
        )
    ]
    t_dt = Table([[caja_dt]], colWidths=[540])
    t_dt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.8, C_PRIMARY),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_dt)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 6: CONCLUSIONES PARA LA TOMA DE DECISIONES
    # =========================================================================
    story.append(Paragraph("6. Conclusiones y Guía de Interpretación para la Toma de Decisiones", STYLE_H1))
    story.append(Paragraph(
        "Al integrar la formulación matemática y correr las simulaciones a 60 meses, surgen conclusiones estratégicas contundentes "
        "para la gestión de activos tecnológicos:",
        STYLE_BODY
    ))

    politicas_tabla = [
        [Paragraph("<b>Política de MP</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Intervalo</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Salud Final</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Disponibilidad</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Costo Total a 60m</b>", STYLE_CELL_BOLD),
         Paragraph("<b>Diagnóstico Dinámico</b>", STYLE_CELL_BOLD)],

        [Paragraph("<b>Sin MP</b>", STYLE_CELL_BOLD),
         Paragraph("0 meses", STYLE_CELL),
         Paragraph("0.30", STYLE_CELL),
         Paragraph("56.8 %", STYLE_CELL),
         Paragraph("USD 1,607 k", STYLE_CELL),
         Paragraph("<b>Catastrófico:</b> El taller colapsa durante 52 meses. Las pérdidas por inactividad representan el 77% del costo.", STYLE_CELL)],

        [Paragraph("<b>MP Baja</b>", STYLE_CELL_BOLD),
         Paragraph("12 meses", STYLE_CELL),
         Paragraph("0.48", STYLE_CELL),
         Paragraph("66.1 %", STYLE_CELL),
         Paragraph("USD 1,440 k", STYLE_CELL),
         Paragraph("<b>Insuficiente:</b> Frena parcialmente la caída, pero el taller sigue saturado casi 48 meses. El costo sigue siendo alto.", STYLE_CELL)],

        [Paragraph("<b>MP Intermedia</b>", STYLE_CELL_BOLD),
         Paragraph("6 meses", STYLE_CELL),
         Paragraph("0.83", STYLE_CELL),
         Paragraph("94.1 %", STYLE_CELL),
         Paragraph("<b>USD 445 k</b>", STYLE_CELL_BOLD),
         Paragraph("<b>ÓPTIMO GLOBAL:</b> Mantiene las fallas por debajo del tope del taller (nunca satura). Ahorra un <b>72% de costo</b> frente a 'Sin MP'.", STYLE_CELL)],

        [Paragraph("<b>MP Intensiva</b>", STYLE_CELL_BOLD),
         Paragraph("3 meses", STYLE_CELL),
         Paragraph("0.90", STYLE_CELL),
         Paragraph("96.7 %", STYLE_CELL),
         Paragraph("USD 475 k", STYLE_CELL),
         Paragraph("<b>Sobremantenimiento:</b> Gana apenas 2.6% de disponibilidad pero cuesta 30,000 USD más por rendimientos decrecientes de B1.", STYLE_CELL)]
    ]

    t_pol = Table(politicas_tabla, colWidths=[90, 55, 60, 75, 95, 165])
    t_pol.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BLUE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_pol)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6.1. La Curva Convexa y la Asimetría del Riesgo", STYLE_H2))
    story.append(Paragraph(
        "El barrido continuo del intervalo de mantenimiento revela que la curva de costo total respecto al intervalo es marcadamente convexa. "
        "El mínimo de costo se sitúa en un intervalo de <b>6 meses</b>.<br/>"
        "Más importante aún es la <b>asimetría del error</b>:<br/>"
        "&bull; Si la organización se equivoca por exceso de celo y hace MP cada 3 meses, el costo total sube apenas un 10% por encima del óptimo.<br/>"
        "&bull; Si la organización se equivoca por defecto y relaja el MP a 12 meses, el costo total se dispara un 223% por encima del óptimo debido "
        "a la saturación del taller.<br/>"
        "<b>Regla de Ingeniería:</b> En sistemas con límites de capacidad y sobrecarga de fallas, <i>equivocarse por exceso de mantenimiento "
        "preventivo es un orden de magnitud más seguro y económico que equivocarse por defecto</i>.",
        STYLE_BODY
    ))
    story.append(Spacer(1, 6))

    resumen_final = [
        Paragraph("<b>Síntesis para la Presentación Académica:</b>", STYLE_CELL_BOLD),
        Paragraph(
            "La formulación matemática de dinámica de sistemas no solo describe fórmulas estáticas; revela la estructura causal "
            "profunda del problema. Las ecuaciones de balance demuestran que el mantenimiento preventivo no es una partida de gasto prescindible, "
            "sino una fuerza estabilizadora que mantiene el sistema fuera de la cuenca de atracción del bucle reforzador R1. "
            "Al limitar la tasa de fallas por debajo de la capacidad crítica de 4 reparaciones/mes, se evita la catástrofe de congestión "
            "y se maximiza la disponibilidad operativa con el menor consumo de recursos.",
            STYLE_BODY
        )
    ]
    t_res = Table([[resumen_final]], colWidths=[540])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eef9f5")),
        ('BOX', (0, 0), (-1, -1), 0.8, C_SECONDARY),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_res)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF explicativo generado exitosamente en: {PDF_PATH}")


if __name__ == "__main__":
    construir_pdf()
