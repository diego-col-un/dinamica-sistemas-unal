"""
Modelo de Dinámica de Sistemas: mantenimiento de un parque de equipos tecnológicos.
Integración de Euler (igual que Vensim). Horizonte: 60 meses.
Las ecuaciones son idénticas a las de documento.mdl.
"""
import numpy as np

# ---------------- Parámetros (supuestos del modelo, ver reporte) ----------------
PARAMS = dict(
    equipos_totales=100.0,        # equipos
    falla_inicial=4.0,            # equipos fallados al inicio
    salud_inicial=0.85,           # índice 0-1
    tasa_base_fallas=0.02,        # 1/mes (equipo en salud perfecta)
    sens_falla_salud=4.0,         # adim: cuánto crece la tasa de fallas al perder salud
    tasa_base_degradacion=0.025,  # 1/mes
    factor_sobrecarga=2.0,        # adim: degradación extra por equipos fuera de servicio
    efectividad_mp=0.6,           # adim: fracción de la brecha de salud recuperada por MP
    retraso_mp=3.0,               # meses: retraso del efecto del MP sobre la salud
    tiempo_reparacion=1.5,        # meses
    capacidad_taller=4.0,         # reparaciones/mes
    costo_mp=120.0,               # USD por intervención preventiva
    costo_mc=900.0,               # USD por reparación correctiva
    costo_inactividad=600.0,      # USD por equipo-mes fuera de servicio
)

# Escenarios de política: intervalo entre MP por equipo (meses). 0 = sin MP.
ESCENARIOS = {
    "Sin MP": 0.0,
    "MP baja (cada 12 m)": 12.0,
    "MP intermedia (cada 6 m)": 6.0,
    "MP intensiva (cada 3 m)": 3.0,
}

T_FINAL, DT = 60.0, 0.25


def simular(intervalo_mp, p=None, t_final=T_FINAL, dt=DT):
    p = {**PARAMS, **(p or {})}
    n = int(round(t_final / dt)) + 1
    t = np.arange(n) * dt
    N = p["equipos_totales"]
    frec_mp = 0.0 if intervalo_mp == 0 else 1.0 / intervalo_mp

    O = np.zeros(n); F = np.zeros(n); S = np.zeros(n)
    Cm = np.zeros(n); Ci = np.zeros(n); MPe = np.zeros(n)
    fallas = np.zeros(n); repar = np.zeros(n)

    F[0] = p["falla_inicial"]; O[0] = N - F[0]; S[0] = p["salud_inicial"]
    MPe[0] = 0.0   # la política se introduce en t=0 -> el efecto llega con retraso

    for k in range(n):
        tasa_f = p["tasa_base_fallas"] * (1 + p["sens_falla_salud"] * (1 - S[k]))
        fallas[k] = O[k] * tasa_f
        repar[k] = min(F[k] / p["tiempo_reparacion"], p["capacidad_taller"])
        deg = S[k] * p["tasa_base_degradacion"] * (1 + p["factor_sobrecarga"] * F[k] / N)
        rec = (1 - S[k]) * p["efectividad_mp"] * MPe[k]
        c_mp = frec_mp * O[k] * p["costo_mp"]
        c_mc = repar[k] * p["costo_mc"]
        c_in = F[k] * p["costo_inactividad"]
        if k == n - 1:
            break
        O[k+1] = O[k] + dt * (repar[k] - fallas[k])
        F[k+1] = F[k] + dt * (fallas[k] - repar[k])
        S[k+1] = S[k] + dt * (rec - deg)
        Cm[k+1] = Cm[k] + dt * (c_mp + c_mc)
        Ci[k+1] = Ci[k] + dt * c_in
        MPe[k+1] = MPe[k] + dt * (frec_mp - MPe[k]) / p["retraso_mp"]

    return dict(t=t, operativos=O, en_falla=F, salud=S, costo_mant=Cm, costo_inact=Ci,
                costo_total=Cm + Ci, disponibilidad=O / N, inactividad_pct=100 * F / N,
                fallas=fallas, reparaciones=repar, mp_efectivo=MPe)


def resumen(res):
    return dict(
        salud_final=res["salud"][-1],
        disp_final=100 * res["disponibilidad"][-1],
        disp_media=100 * res["disponibilidad"].mean(),
        inact_media=res["inactividad_pct"].mean(),
        costo_mant=res["costo_mant"][-1],
        costo_inact=res["costo_inact"][-1],
        costo_total=res["costo_total"][-1],
    )


if __name__ == "__main__":
    for nombre, iv in ESCENARIOS.items():
        r = resumen(simular(iv))
        print(f"{nombre:28s}", {k: round(v, 1) for k, v in r.items()})
