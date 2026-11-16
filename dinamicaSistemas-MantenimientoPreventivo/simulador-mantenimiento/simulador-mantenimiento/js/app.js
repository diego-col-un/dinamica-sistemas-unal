"use strict";
/* Cálculo, render de la interfaz y arranque. */
let sims = [], sweep = {xs: [], ys: [], best: null};
/* estado de la ejecución: idle | running | paused | done */
const run = {estado: "idle", k: 0, kf: 0, n: 0, last: 0, raf: null};

function compute(){
  const p = state;
  sims = FIXED.map(s => ({...s, r: simulate(s.iv, p)}));
  const civ = p.intervalo_custom;
  sims.push({name: `Personalizado (${civ > 0 ? "cada " + fnum(civ, civ % 1 ? 1 : 0) + " m" : "sin MP"})`, iv: civ, color: CUSTOM_COLOR, dash: true, r: simulate(civ, p)});
  const xs = [], ys = [];
  for (let iv = 1; iv <= 24; iv += 0.5){ xs.push(iv); ys.push(simulate(iv, p).costoTotal / 1000); }
  let bi = 0; ys.forEach((v, i) => { if (v < ys[bi]) bi = i; });
  sweep = {xs, ys, best: {iv: xs[bi], cost: ys[bi]}};
}

function renderKPI(){
  const T = state.horizonte;
  $("subtitle").textContent = `Dinámica de sistemas (niveles y flujos de Forrester) · método: ${METODOS[state.metodo].nombre} · paso ${state.dt} mes`;
  $("kpiTitle").textContent = `Indicadores a ${T} meses`;
  const minCost = Math.min(...sims.map(s => s.r.costoTotal));
  let h = `<table><thead><tr><th>Escenario</th><th>Salud final</th><th>Disponibilidad media</th><th>Inactividad media</th><th>Meses con taller saturado</th><th>Costo mant. (USD)</th><th>Costo inact. (USD)</th><th>Costo total (USD)</th></tr></thead><tbody>`;
  sims.forEach(s => {
    const r = s.r, best = r.costoTotal === minCost;
    h += `<tr class="${best ? "best" : ""}"><td><span class="dot" style="background:${s.color}"></span>${esc(s.name)}${best ? '<span class="tag">menor costo</span>' : ""}</td>` +
      `<td>${fnum(r.saludFinal, 2)}</td><td>${fnum(r.dispMedia)} %</td><td>${fnum(r.inactMedia)} %</td><td>${fnum(r.sat)} de ${T}</td><td>${fk(r.costoMant)}</td><td>${fk(r.costoInact)}</td><td>${fk(r.costoTotal)}</td></tr>`;
  });
  $("kpi").innerHTML = h + "</tbody></table>";

  const byCost = [...sims].sort((a, b) => a.r.costoTotal - b.r.costoTotal);
  const byDisp = [...sims].sort((a, b) => b.r.dispMedia - a.r.dispMedia);
  const sat = sims.filter(s => s.r.sat > 0.01).map(s => `${s.name}: ${fnum(s.r.sat)} de ${T} meses`);
  const li = [
    `Menor costo total: <b>${esc(byCost[0].name)}</b> (USD ${fk(byCost[0].r.costoTotal)}); el más caro es ${esc(byCost[byCost.length-1].name)} (USD ${fk(byCost[byCost.length-1].r.costoTotal)}).`,
    `Mayor disponibilidad media: <b>${esc(byDisp[0].name)}</b> (${fnum(byDisp[0].r.dispMedia)} %).`,
    sat.length ? `Taller saturado (reparaciones al tope de capacidad): ${esc(sat.join("; "))}.` : "El taller no se satura en ningún escenario con estos parámetros.",
    `Barrido de intervalos (1 a 24 meses): costo total mínimo con MP cada <b>${fnum(sweep.best.iv, sweep.best.iv % 1 ? 1 : 0)} meses</b> (USD ${fnum(sweep.best.cost, 0)} k).`,
  ];
  $("lectura").innerHTML = li.map(x => `<li>${x}</li>`).join("");
}


