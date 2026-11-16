"""
Dibuja el diagrama de bucles causales y el diagrama de Forrester (niveles y flujos).
Uso:  python diagramas.py   (desde scripts/)  ->  ../diagramas/diagrama_causal.png, diagrama_forrester.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Ellipse, Polygon, FancyBboxPatch

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "diagramas")

AZUL, ROJO, VERDE, GRIS, NARANJA = "#2b5fa8", "#c0503a", "#2a7f62", "#555555", "#d98b2b"


# =====================================================================
# 1. DIAGRAMA CAUSAL
# =====================================================================
def diagrama_causal():
    fig, ax = plt.subplots(figsize=(13, 8.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal")
    ax.axis("off")

    nodos = {  # nombre: (x, y, ancho, alto)
        "Salud del parque": (3.2, 4.3, 2.6, 0.8),
        "Tasa de fallas": (3.2, 7.4, 2.6, 0.8),
        "Equipos en falla\n(inactividad)": (8.3, 7.4, 2.8, 0.95),
        "Degradación": (8.3, 4.3, 2.6, 0.8),
        "Recuperación\npor MP": (3.2, 1.3, 2.6, 0.95),
        "MP efectivo": (6.7, 1.3, 2.2, 0.8),
        "Frecuencia de MP\n(política)": (10.4, 1.3, 2.6, 0.95),
        "Reparación": (11.7, 7.4, 2.0, 0.8),
        "Capacidad\ndel taller": (11.7, 4.9, 2.0, 0.95),
    }
    patches = {}
    for nombre, (x, y, w, h) in nodos.items():
        es_politica = "política" in nombre
        r = Rectangle((x - w / 2, y - h / 2), w, h, fc="#eef3fb" if not es_politica else "#fdf1dc",
                      ec=AZUL if not es_politica else NARANJA, lw=1.6, zorder=2)
        ax.add_patch(r)
        ax.text(x, y, nombre, ha="center", va="center", fontsize=10, zorder=3)
        patches[nombre] = r

    def flecha(a, b, signo, rad=0.0, color=GRIS, retraso=False, off=0.22):
        pa, pb = nodos[a], nodos[b]
        arr = FancyArrowPatch((pa[0], pa[1]), (pb[0], pb[1]), patchA=patches[a], patchB=patches[b],
                              arrowstyle="-|>", mutation_scale=16, lw=1.8, color=color,
                              connectionstyle=f"arc3,rad={rad}", shrinkA=3, shrinkB=3, zorder=1)
        ax.add_patch(arr)
        # punto medio de la curva y etiqueta de polaridad
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        cx, cy = mx + 0.5 * rad * dy, my - 0.5 * rad * dx
        n = (dx ** 2 + dy ** 2) ** 0.5
        # desplazamiento hacia el lado de la curvatura
        sgn = 1 if rad >= 0 else -1
        ox, oy = sgn * dy / n * off, -sgn * dx / n * off
        if rad == 0:
            ox, oy = dy / n * off, -dx / n * off
        ax.text(cx + ox, cy + oy, signo, color=color, fontsize=15, fontweight="bold", ha="center",
                va="center", zorder=4,
                bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
        if retraso:
            ax.text(cx, cy, "//", color=color, fontsize=16, fontweight="bold", ha="center", va="center",
                    rotation=-30, zorder=4)

    # Bucle R1: círculo vicioso de degradación
    flecha("Salud del parque", "Tasa de fallas", "-", rad=0.0, color=ROJO)
    flecha("Tasa de fallas", "Equipos en falla\n(inactividad)", "+", color=ROJO)
    flecha("Equipos en falla\n(inactividad)", "Degradación", "+", color=ROJO)
    flecha("Degradación", "Salud del parque", "-", color=ROJO)
    # Bucle B1: efecto del MP (brecha de salud)
    flecha("Salud del parque", "Recuperación\npor MP", "-", rad=0.35, color=VERDE)
    flecha("Recuperación\npor MP", "Salud del parque", "+", rad=0.35, color=VERDE)
    flecha("Frecuencia de MP\n(política)", "MP efectivo", "+", color=GRIS, retraso=True)
    flecha("MP efectivo", "Recuperación\npor MP", "+", color=GRIS)
    # Bucle B2: reparación
    flecha("Equipos en falla\n(inactividad)", "Reparación", "+", rad=0.3, color=AZUL)
    flecha("Reparación", "Equipos en falla\n(inactividad)", "-", rad=0.3, color=AZUL)
    flecha("Capacidad\ndel taller", "Reparación", "+", color=GRIS)

    # etiquetas de bucles
    def etiqueta_bucle(x, y, txt, color):
        ax.text(x, y, txt, ha="center", va="center", fontsize=10.5, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=color, lw=1.4), zorder=5)

    etiqueta_bucle(5.75, 5.85, "R1  Círculo vicioso\nde degradación", ROJO)
    etiqueta_bucle(1.15, 2.8, "B1  Efecto\ndel MP", VERDE)
    etiqueta_bucle(10.0, 6.0, "B2  Reparación\n(satura el taller)", AZUL)

    ax.text(0.1, 8.45, "Diagrama de bucles causales: mantenimiento de un parque de equipos tecnológicos",
            fontsize=12, fontweight="bold", va="top")
    ax.text(0.1, 0.35, "+  : misma dirección     -  : dirección opuesta     //  : retraso     "
            "R: bucle reforzador     B: bucle estabilizador", fontsize=9, color=GRIS)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "diagrama_causal.png"), dpi=170)
    plt.close(fig)


# =====================================================================
# 2. DIAGRAMA DE FORRESTER
# =====================================================================
def diagrama_forrester():
    fig, ax = plt.subplots(figsize=(16, 11.4))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11.4)
    ax.set_aspect("equal")
    ax.axis("off")
    PIPE = "#7ea6d6"

    def stock(x, y, w, h, txt, fs=10):
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#dce9f9", ec=AZUL, lw=2.2, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, fontweight="bold", zorder=4)

    def cloud(x, y):
        for dx, dy in [(-0.12, 0), (0.12, 0), (0, 0.1), (0, -0.08)]:
            ax.add_patch(Ellipse((x + dx, y + dy), 0.4, 0.3, fc="white", ec=GRIS, lw=1.2, zorder=3))

    def pipe(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="simple,head_width=1.1,head_length=0.9,tail_width=0.45",
                                    fc=PIPE, ec=AZUL, lw=1.0, shrinkA=0, shrinkB=0), zorder=2)

    def valve(x, y):
        s = 0.22
        ax.add_patch(Polygon([(x - s, y + s), (x - s, y - s), (x + s, y + s), (x + s, y - s)],
                             closed=True, fc="white", ec=AZUL, lw=1.8, zorder=5))

    def label(x, y, txt, fs=9.5, ha="center", bold=False, color="black"):
        ax.text(x, y, txt, ha=ha, va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=6)

    def aux(x, y, txt, param=False):
        ax.text(x, y, txt, ha="center", va="center", fontsize=9, zorder=6,
                bbox=dict(boxstyle="round,pad=0.28", fc="#fff6e0" if not param else "#f1f1f1",
                          ec=NARANJA if not param else "#999999", lw=1.1))

    def info(p1, p2, rad=0.0, color=ROJO):
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11, lw=1.2, color=color,
                                     linestyle=(0, (4, 3)), connectionstyle=f"arc3,rad={rad}",
                                     shrinkA=0, shrinkB=0, zorder=4))

    # ---- Niveles
    stock(3.2, 4.2, 2.8, 1.5, "Equipos\noperativos")
    stock(11.0, 4.2, 2.8, 1.5, "Equipos\nen falla")
    stock(7.0, 9.4, 3.0, 1.3, "Salud\ndel parque")

    # ---- Flujo Fallas (O -> F) y Reparación (F -> O)
    pipe(4.6, 4.6, 9.6, 4.6)
    valve(7.0, 4.6)
    label(7.9, 5.0, "Fallas", bold=True, ha="left")
    pipe(9.6, 3.8, 4.6, 3.8)
    valve(7.0, 3.8)
    label(7.0, 3.35, "Reparación", bold=True)

    # ---- Flujo Recuperación por MP (nube -> Salud) y Degradación (Salud -> nube)
    cloud(1.0, 9.4)
    pipe(1.2, 9.4, 5.5, 9.4)
    valve(3.6, 9.4)
    label(3.6, 10.05, "Recuperación por MP", bold=True)
    pipe(8.5, 9.4, 12.5, 9.4)
    valve(10.4, 9.4)
    cloud(12.8, 9.4)
    label(10.4, 10.05, "Degradación", bold=True)

    # ---- Auxiliares: Tasa de fallas
    aux(7.0, 7.3, "Tasa de fallas")
    aux(4.6, 6.0, "Tasa base de fallas", param=True)
    aux(9.3, 6.0, "Sensibilidad\nfalla-salud", param=True)
    info((7.0, 8.75), (7.0, 7.62))                 # Salud -> Tasa de fallas
    info((7.0, 6.98), (7.0, 4.85))                 # Tasa de fallas -> Fallas
    info((5.1, 6.28), (6.55, 7.1), color=GRIS)
    info((8.9, 6.3), (7.5, 7.1), color=GRIS)
    info((3.9, 4.95), (6.8, 4.75), rad=-0.35)      # Operativos -> Fallas

    # ---- Reparación: capacidad y tiempo
    aux(5.6, 2.0, "Tiempo de\nreparación", param=True)
    aux(8.6, 2.0, "Capacidad\ndel taller", param=True)
    info((5.9, 2.45), (6.8, 3.6), color=GRIS)
    info((8.4, 2.45), (7.2, 3.6), color=GRIS)
    info((10.6, 3.45), (7.25, 3.65), rad=0.35)     # En falla -> Reparación

    # ---- Degradación: sobrecarga
    aux(11.0, 6.5, "Fracción de equipos\nen falla")
    aux(13.9, 6.7, "Factor de\nsobrecarga", param=True)
    aux(14.2, 8.0, "Tasa base de\ndegradación", param=True)
    info((11.0, 4.98), (11.0, 6.0))
    info((10.8, 7.05), (10.5, 9.1))
    info((13.5, 7.05), (10.65, 9.15), color=GRIS)
    info((13.7, 7.7), (10.7, 9.25), color=GRIS)
    info((8.6, 10.1), (10.25, 9.8), rad=-0.35)     # Salud -> Degradación

    # ---- Recuperación por MP: MP efectivo con retraso
    aux(3.6, 7.6, "MP efectivo\n(DELAY1: retraso\ndel efecto)")
    aux(1.3, 8.0, "Retraso\ndel efecto MP", param=True)
    aux(1.3, 6.5, "Frecuencia MP", param=False)
    aux(1.3, 5.3, "Intervalo MP\n(escenario)", param=True)
    aux(1.4, 10.65, "Efectividad\ndel MP", param=True)
    info((3.6, 8.2), (3.6, 9.12))
    info((2.0, 7.95), (2.85, 7.75), color=GRIS)
    info((1.85, 6.55), (2.9, 7.2))
    info((1.3, 5.7), (1.3, 6.15), color=GRIS)
    info((2.0, 10.4), (3.4, 9.7), color=GRIS)
    info((6.2, 10.1), (3.9, 9.8), rad=0.35)        # Salud -> Recuperación (brecha 1-S)

    # ---- Costos (acumuladores)
    cloud(0.8, 0.8)
    pipe(1.0, 0.8, 3.0, 0.8)
    valve(2.0, 0.8)
    stock(4.6, 0.8, 3.4, 1.1, "Costo acumulado\nde mantenimiento", fs=9.5)
    label(2.0, 1.4, "Costo MP + MC", fs=9, bold=True)
    aux(1.6, 2.5, "Costos unitarios\nMP y MC", param=True)
    info((1.7, 2.1), (2.0, 1.1), color=GRIS)
    info((6.8, 3.55), (2.2, 1.1), rad=-0.15)

    pipe(10.2, 0.8, 12.0, 0.8)
    valve(11.1, 0.8)
    cloud(9.8, 0.8)
    stock(13.7, 0.8, 3.4, 1.1, "Costo acumulado\nde inactividad", fs=9.5)
    label(11.1, 1.4, "Costo inactividad", fs=9, bold=True)
    aux(13.3, 2.6, "Costo por\nequipo-mes parado", param=True)
    info((13.0, 2.2), (11.3, 1.1), color=GRIS)
    info((11.5, 3.45), (11.2, 1.1), rad=-0.1)

    ax.text(0.2, 11.2, "Diagrama de Forrester (niveles y flujos): parque de equipos tecnológicos", fontsize=13,
            fontweight="bold", va="top")
    ax.text(0.2, 0.0, "Rectángulos: niveles | válvulas: flujos | amarillo: auxiliares | gris: parámetros | "
            "flechas rojas punteadas: información", fontsize=9, color=GRIS, va="bottom")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "diagrama_forrester.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    diagrama_causal()
    diagrama_forrester()
    print("Diagramas generados en", os.path.abspath(OUT))
