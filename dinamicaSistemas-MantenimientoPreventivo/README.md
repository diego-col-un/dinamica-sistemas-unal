# Dinámica de Sistemas: Gestión de Mantenimiento Preventivo vs. Correctivo en un Parque Tecnológico

[![Universidad Nacional de Colombia](https://img.shields.io/badge/Universidad-Nacional%20de%20Colombia-003366?style=for-the-badge)](https://unal.edu.co/)
[![Asignatura](https://img.shields.io/badge/Curso-Din%C3%A1mica%20de%20Sistemas-17b978?style=for-the-badge)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Vensim](https://img.shields.io/badge/Model-Vensim%20.mdl-orange?style=for-the-badge)](#)
[![Web App](https://img.shields.io/badge/Simulador-HTML5%20%7C%20JS-yellow?style=for-the-badge)](#)

> **Proyecto Académico de Dinámica de Sistemas**  
> **Autores:** Diego Aristizábal & Ana María Suárez  
> **Fecha:** Noviembre de 2026

---

## 📌 Descripción del Proyecto

Este proyecto aborda la modelación y simulación de un parque tecnológico compuesto por **100 equipos computacionales y de telecomunicaciones** a lo largo de un horizonte temporal de **60 meses (5 años)**. A través de los principios de **Dinámica de Sistemas (escuela de Jay Forrester)**, se evalúa el compromiso (*trade-off*) entre el costo directo de realizar **Mantenimiento Preventivo (MP)** programado y las pérdidas económicas asociadas a averías imprevistas (**Mantenimiento Correctivo - MC**) y al lucro cesante (**Costo de Inactividad**).

El modelo demuestra cuantitativamente cómo la falta de mantenimiento activa un **círculo vicioso de sobrecarga y degradación** que satura la capacidad del taller de reparaciones, provocando el colapso operativo del parque.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ECOSISTEMA DEL PROYECTO                                │
├─────────────────────────┬──────────────────────────┬────────────────────────────┤
│ 📐 Modelo Vensim        │ 🐍 Scripts de Simulación │ 💻 Simulador Web           │
│    documento.mdl        │    scripts/              │    simulador-mantenimiento │
│ • 5 Niveles / Stocks    │ • Solucionador Euler     │ • Animación paso a paso    │
│ • Retardo DELAY1I       │ • Análisis de Tornado    │ • Gráficas interactivas    │
│ • Euler (dt = 0.25 m)   │ • Barrido de óptimo      │ • Integración con LLMs     │
│ • 4 Escenarios          │ • Reportes en PDF        │ • Exportación de datos     │
└─────────────────────────┴──────────────────────────┴────────────────────────────┘
```

---

## 🎯 Pregunta de Investigación e Hipótesis Dinámica

- **Pregunta Central:** ¿Con qué periodicidad e intensidad conviene intervenir preventivamente un parque de equipos tecnológicos para maximizar la disponibilidad y minimizar el costo acumulado total de ciclo de vida?
- **Hipótesis Dinámica:**
  1. La política **"Sin MP"** genera una espiral desestabilizadora: al bajar la salud del parque, la tasa de fallas sube hasta exceder la capacidad del taller ($C_{\text{taller}} = 4$ equipos/mes), desatando un colapso por saturación.
  2. El MP introduce un **bucle estabilizador** que recupera salud, pero con **rendimientos marginales decrecientes** (conforme la salud se acerca al 100%, cada intervención aporta menos confiabilidad adicional).
  3. En consecuencia, la curva de costo total respecto al intervalo de MP es **estrictamente convexa**, existiendo un intervalo óptimo intermedio (alrededor de 6 meses) que minimiza los costos totales.

---

## 🔄 Estructura de Bucles de Realimentación (Feedback Loops)

El sistema está gobernado por tres bucles principales interconectados:

1. **R1 — Círculo Vicioso de Degradación (Reforzador / Bola de nieve):**  
   $$\text{Salud } \downarrow \;\longrightarrow\; \text{Tasa de Fallas } \uparrow \;\longrightarrow\; \text{Equipos en Falla } \uparrow \;\longrightarrow\; \text{Sobrecarga Operativa } \uparrow \;\longrightarrow\; \text{Degradación } \uparrow \;\longrightarrow\; \text{Salud } \downarrow$$
   *Es el bucle destructivo responsable del colapso en ausencia de mantenimiento preventivo.*

2. **B1 — Efecto del Mantenimiento Preventivo (Balanceador / Estabilizador):**  
   $$\text{Salud } \downarrow \;\longrightarrow\; \text{Brecha } (1 - \text{Salud}) \uparrow \;\longrightarrow\; \text{Recuperación por MP } \uparrow \;\longrightarrow\; \text{Salud } \uparrow$$
   *Frena el deterioro del hardware con rendimientos decrecientes y un retardo de información de 3 meses.*

3. **B2 — Taller de Reparación (Balanceador con Saturación no lineal):**  
   $$\text{Equipos en Falla } \uparrow \;\longrightarrow\; \text{Reparaciones Requeridas } \uparrow \;\longrightarrow\; \text{Equipos en Falla } \downarrow$$
   *Posee un límite físico estricto de capacidad ($C_{\text{taller}} = 4.0$ equipos/mes). Si la demanda supera dicho tope, B2 se desactiva y el bucle R1 toma el control absoluto del parque.*

---

## 📐 Formulación Matemática y Ecuaciones de Balance

El sistema continuo se modela mediante el vector de estado $\vec{y}(t) = [O, F, S, C_m, C_i, MP_e]^T \in \mathbb{R}^6$:

### Ecuaciones de Nivel (Stocks / Balance)
- **Equipos Operativos ($O$):**
  $$\frac{dO(t)}{dt} = R(t) - F_{\text{flujo}}(t), \quad O(0) = 96 \text{ equipos}$$
- **Equipos en Falla ($F$):**
  $$\frac{dF(t)}{dt} = F_{\text{flujo}}(t) - R(t), \quad F(0) = 4 \text{ equipos}$$
  *(Ley de Conservación: $\frac{d(O+F)}{dt} = 0 \implies O(t) + F(t) = 100 \text{ equipos (constante)} $)*
- **Salud del Parque ($S$):**
  $$\frac{dS(t)}{dt} = \text{Rec}_{\text{MP}}(t) - \text{Deg}(t), \quad S(0) = 0.85 \quad [\text{adimensional } 0-1]$$
- **Costo Acumulado de Mantenimiento ($C_m$):**
  $$\frac{dC_m(t)}{dt} = c_{\text{mp}}(t) + c_{\text{mc}}(t), \quad C_m(0) = 0 \text{ USD}$$
- **Costo Acumulado de Inactividad ($C_i$):**
  $$\frac{dC_i(t)}{dt} = c_{\text{inact}}(t), \quad C_i(0) = 0 \text{ USD}$$
- **Nivel de Retardo de Política ($MP_e$):**
  $$\frac{d(MP_e(t))}{dt} = \frac{f_{\text{mp}} - MP_e(t)}{\tau_{\text{mp}}}, \quad MP_e(0) = 0 \text{ mes}^{-1}, \quad \tau_{\text{mp}} = 3.0 \text{ meses}$$

### Ecuaciones de Flujo (Rates)
- **Fallas:** $F_{\text{flujo}}(t) = O(t) \cdot \lambda(S(t))$ con $\lambda(S) = 0.02 \cdot [1 + 4 \cdot (1 - S(t))]$
- **Reparación:** $R(t) = \min\left( \frac{F(t)}{1.5}, \; 4.0 \right)$ *(Función no lineal de cuello de botella)*
- **Degradación:** $\text{Deg}(t) = S(t) \cdot 0.025 \cdot \left[ 1 + 2.0 \cdot \frac{F(t)}{100} \right]$
- **Recuperación por MP:** $\text{Rec}_{\text{MP}}(t) = (1 - S(t)) \cdot 0.6 \cdot MP_e(t)$
- **Flujos de Costo:**
  - Preventivo: $c_{\text{mp}}(t) = f_{\text{mp}} \cdot O(t) \cdot 120 \text{ USD/mes}$
  - Correctivo: $c_{\text{mc}}(t) = R(t) \cdot 900 \text{ USD/mes}$
  - Inactividad: $c_{\text{inact}}(t) = F(t) \cdot 600 \text{ USD/mes}$

---

## 📊 Comparación de Políticas y Resultados Clave

Simulación numérica a **60 meses** con paso de integración de Euler $\Delta t = 0.25$ meses:

| Escenario de Política | Intervalo MP | Salud Final | Disponibilidad Media | Inactividad Media | Costo Total (60 meses) | Diagnóstico Dinámico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Sin MP** | 0 m | 0.30 | 56.8 % | 43.2 % | **USD 1,607,000** | **Catastrófico:** Taller saturado 52 meses; inactividad representa el 77% del costo. |
| **2. MP Baja** | 12 m | 0.48 | 66.1 % | 33.9 % | **USD 1,440,000** | **Insuficiente:** No evita la saturación prolongada del taller (48 meses). |
| **3. MP Intermedia** | **6 m** | **0.83** | **94.1 %** | **5.9 %** | **USD 445,000** | **ÓPTIMO GLOBAL:** Evita la saturación; **ahorra un 72% de costo** frente a Sin MP. |
| **4. MP Intensiva** | 3 m | 0.90 | 96.7 % | 3.3 % | **USD 475,000** | **Sobregasto:** Gana apenas 2.6% de disponibilidad pero cuesta USD 30k más. |

### Hallazgo de Asimetría del Riesgo
- Equivocarse por **exceso de mantenimiento** (cada 3 meses) incrementa el costo total solo un **+10%** respecto al óptimo.
- Equivocarse por **defecto de mantenimiento** (cada 12 meses) dispara el costo un **+223%** debido al colapso del taller.
> *En sistemas de mantenimiento con capacidad acotada, equivocarse por exceso de prevención es un orden de magnitud más seguro y económico que equivocarse por defecto.*

---

## 📁 Estructura del Repositorio

```text
dinamicaSistemas-MantenimientoPreventivo/
├── documento.mdl                    # Modelo canónico de Forrester en Vensim (UTF-8)
├── reporte_analisis.pdf             # Reporte ejecutivo global del análisis y conclusiones
├── README.md                        # Documentación principal del repositorio
│
├── diagramas/                       # Recursos gráficos y salidas visuales
│   ├── diagrama_causal.png          # Diagrama de bucles causales (R1, B1, B2)
│   ├── diagrama_forrester.png       # Diagrama de niveles y flujos de Forrester
│   ├── resultados_trayectorias.png  # Trayectorias comparativas de las 4 políticas
│   ├── resultados_costos.png        # Composición de costos acumulados por escenario
│   ├── resultados_sensibilidad.png  # Diagrama de tornado de parámetros críticos
│   └── resultados_intervalo_optimo.png # Curva de convexidad y barrido óptimo
│
├── formulacionMatematica/           # Paquete formal de deducción matemática y balances
│   ├── Formulacion_Matematica_Dinamica_Sistemas.pdf  # PDF formal con balances y matrices
│   ├── Explicacion_Detallada_Formulacion_Matematica.pdf # PDF pedagógico y de estabilidad
│   ├── README.md                    # Fuente Markdown con fórmulas en LaTeX
│   └── EXPLICACION_FORMULACION.md   # Guía explicativa conceptual en Markdown
│
├── referencias/                     # Declaración ética de IA y bibliografía IEEE
│   └── README.md                    # Agradecimientos (Claude & Gemini) y fuentes [1]-[7]
│
├── scripts/                         # Suite computacional en Python
│   ├── modelo_mantenimiento.py      # Motor de simulación matemática (NumPy / Euler)
│   ├── analisis.py                  # Barrido de intervalos, tornado y validaciones
│   ├── diagramas.py                 # Generador programático de diagramas en Matplotlib
│   ├── reporte.py                   # Generador del informe ejecutivo PDF (ReportLab)
│   ├── generar_pdf_formulacion.py   # Compilador del PDF de formulación matemática
│   ├── generar_pdf_explicacion.py   # Compilador del PDF de la guía explicativa
│   └── resultados.json              # Datos numéricos serializados de las simulaciones
│
└── simulador-mantenimiento/         # Aplicación web interactiva frontend
    └── simulador-mantenimiento/
        ├── index.html               # Interfaz de usuario interactiva
        ├── css/styles.css           # Estilos responsivos y modo de impresión
        └── js/
            ├── app.js               # Controlador de interfaz y eventos
            ├── simulation.js        # Motor de dinámica de sistemas en JavaScript
            ├── params.js            # Parámetros y escenarios por defecto
            ├── charts.js            # Renderizador gráfico SVG/Canvas
            ├── llm.js               # Conector para diagnósticos con IA (OpenAI/Anthropic)
            └── utils.js             # Formateadores numéricos y utilidades
```

---

## 🚀 Instrucciones de Ejecución

### 1. Entorno de Simulación en Python
Asegúrate de contar con Python 3.10 o superior y las dependencias requeridas:
```bash
pip install numpy matplotlib reportlab pillow pypdf
```

Para correr las simulaciones, actualizar análisis y recompilar todos los documentos:
```bash
# 1. Ejecutar simulación base por consola
python scripts/modelo_mantenimiento.py

# 2. Generar curvas de análisis, sensibilidad y barrido de óptimo
python scripts/analisis.py

# 3. Dibujar diagramas causal y de Forrester
python scripts/diagramas.py

# 4. Compilar reportes y documentos en PDF
python scripts/reporte.py
python scripts/generar_pdf_formulacion.py
python scripts/generar_pdf_explicacion.py
```

### 2. Simulador Web Interactivo
No requiere instalación de servidores ni paquetes de Node.js:
1. Navega a `simulador-mantenimiento/simulador-mantenimiento/`.
2. Abre el archivo `index.html` en cualquier navegador web moderno (Chrome, Edge, Firefox, Safari).
3. Utiliza los controles deslizantes para modificar parámetros en tiempo real, visualizar la simulación paso a paso o solicitar diagnósticos contextuales mediante la integración LLM.

### 3. Modelo Vensim
Abre el archivo `documento.mdl` directamente en **Vensim PLE / DSS** para inspeccionar la formulación visual, ejecutar simulaciones con la herramienta `SyntheSim` o exportar conjuntos de datos `.vdfx`.

---

## 👥 Autores y Créditos

Este trabajo fue desarrollado para la asignatura de **Dinámica de Sistemas** en la **Universidad Nacional de Colombia**:

- **Diego Aristizábal**
- **Ana María Suárez**

*Noviembre de 2026.*

---

## 🤝 Agradecimientos (Acknowledgment)

En estricto cumplimiento de los lineamientos del **IEEE** (*IEEE Author Guidelines for Artificial Intelligence (AI)-Generated Text*), los autores declaran formalmente el uso asistido de herramientas de Inteligencia Artificial Generativa:

- **Claude (Anthropic):** Utilizado en la conceptualización de diagramas causales de realimentación, estructuración del modelo en Vensim (`documento.mdl`) y apoyo en la arquitectura modular del simulador web.
- **Gemini (Google DeepMind):** Utilizado en la formulación analítica de ecuaciones de balance, verificación de consistencia dimensional, cálculo formal del criterio de estabilidad numérica de Euler ($\Delta t \le \tau_{\min}/2$) y desarrollo de scripts de análisis y reportes en Python con ReportLab.

Los autores revisaron, validaron y asumen plena responsabilidad por el contenido, resultados y conclusiones presentadas en este trabajo.

---

## 📚 Referencias (References)

Formato estándar **IEEE**:

```text
[1] J. D. Sterman, Business Dynamics: Systems Thinking and Modeling for a Complex World. Boston, MA, USA: Irwin/McGraw-Hill, 2000.

[2] J. W. Forrester, Industrial Dynamics. Cambridge, MA, USA: The MIT Press, 1961.

[3] J. W. Forrester, Principles of Systems, 2nd ed. Cambridge, MA, USA: Wright-Allen Press, 1968.

[4] A. K. S. Jardine and A. H. C. Tsang, Maintenance, Replacement, and Reliability: Theory and Applications, 2nd ed. Boca Raton, FL, USA: CRC Press, 2013.

[5] B. S. Blanchard, D. Verma, and E. L. Peterson, Maintainability: A Key to Effective Serviceability and Maintenance Management. New York, NY, USA: John Wiley & Sons, 1995.

[6] Ventana Systems, Vensim Modeling Guide: Version 10. Harvard, MA, USA: Ventana Systems, Inc., 2023. [Online]. Available: https://vensim.com/documentation/

[7] IEEE, "IEEE Author Guidelines for Artificial Intelligence (AI)-Generated Text," IEEE Author Center, 2023. [Online]. Available: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
```