function renderCharts(k){
  const lg = $("legend");
  lg.innerHTML = sims.map((s, i) => `<button data-i="${i}" class="${hidden.has(i) ? "off" : ""}"><span class="dot" style="background:${s.color}"></span>${esc(s.name)}</button>`).join("");
  lg.querySelectorAll("button").forEach(b => b.onclick = () => { const i = +b.dataset.i; hidden.has(i) ? hidden.delete(i) : hidden.add(i); renderCharts(run.k); });
  const mk = key => sims.map((s, i) => ({name: s.name, short: s.name.replace(/\s*\(.*\)/, ""), x: s.r.t.slice(0, k + 1), y: s.r[key].slice(0, k + 1), color: s.color, dash: s.dash, hidden: hidden.has(i)}));
  const maxAll = key => Math.max(...sims.map(s => Math.max(...s.r[key])));
  const specs = [
    {title: "Salud del parque (índice 0–1)", key: "salud", ymin: 0, ymax: 1, yfmt: v => fnum(v, 2)},
    {title: "Disponibilidad (% de equipos operativos)", key: "disp", ymin: 0, ymax: 100, yfmt: v => fnum(v, 0)},
    {title: "Inactividad (% de equipos fuera de servicio)", key: "inact", ymin: 0, ymax: maxAll("inact"), yfmt: (v, t) => fnum(v, t ? 1 : 0)},
    {title: "Costo total acumulado (miles de USD)", key: "total", ymin: 0, ymax: maxAll("total"), yfmt: (v, t) => t ? fnum(v, 0) + " k" : fnum(v, 0)},
  ];
  const host = $("charts"); host.innerHTML = "";
  specs.forEach(sp => {
    const d = document.createElement("div"); d.className = "chart"; host.appendChild(d);
    drawChart(d, {title: sp.title, series: mk(sp.key), ymin: sp.ymin, ymax: sp.ymax, yfmt: sp.yfmt, xlabel: "Mes", xname: "Mes", xmax: state.horizonte});
  });
}

function renderSweep(){
  const marks = [{x: sweep.best.iv, y: sweep.best.cost, color: "#c0503a", r: 5.5, label: `mín. ${fnum(sweep.best.iv, sweep.best.iv % 1 ? 1 : 0)} m`}];
  sims.forEach(s => {
    if (s.iv >= 1 && s.iv <= 24){
      const i = sweep.xs.findIndex(x => Math.abs(x - s.iv) < 1e-9);
      if (i >= 0 && Math.abs(s.iv - sweep.best.iv) > 0.01) marks.push({x: s.iv, y: sweep.ys[i], color: s.color, r: 4});
    }
  });
  drawChart($("sweep"), {title: `Costo total a ${state.horizonte} meses según el intervalo entre MP`, series: [{name: "Costo total", x: sweep.xs, y: sweep.ys, color: "#2b5fa8"}],
    marks, yfmt: (v, t) => t ? fnum(v, 0) + " k USD" : fnum(v, 0), xlabel: "Intervalo entre intervenciones de MP (meses)", xname: "Cada", ymin: 0});
  $("sweepNote").textContent = "Punto rojo: intervalo de costo mínimo. Puntos de colores: los escenarios fijos y el personalizado. Los intervalos largos son mucho más caros que los cortos.";
}

function renderPrintParams(){
  const rows = DEFS.map(d => `<tr><td>${esc(d.label)}</td><td>${state[d.k]} ${esc(d.unit)}</td><td>${state[d.k] !== d.def ? "modificado (base " + d.def + ")" : "base"}</td></tr>`);
  rows.push(`<tr><td>Método numérico</td><td>${esc(METODOS[state.metodo].nombre)}</td><td>${state.metodo !== NUM_DEF.metodo ? "modificado" : "base"}</td></tr>`);
  rows.push(`<tr><td>Paso de tiempo (dt)</td><td>${state.dt} meses</td><td>${state.dt !== NUM_DEF.dt ? "modificado (base " + NUM_DEF.dt + ")" : "base"}</td></tr>`);
  $("printParams").innerHTML = `<table><thead><tr><th>Parámetro</th><th>Valor</th><th>Estado</th></tr></thead><tbody>${rows.join("")}</tbody></table>`;
  $("printMeta").innerHTML = `<b>Reporte de simulación</b> · generado el ${new Date().toLocaleString("es-CO")}`;
}


