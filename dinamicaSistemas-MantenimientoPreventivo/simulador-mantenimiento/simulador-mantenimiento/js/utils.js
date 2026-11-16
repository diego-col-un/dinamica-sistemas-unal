"use strict";
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fk = v => (v/1000).toLocaleString("es-CO",{maximumFractionDigits:0}) + " k";
const fnum = (v,d=1) => v.toLocaleString("es-CO",{minimumFractionDigits:d,maximumFractionDigits:d});

function niceTicks(lo, hi, n){
  if (hi === lo){ hi = lo + 1; }
  const raw = (hi - lo) / n, mag = Math.pow(10, Math.floor(Math.log10(raw))), norm = raw / mag;
  const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
  const out = [];
  for (let v = Math.floor(lo/step)*step; v <= Math.ceil(hi/step)*step + step*1e-6; v += step) out.push(+v.toFixed(10));
  return out;
}
