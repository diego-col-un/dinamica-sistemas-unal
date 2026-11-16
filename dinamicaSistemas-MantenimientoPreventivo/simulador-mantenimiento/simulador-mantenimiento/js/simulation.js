"use strict";
/* =====================================================================
   Motor de simulación (dinámica de sistemas, niveles y flujos).

   Vector de niveles y = [O, F, S, Cm, Ci, MPe]
     O   equipos operativos
     F   equipos en falla
     S   salud del parque (0–1)
     Cm  costo acumulado de mantenimiento (MP + MC)
     Ci  costo acumulado de inactividad
     MPe esfuerzo de MP efectivo (retraso de primer orden)

   El sistema es dy/dt = f(y). El método de Euler avanza así:
        y(t + dt) = y(t) + dt * f(y(t))
   ===================================================================== */

/* Flujos del modelo en el estado y, para una frecuencia de MP dada. */
function flujos(y, p, frec){
  const [O, F, S, , , MPe] = y, N = p.equipos_totales;
  const tasaFallas   = p.tasa_base_fallas * (1 + p.sens_falla_salud * (1 - S));
  const fallas       = O * tasaFallas;
  const reparaciones = Math.min(F / p.tiempo_reparacion, p.capacidad_taller);
  const degradacion  = S * p.tasa_base_degradacion * (1 + p.factor_sobrecarga * F / N);
  const recuperacion = (1 - S) * p.efectividad_mp * MPe;
  return {
    fallas, reparaciones, degradacion, recuperacion,
    saturado: reparaciones >= p.capacidad_taller - 1e-9,
    costoMP: frec * O * p.costo_mp,
    costoMC: reparaciones * p.costo_mc,
    costoIn: F * p.costo_inactividad,
  };
}

/* Derivadas dy/dt. */
function derivadas(y, p, frec){
  const f = flujos(y, p, frec);
  return [
    f.reparaciones - f.fallas,           // dO/dt
    f.fallas - f.reparaciones,           // dF/dt
    f.recuperacion - f.degradacion,      // dS/dt
    f.costoMP + f.costoMC,               // dCm/dt
    f.costoIn,                           // dCi/dt
    (frec - y[5]) / p.retraso_mp,        // dMPe/dt
  ];
}

/* ---------- Métodos de integración ---------- */
function pasoEuler(y, p, frec, dt){
  const d = derivadas(y, p, frec);
  return y.map((v, i) => v + dt * d[i]);
}

function pasoRK4(y, p, frec, dt){   // solo como referencia para comparar
  const add = (a, b, h) => a.map((v, i) => v + h * b[i]);
  const k1 = derivadas(y, p, frec);
  const k2 = derivadas(add(y, k1, dt/2), p, frec);
  const k3 = derivadas(add(y, k2, dt/2), p, frec);
  const k4 = derivadas(add(y, k3, dt), p, frec);
  return y.map((v, i) => v + dt/6 * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]));
}

const METODOS = {
  euler: {nombre: "Euler (explícito)", paso: pasoEuler},
  rk4:   {nombre: "Runge-Kutta 4 (referencia)", paso: pasoRK4},
};

/* ---------- Simulación de un escenario ---------- */
function simulate(interval, p){
  const dt = p.dt, T = p.horizonte, n = Math.round(T / dt) + 1, N = p.equipos_totales;
  const frec = interval > 0 ? 1 / interval : 0;
  const paso = (METODOS[p.metodo] || METODOS.euler).paso;

  let y = [N - Math.min(p.falla_inicial, N), Math.min(p.falla_inicial, N), p.salud_inicial, 0, 0, 0];
  const t = new Array(n), salud = new Array(n), disp = new Array(n), inact = new Array(n), total = new Array(n);
  let sat = 0, dispSum = 0, inactSum = 0;

  for (let k = 0; k < n; k++){
    t[k] = k * dt;
    salud[k] = y[2];
    disp[k] = 100 * y[0] / N;
    inact[k] = 100 * y[1] / N;
    total[k] = (y[3] + y[4]) / 1000;
    dispSum += disp[k]; inactSum += inact[k];
    if (flujos(y, p, frec).saturado) sat += dt;
    if (k < n - 1) y = paso(y, p, frec, dt);
  }
  return {t, salud, disp, inact, total, sat,
    saludFinal: y[2], dispMedia: dispSum / n, inactMedia: inactSum / n,
    costoMant: y[3], costoInact: y[4], costoTotal: y[3] + y[4]};
}