function limpiarResultados(msg){
  $("kpiTitle").textContent = "Indicadores";
  $("kpi").innerHTML = `<p class="note">${msg}</p>`;
  $("lectura").innerHTML = "";
  $("sweep").innerHTML = ""; $("sweepNote").textContent = "";
  $("charts").innerHTML = ""; $("legend").innerHTML = "";
  $("prompt").value = "";
}

function setRun(msg, err){ const s = $("runStatus"); s.textContent = msg; s.className = "status" + (err ? " err" : ""); }

function updateButtons(){
  const e = run.estado;
  $("btnStart").disabled = e === "running" || e === "paused";
  $("btnPause").disabled = !(e === "running" || e === "paused");
  $("btnPause").textContent = e === "paused" ? "Continuar" : "Pausar";
  $("btnStop").disabled = e === "idle";
  $("btnStart").textContent = e === "done" ? "Simular de nuevo" : "Iniciar simulación";
}

function iniciar(){
  cancelAnimationFrame(run.raf);
  compute();
  run.estado = "running"; run.k = 0; run.kf = 0; run.last = 0; run.n = sims[0].r.t.length;
  run.firma = firma();
  interpretacion = null; renderOut();
  limpiarResultados("Los indicadores aparecen cuando termina la simulación.");
  updateButtons(); renderCharts(0); $("bar").style.width = "0%";
  setRun(`Simulando con ${METODOS[state.metodo].nombre}, dt = ${state.dt} mes…`);
  run.raf = requestAnimationFrame(frame);
}

function frame(ts){
  if (run.estado !== "running") return;
  if (!run.last) run.last = ts;
  const dtReal = Math.min(0.1, (ts - run.last) / 1000); run.last = ts;
  run.kf += (+$("speed").value / state.dt) * dtReal;
  const k = Math.min(run.n - 1, Math.floor(run.kf));
  if (k !== run.k){
    run.k = k; renderCharts(k);
    $("bar").style.width = (100 * k / (run.n - 1)) + "%";
    setRun(`Mes ${fnum(sims[0].r.t[k], 1)} de ${state.horizonte}`);
  }
  if (k >= run.n - 1) return terminar();
  run.raf = requestAnimationFrame(frame);
}

function terminar(){
  run.estado = "done"; updateButtons();
  renderKPI(); renderSweep(); renderPrintParams();
  $("prompt").value = buildPrompt(); renderOut();
  setRun(`Simulación terminada (${state.horizonte} meses).`);
}

function pausar(){
  if (run.estado === "running"){ run.estado = "paused"; setRun("En pausa."); }
  else if (run.estado === "paused"){ run.estado = "running"; run.last = 0; setRun("Continuando…"); run.raf = requestAnimationFrame(frame); }
  updateButtons();
}

function detener(){
  cancelAnimationFrame(run.raf);
  run.estado = "idle"; run.k = 0; sims = []; interpretacion = null; renderOut();
  limpiarResultados("Pulsa «Iniciar simulación» para ver los resultados.");
  $("bar").style.width = "0%"; updateButtons();
  setRun("Ajusta los parámetros y pulsa «Iniciar simulación».");
}

/* Cambiar parámetros no recalcula solo: hay que pulsar Iniciar. */
function schedule(){
  renderPrintParams();
  if (run.estado !== "idle") setRun("Cambiaste parámetros: pulsa «Simular de nuevo» (o «Reiniciar») para usar los nuevos valores.", true);
  $("subtitle").textContent = `Dinámica de sistemas (niveles y flujos de Forrester) · método: ${METODOS[state.metodo].nombre} · paso ${state.dt} mes`;
}

