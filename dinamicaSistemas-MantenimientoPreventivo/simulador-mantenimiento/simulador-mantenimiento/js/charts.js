"use strict";
/* Gráficas SVG sin librerías. */
function drawChart(el, cfg){
  const W = 600, H = 290, m = {l:58, r:16, t:34, b:40};
  const vis = cfg.series.filter(s => !s.hidden);
  const x0 = cfg.series[0].x[0], x1 = cfg.xmax !== undefined ? cfg.xmax : cfg.series[0].x[cfg.series[0].x.length - 1];
  let lo = cfg.ymin, hi = cfg.ymax;
  if (lo === undefined || hi === undefined){
    let a = Infinity, b = -Infinity;
    vis.forEach(s => s.y.forEach(v => { if (v < a) a = v; if (v > b) b = v; }));
    if (!isFinite(a)){ a = 0; b = 1; }
    if (lo === undefined) lo = Math.min(0, a);
    if (hi === undefined) hi = b;
  }
  const yt = niceTicks(lo, hi, 5); lo = yt[0]; hi = yt[yt.length - 1];
  const xt = niceTicks(x0, x1, 6).filter(v => v >= x0 - 1e-9 && v <= x1 + 1e-9);
  const sx = x => m.l + (x - x0) / (x1 - x0) * (W - m.l - m.r);
  const sy = y => H - m.b - (y - lo) / (hi - lo) * (H - m.t - m.b);
  let g = "";
  yt.forEach(v => { g += `<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${sy(v)}" y2="${sy(v)}"/><text x="${m.l-6}" y="${sy(v)+4}" text-anchor="end">${cfg.yfmt(v)}</text>`; });
  xt.forEach(v => { g += `<text x="${sx(v)}" y="${H-m.b+16}" text-anchor="middle">${v}</text>`; });
  g += `<line class="axis" x1="${m.l}" x2="${W-m.r}" y1="${H-m.b}" y2="${H-m.b}"/><line class="axis" x1="${m.l}" x2="${m.l}" y1="${m.t}" y2="${H-m.b}"/>`;
  g += `<text x="${(m.l+W-m.r)/2}" y="${H-6}" text-anchor="middle">${esc(cfg.xlabel)}</text>`;
  g += `<text class="ttl" x="${m.l}" y="18">${esc(cfg.title)}</text>`;
  vis.forEach(s => {
    const d = s.x.map((x, i) => (i ? "L" : "M") + sx(x).toFixed(1) + "," + sy(s.y[i]).toFixed(1)).join("");
    g += `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="2.2" ${s.dash ? 'stroke-dasharray="6 4"' : ""} stroke-linejoin="round"/>`;
  });
  (cfg.marks || []).forEach(mk => {
    g += `<circle cx="${sx(mk.x)}" cy="${sy(mk.y)}" r="${mk.r || 4}" fill="${mk.color}" stroke="var(--card)" stroke-width="1.5"/>`;
    if (mk.label) g += `<text x="${sx(mk.x)}" y="${sy(mk.y)-9}" text-anchor="middle" style="fill:${mk.color};font-weight:600">${esc(mk.label)}</text>`;
  });
  g += `<line class="xh" x1="0" x2="0" y1="${m.t}" y2="${H-m.b}"/>`;
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(cfg.title)}">${g}</svg><div class="tip"></div>`;
  const svg = el.querySelector("svg"), xh = el.querySelector(".xh"), tip = el.querySelector(".tip");
  const base = cfg.series[0].x, len = base.length;
  svg.addEventListener("mousemove", e => {
    const r = svg.getBoundingClientRect();
    const fx = (e.clientX - r.left) / r.width * W;
    const xv = x0 + (fx - m.l) / (W - m.l - m.r) * (x1 - x0);
    const step = len > 1 ? base[1] - base[0] : 1;
    if (xv < x0 || xv > base[len - 1] + step / 2){ xh.style.display = tip.style.display = "none"; return; }
    const i = Math.max(0, Math.min(len - 1, Math.round((xv - x0) / step)));
    xh.setAttribute("x1", sx(base[i])); xh.setAttribute("x2", sx(base[i])); xh.style.display = "block";
    tip.innerHTML = `<b>${esc(cfg.xname)} ${fnum(base[i], base[i] % 1 ? 1 : 0)}</b>` +
      vis.map(s => `<div><span class="dot" style="background:${s.color};height:3px"></span>${esc(s.short || s.name)}: ${cfg.yfmt(s.y[i], true)}</div>`).join("");
    tip.style.display = "block";
    let left = e.clientX - el.getBoundingClientRect().left + 14;
    if (left + tip.offsetWidth > el.clientWidth) left -= tip.offsetWidth + 28;
    tip.style.left = Math.max(0, left) + "px"; tip.style.top = (e.clientY - el.getBoundingClientRect().top + 10) + "px";
  });
  svg.addEventListener("mouseleave", () => { xh.style.display = tip.style.display = "none"; });
}
