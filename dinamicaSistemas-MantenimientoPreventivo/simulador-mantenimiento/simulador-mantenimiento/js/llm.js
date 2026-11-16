"use strict";
/* Interpretación con un modelo de lenguaje (Anthropic, OpenRouter o compatible con OpenAI). */
const DEFAULT_MODEL = {anthropic: "claude-sonnet-5-5", openrouter: "anthropic/claude-sonnet-4.5", custom: ""};

function mdToHtml(t){
  const lines = esc(t).split(/\r?\n/); let html = "", inList = false;
  const inline = s => s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  lines.forEach(l => {
    const li = l.match(/^\s*[-*•]\s+(.*)/), hd = l.match(/^#{1,4}\s+(.*)/);
    if (li){ if (!inList){ html += "<ul>"; inList = true; } html += `<li>${inline(li[1])}</li>`; return; }
    if (inList){ html += "</ul>"; inList = false; }
    if (hd) html += `<h4>${inline(hd[1])}</h4>`;
    else if (l.trim()) html += `<p>${inline(l)}</p>`;
  });
  return html + (inList ? "</ul>" : "");
}

function firma(){ return JSON.stringify(state); }

function buildPrompt(){
  const T = state.horizonte, met = METODOS[state.metodo].nombre;
  const params = DEFS.map(d => `- ${d.label}: ${state[d.k]} ${d.unit}${state[d.k] !== d.def ? ` (valor base: ${d.def})` : ""}`).join("\n");
  const res = sims.map(s => `- ${s.name}: salud final ${fnum(s.r.saludFinal, 2)}; disponibilidad media ${fnum(s.r.dispMedia)} %; inactividad media ${fnum(s.r.inactMedia)} %; meses con taller saturado ${fnum(s.r.sat)}/${T}; costo mantenimiento USD ${fk(s.r.costoMant)}; costo inactividad USD ${fk(s.r.costoInact)}; costo total USD ${fk(s.r.costoTotal)}`).join("\n");
  return `Eres analista de dinámica de sistemas. Interpreta los resultados de este modelo para un informe académico, en español, sin inventar datos.

MODELO (Forrester, método ${met}, paso ${state.dt} mes, ${T} meses). Niveles: equipos operativos, equipos en falla, salud del parque (0–1), costo acumulado de mantenimiento y de inactividad. Flujos: fallas = operativos × tasa de fallas (que crece al bajar la salud); reparación = mín(en falla / tiempo de reparación, capacidad del taller); degradación (aumenta con la fracción de equipos parados); recuperación por MP = (1 − salud) × efectividad × frecuencia de MP con retraso de primer orden. Bucles: R1 círculo vicioso de degradación (menos salud → más fallas → más equipos parados → más degradación); B1 efecto del MP (recupera la brecha de salud, con rendimientos decrecientes); B2 reparación, que se satura cuando las fallas superan la capacidad del taller.

PARÁMETROS (supuestos, no datos reales):
${params}

RESULTADOS:
${res}

Intervalo de MP de costo total mínimo en el barrido de 1 a 24 meses: cada ${fnum(sweep.best.iv, sweep.best.iv % 1 ? 1 : 0)} meses (USD ${fnum(sweep.best.cost, 0)} k).

Responde con estas secciones breves (máximo 400 palabras en total): 1) Lectura general. 2) Qué explica cada escenario en términos de los bucles R1, B1 y B2 (menciona la saturación del taller si ocurre). 3) Sensibilidad: qué parámetros de los usados pesan más en este caso y por qué. 4) Recomendación sobre la frecuencia de MP. 5) Limitaciones (parámetros supuestos, sin datos reales).`;
}

function renderOut(){
  const o = $("out");
  $("iaCard").classList.toggle("empty", !interpretacion);
  if (!interpretacion){ o.style.display = "none"; o.innerHTML = ""; return; }
  const vieja = interpretacion.firma !== firma();
  o.style.display = "block";
  o.innerHTML = `<h3 style="margin-top:0">Interpretación (${esc(interpretacion.fecha)}) ${vieja ? '<span class="stale noprint">desactualizada: cambiaste parámetros después de generarla</span>' : ""}</h3>` + mdToHtml(interpretacion.texto) +
    `<p class="note">Texto generado por un modelo de lenguaje a partir de los resultados de este simulador; revísalo antes de usarlo.</p>`;
}

function setStatus(msg, err){ const s = $("status"); s.textContent = msg; s.className = "status" + (err ? " err" : ""); }

async function interpretar(){
  if (run.estado !== "done"){ setStatus("Primero ejecuta la simulación hasta el final.", true); return; }
  const key = $("key").value.trim(), prov = $("prov").value, model = $("model").value.trim();
  if (!key){ setStatus("Falta la API key.", true); return; }
  if (!model){ setStatus("Falta el nombre del modelo.", true); return; }
  const prompt = buildPrompt(), sys = "Eres un analista experto en dinámica de sistemas. Responde en español, con precisión y sin inventar cifras.";
  const btn = $("btnIA"); btn.disabled = true; setStatus("Consultando al modelo…");
  try {
    let url, headers, body, extract;
    if (prov === "anthropic"){
      url = "https://api.anthropic.com/v1/messages";
      headers = {"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01", "anthropic-dangerous-direct-browser-access": "true"};
      body = {model, max_tokens: 1800, system: sys, messages: [{role: "user", content: prompt}]};
      extract = d => (d.content || []).filter(b => b.type === "text").map(b => b.text).join("\n");
    } else {
      const base = prov === "openrouter" ? "https://openrouter.ai/api/v1" : $("base").value.trim().replace(/\/+$/, "");
      if (!base){ setStatus("Falta la URL base.", true); btn.disabled = false; return; }
      url = base + "/chat/completions";
      headers = {"content-type": "application/json", "authorization": "Bearer " + key};
      body = {model, max_tokens: 1800, messages: [{role: "system", content: sys}, {role: "user", content: prompt}]};
      extract = d => d.choices && d.choices[0] && d.choices[0].message ? d.choices[0].message.content : "";
    }
    const res = await fetch(url, {method: "POST", headers, body: JSON.stringify(body)});
    const data = await res.json().catch(() => ({}));
    if (!res.ok){
      const msg = (data.error && (data.error.message || data.error)) || data.message || ("HTTP " + res.status);
      throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
    }
    const texto = extract(data);
    if (!texto) throw new Error("La respuesta no trajo texto.");
    interpretacion = {texto, firma: firma(), fecha: new Date().toLocaleString("es-CO")};
    renderOut(); setStatus("Listo. Si descargas el PDF ahora, la interpretación se incluye.");
  } catch (e){
    const extra = e instanceof TypeError ? " (no se pudo conectar: revisa tu conexión, la URL, o que el navegador no esté bloqueando la petición)" : "";
    setStatus("Error: " + e.message + extra, true);
  } finally { btn.disabled = false; }
}

function copiarPrompt(){
  const ta = $("prompt"), done = () => setStatus("Prompt copiado. Pégalo en el chat del modelo que prefieras.");
  const fallback = () => { ta.parentElement.open = true; ta.select(); try { document.execCommand("copy"); done(); } catch (_) { setStatus("Selecciona el texto del prompt y cópialo manualmente.", true); } };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(ta.value).then(done, fallback); else fallback();
}