/* ---------- Controles ---------- */
function buildControls(){
  const host = $("controls"); host.innerHTML = "<h2>Parámetros</h2>";
  [...new Set(DEFS.map(d => d.g))].forEach(g => {
    const box = document.createElement("details"); box.open = true;
    box.innerHTML = `<summary>${esc(g)}</summary>`;
    DEFS.filter(d => d.g === g).forEach(d => {
      const row = document.createElement("div"); row.className = "ctl"; row.id = "c_" + d.k;
      row.innerHTML = `<label for="n_${d.k}"><span>${esc(d.label)}</span><span class="unit">${esc(d.unit)}</span></label>
        <div class="inputs"><input type="range" id="r_${d.k}" min="${d.min}" max="${d.max}" step="${d.step}" value="${state[d.k]}" aria-label="${esc(d.label)}">
        <input type="number" id="n_${d.k}" min="${d.min}" max="${d.max}" step="${d.step}" value="${state[d.k]}"></div><small>${esc(d.tip)}</small>`;
      box.appendChild(row);
      const r = row.querySelector("input[type=range]"), n = row.querySelector("input[type=number]");
      const set = v => {
        v = Math.min(d.max, Math.max(d.min, v)); if (isNaN(v)) return;
        state[d.k] = v; r.value = v; if (document.activeElement !== n) n.value = v;
        row.classList.toggle("changed", v !== d.def); schedule();
      };
      r.addEventListener("input", () => set(parseFloat(r.value)));
      n.addEventListener("input", () => { const v = parseFloat(n.value); if (!isNaN(v)) set(v); });
      n.addEventListener("blur", () => { n.value = state[d.k]; });
    });
    host.appendChild(box);
  });

  /* Método numérico */
  const nb = document.createElement("details"); nb.open = true;
  nb.innerHTML = `<summary>Método numérico</summary>
    <div class="ctl"><label for="s_metodo"><span>Método de integración</span></label>
      <select id="s_metodo">${Object.entries(METODOS).map(([k, m]) => `<option value="${k}">${esc(m.nombre)}</option>`).join("")}</select>
      <small>Euler: y(t+dt) = y(t) + dt·f(y). RK4 sirve para comprobar que Euler no está distorsionando los resultados.</small></div>
    <div class="ctl"><label for="s_dt"><span>Paso de tiempo (dt)</span><span class="unit">meses</span></label>
      <select id="s_dt">${DT_OPCIONES.map(v => `<option value="${v}">${v}</option>`).join("")}</select>
      <small>Un dt menor da más precisión con Euler, pero más cálculo.</small></div>`;
  host.appendChild(nb);
  $("s_metodo").value = state.metodo; $("s_dt").value = state.dt;
  $("s_metodo").onchange = e => { state.metodo = e.target.value; schedule(); };
  $("s_dt").onchange = e => { state.dt = parseFloat(e.target.value); schedule(); };
}

function resetAll(){
  DEFS.forEach(d => state[d.k] = d.def);
  Object.assign(state, NUM_DEF);
  hidden.clear(); buildControls(); detener(); schedule();
}

function descargarPDF(){
  const t = document.title;
  document.title = "reporte_simulacion_mantenimiento";
  renderPrintParams();
  setTimeout(() => { window.print(); document.title = t; }, 50);
}

/* ---------- Inicio ---------- */
function init(){
  buildControls();
  $("btnReset").onclick = resetAll;
  $("btnStart").onclick = iniciar;
  $("btnPause").onclick = pausar;
  $("btnStop").onclick = detener;
  $("btnPdf").onclick = descargarPDF;
  $("btnIA").onclick = interpretar;
  $("btnCopy").onclick = copiarPrompt;
  const prov = $("prov"), model = $("model"); let tocado = false;
  model.value = DEFAULT_MODEL.anthropic;
  model.addEventListener("input", () => tocado = true);
  prov.addEventListener("change", () => {
    $("baseWrap").style.display = prov.value === "custom" ? "block" : "none";
    if (!tocado) model.value = DEFAULT_MODEL[prov.value];
  });
  try {
    const k = localStorage.getItem("sim_mant_key");
    if (k){ $("key").value = k; $("remember").checked = true; }
    $("remember").addEventListener("change", e => { e.target.checked ? localStorage.setItem("sim_mant_key", $("key").value) : localStorage.removeItem("sim_mant_key"); });
    $("key").addEventListener("input", () => { if ($("remember").checked) localStorage.setItem("sim_mant_key", $("key").value); });
  } catch (_) { $("remember").disabled = true; }
  window.addEventListener("beforeprint", renderPrintParams);
  detener(); schedule();
}
init();
