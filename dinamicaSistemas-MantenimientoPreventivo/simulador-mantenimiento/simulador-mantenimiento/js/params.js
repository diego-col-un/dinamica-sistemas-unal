"use strict";
/* Parámetros del modelo, escenarios y estado compartido. */
const DEFS = [
  {k:"equipos_totales",label:"Equipos totales",unit:"equipos",min:20,max:500,step:10,def:100,g:"Parque y condiciones iniciales",tip:"Tamaño del parque (constante: sin compras ni bajas)."},
  {k:"falla_inicial",label:"Equipos en falla al inicio",unit:"equipos",min:0,max:50,step:1,def:4,g:"Parque y condiciones iniciales",tip:"Equipos fuera de servicio en t = 0."},
  {k:"salud_inicial",label:"Salud inicial",unit:"0–1",min:0.3,max:1,step:0.01,def:0.85,g:"Parque y condiciones iniciales",tip:"Índice de condición del parque al inicio."},
  {k:"tasa_base_fallas",label:"Tasa base de fallas",unit:"1/mes",min:0.005,max:0.06,step:0.001,def:0.02,g:"Fallas y degradación",tip:"Fracción de equipos que falla por mes con salud perfecta."},
  {k:"sens_falla_salud",label:"Sensibilidad falla–salud",unit:"adim.",min:0,max:10,step:0.5,def:4,g:"Fallas y degradación",tip:"Cuánto crece la tasa de fallas al perder salud (con salud 0 es 1 + este valor veces la base)."},
  {k:"tasa_base_degradacion",label:"Tasa base de degradación",unit:"1/mes",min:0.005,max:0.08,step:0.001,def:0.025,g:"Fallas y degradación",tip:"Desgaste natural mensual de la salud."},
  {k:"factor_sobrecarga",label:"Factor de sobrecarga",unit:"adim.",min:0,max:6,step:0.1,def:2,g:"Fallas y degradación",tip:"Degradación extra cuando hay equipos parados (más carga sobre los operativos)."},
  {k:"efectividad_mp",label:"Efectividad del MP",unit:"adim.",min:0.1,max:1,step:0.05,def:0.6,g:"Mantenimiento preventivo",tip:"Fracción de la brecha de salud que recupera cada intervención por mes."},
  {k:"retraso_mp",label:"Retraso del efecto del MP",unit:"meses",min:0.5,max:12,step:0.5,def:3,g:"Mantenimiento preventivo",tip:"El efecto del MP sobre la salud llega con retraso de primer orden."},
  {k:"intervalo_custom",label:"Intervalo MP del escenario personalizado",unit:"meses",min:0,max:24,step:0.5,def:8,g:"Mantenimiento preventivo",tip:"Meses entre intervenciones por equipo (0 = sin MP). Se suma a los 4 escenarios fijos."},
  {k:"tiempo_reparacion",label:"Tiempo de reparación",unit:"meses",min:0.5,max:6,step:0.25,def:1.5,g:"Taller de reparación",tip:"Tiempo medio que tarda una reparación."},
  {k:"capacidad_taller",label:"Capacidad del taller",unit:"equipos/mes",min:1,max:15,step:0.5,def:4,g:"Taller de reparación",tip:"Máximo de reparaciones por mes. Si las fallas lo superan se forma cola."},
  {k:"costo_mp",label:"Costo unitario MP",unit:"USD",min:20,max:500,step:10,def:120,g:"Costos",tip:"Costo de una intervención preventiva."},
  {k:"costo_mc",label:"Costo unitario MC",unit:"USD",min:100,max:3000,step:50,def:900,g:"Costos",tip:"Costo de una reparación correctiva."},
  {k:"costo_inactividad",label:"Costo de inactividad",unit:"USD/equipo-mes",min:100,max:2000,step:50,def:600,g:"Costos",tip:"Pérdida por cada equipo fuera de servicio durante un mes."},
  {k:"horizonte",label:"Horizonte de simulación",unit:"meses",min:12,max:120,step:6,def:60,g:"Simulación",tip:"Duración de la simulación."},
];

/* Opciones del método numérico (no son parámetros del modelo). */
const DT_OPCIONES = [1, 0.5, 0.25, 0.125, 0.0625];
const NUM_DEF = {metodo: "euler", dt: 0.25};

const FIXED = [
  {name:"Sin MP",iv:0,color:"#8c8c8c"},
  {name:"MP baja (cada 12 m)",iv:12,color:"#d98b2b"},
  {name:"MP intermedia (cada 6 m)",iv:6,color:"#2a7f62"},
  {name:"MP intensiva (cada 3 m)",iv:3,color:"#2b5fa8"},
];
const CUSTOM_COLOR = "#8a4fb3";

const state = {...NUM_DEF};
DEFS.forEach(d => state[d.k] = d.def);
const hidden = new Set();
let interpretacion = null;   // {texto, firma, fecha}
