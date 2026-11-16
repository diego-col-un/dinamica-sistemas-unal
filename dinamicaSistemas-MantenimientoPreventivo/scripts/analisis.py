"""
Genera las gráficas de resultados, el análisis de sensibilidad y las pruebas de validación.
Uso:  python analisis.py     (desde la carpeta scripts/)
Salidas: ../diagramas/resultados_*.png y resultados.json (lo consume el reporte)
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modelo_mantenimiento import PARAMS, ESCENARIOS, simular, resumen

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "diagramas")
COLORES = ["#8c8c8c", "#d98b2b", "#2a7f62", "#2b5fa8"]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25})

resultados = {}

# ---------------------------------------------------------------- 1. Escenarios
sims = {n: simular(iv) for n, iv in ESCENARIOS.items()}
resultados["escenarios"] = {n: {k: float(v) for k, v in resumen(r).items()} for n, r in sims.items()}

fig, ax = plt.subplots(2, 2, figsize=(11, 7.5))
paneles = [("salud", "Salud del parque (índice 0-1)", 1),
           ("disponibilidad", "Disponibilidad (fracción de equipos operativos)", 1),
           ("inactividad_pct", "Inactividad del parque (% de equipos fuera de servicio)", 1),
           ("costo_total", "Costo total acumulado (USD)", 1)]
for a, (clave, titulo, _) in zip(ax.ravel(), paneles):
    for (nombre, r), c in zip(sims.items(), COLORES):
        a.plot(r["t"], r[clave], label=nombre, color=c, lw=2)
    a.set_title(titulo, fontsize=10.5, loc="left")
    a.set_xlabel("Mes")
    a.set_xlim(0, 60)
ax[0, 0].legend(frameon=False, fontsize=9)
ax[1, 1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1e3:,.0f} k"))
fig.suptitle("Trayectorias a 60 meses por escenario de política", x=0.01, ha="left", fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "resultados_trayectorias.png"), dpi=170)
plt.close(fig)

# Composición del costo
fig, a = plt.subplots(figsize=(8.5, 4.8))
nombres = list(sims)
mant = [sims[n]["costo_mant"][-1] / 1e3 for n in nombres]
inact = [sims[n]["costo_inact"][-1] / 1e3 for n in nombres]
x = np.arange(len(nombres))
a.bar(x, mant, color="#2b5fa8", label="Mantenimiento (MP + MC)")
a.bar(x, inact, bottom=mant, color="#d98b2b", label="Inactividad")
for i, (m, c) in enumerate(zip(mant, inact)):
    a.text(i, m + c + 15, f"{m + c:,.0f} k", ha="center", fontweight="bold")
a.set_xticks(x)
a.set_xticklabels([n.replace(" (", "\n(") for n in nombres])
a.set_ylabel("USD acumulados a 60 meses (miles)")
a.set_title("Composición del costo total por escenario", loc="left")
a.legend(frameon=False)
a.grid(axis="x", visible=False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "resultados_costos.png"), dpi=170)
plt.close(fig)

# ---------------------------------------------------------------- 2. Barrido del intervalo de MP
intervalos = np.arange(1, 25, 0.5)
barrido = {}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
for ef, c in zip([0.4, 0.6, 0.8], ["#d98b2b", "#2a7f62", "#2b5fa8"]):
    costos = [simular(iv, {"efectividad_mp": ef})["costo_total"][-1] / 1e3 for iv in intervalos]
    disp = [100 * simular(iv, {"efectividad_mp": ef})["disponibilidad"].mean() for iv in intervalos]
    i = int(np.argmin(costos))
    barrido[str(ef)] = dict(intervalo_optimo=float(intervalos[i]), costo_min=float(costos[i]))
    a1.plot(intervalos, costos, color=c, lw=2, label=f"Efectividad MP = {ef}")
    a1.plot(intervalos[i], costos[i], "o", color=c)
    a2.plot(intervalos, disp, color=c, lw=2)
a1.set_xlabel("Intervalo entre MP (meses)")
a1.set_ylabel("Costo total a 60 m (miles USD)")
a1.set_title("Costo total vs. intervalo de MP (punto = mínimo)", loc="left", fontsize=10.5)
a1.legend(frameon=False)
a2.set_xlabel("Intervalo entre MP (meses)")
a2.set_ylabel("Disponibilidad media (%)")
a2.set_title("Disponibilidad media vs. intervalo de MP", loc="left", fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "resultados_intervalo_optimo.png"), dpi=170)
plt.close(fig)
resultados["barrido_intervalo"] = barrido

# ---------------------------------------------------------------- 3. Tornado (escenario intermedio)
base = simular(6.0)
c0, d0 = base["costo_total"][-1], 100 * base["disponibilidad"].mean()
etiquetas = {
    "tasa_base_fallas": "Tasa base de fallas",
    "tasa_base_degradacion": "Tasa base de degradación",
    "efectividad_mp": "Efectividad del MP",
    "retraso_mp": "Retraso del efecto del MP",
    "capacidad_taller": "Capacidad del taller",
    "factor_sobrecarga": "Factor de sobrecarga",
    "sens_falla_salud": "Sensibilidad falla a salud",
    "costo_mc": "Costo unitario MC",
    "costo_mp": "Costo unitario MP",
    "costo_inactividad": "Costo de inactividad",
}
filas = []
for k, et in etiquetas.items():
    bajo = simular(6.0, {k: PARAMS[k] * 0.75})
    alto = simular(6.0, {k: PARAMS[k] * 1.25})
    filas.append((et, bajo["costo_total"][-1] - c0, alto["costo_total"][-1] - c0,
                  100 * bajo["disponibilidad"].mean() - d0, 100 * alto["disponibilidad"].mean() - d0))
filas.sort(key=lambda f: max(abs(f[1]), abs(f[2])))
fig, a = plt.subplots(figsize=(9, 5.2))
for i, (et, lo, hi, _, _) in enumerate(filas):
    a.barh(i, lo / 1e3, color="#2a7f62", height=0.6)
    a.barh(i, hi / 1e3, color="#c0503a", height=0.6)
a.set_yticks(range(len(filas)))
a.set_yticklabels([f[0] for f in filas])
a.axvline(0, color="k", lw=0.8)
a.set_xlabel(f"Cambio en el costo total vs. caso base ({c0/1e3:,.0f} k USD), miles USD")
a.set_title("Sensibilidad (MP cada 6 m): verde = parámetro -25 %, rojo = parámetro +25 %", loc="left", fontsize=10.5)
a.grid(axis="y", visible=False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "resultados_sensibilidad.png"), dpi=170)
plt.close(fig)
resultados["sensibilidad"] = [dict(parametro=f[0], costo_m25=float(f[1]), costo_p25=float(f[2]),
                                   disp_m25=float(f[3]), disp_p25=float(f[4])) for f in reversed(filas)]
resultados["base_intermedia"] = dict(costo_total=float(c0), disp_media=float(d0))

# ---------------------------------------------------------------- 4. Pruebas de validación
val = {}
# (a) conservación de equipos
val["conservacion_max_error"] = float(max(np.abs(r["operativos"] + r["en_falla"] - PARAMS["equipos_totales"]).max()
                                          for r in sims.values()))
# (b) sensibilidad al paso de integración
val["paso_integracion"] = {str(dt): float(simular(6.0, dt=dt)["costo_total"][-1])
                           for dt in (0.5, 0.25, 0.125, 0.0625)}
# (c) condiciones extremas
r = simular(6.0, {"tasa_base_fallas": 0.0})
val["sin_fallas_en_falla_final"] = float(r["en_falla"][-1])
r = simular(0.0, {"tasa_base_degradacion": 0.0, "factor_sobrecarga": 0.0})
val["sin_degradacion_salud_final"] = float(r["salud"][-1])
r = simular(0.0, {"capacidad_taller": 1e6})
val["taller_ilimitado_inact_media"] = float(r["inactividad_pct"].mean())
r = simular(0.0)
val["sin_mp_inact_media"] = float(r["inactividad_pct"].mean())
# (d) salud acotada en [0,1]
val["salud_min_max"] = [float(min(r["salud"].min() for r in sims.values())),
                        float(max(r["salud"].max() for r in sims.values()))]
resultados["validacion"] = val

# Efecto del retraso (salud mínima en el escenario intermedio con distintos retrasos)
resultados["retraso"] = {str(d): dict(salud_min=float(simular(6.0, {"retraso_mp": d})["salud"].min()),
                                      salud_final=float(simular(6.0, {"retraso_mp": d})["salud"][-1]))
                         for d in (0.5, 3.0, 6.0, 12.0)}

with open(os.path.join(AQUI, "resultados.json"), "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)
print(json.dumps(resultados, indent=2, ensure_ascii=False))
