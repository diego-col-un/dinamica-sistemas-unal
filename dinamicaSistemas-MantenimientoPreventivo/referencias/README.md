# Agradecimientos y Referencias Bibliográficas

> **Universidad Nacional de Colombia**  
> **Curso:** Dinámica de Sistemas  
> **Autores:** Diego Aristizábal & Ana María Suárez  
> **Fecha:** Noviembre de 2026  
> **Norma de Citación:** IEEE (*Institute of Electrical and Electronics Engineers*)

---

## Agradecimientos (Acknowledgment)

### Declaración de Uso de Herramientas de Inteligencia Artificial (IA)

En estricto cumplimiento de las directrices éticas y editoriales internacionales del IEEE (*IEEE Author Guidelines for Artificial Intelligence (AI)-Generated Text*), los autores declaran formalmente el uso asistido de sistemas de Inteligencia Artificial Generativa durante el desarrollo del proyecto:

1. **Sistemas de Inteligencia Artificial Utilizados:**
   - **Claude (Anthropic):** Empleado como asistente para la estructuración conceptual de los diagramas de bucles causales (identificación de polaridades en bucles reforzadores y balanceadores), sintaxis y funciones de control en Vensim (`documento.mdl`), y apoyo en la arquitectura modular de la interfaz interactiva web (`simulador-mantenimiento/`).
   - **Gemini (Google DeepMind):** Empleado como asistente para la deducción matemática analítica de las ecuaciones de balance de los niveles ($d\vec{y}/dt$), comprobación del teorema de conservación de flota, análisis de consistencia dimensional, cálculo formal del criterio de estabilidad numérica de Euler ($\Delta t \le \tau_{\min}/2$) y estructuración del pipeline de análisis y reportes técnicos en Python.

2. **Alcance y Justificación:**
   - Estas herramientas fueron utilizadas exclusivamente como aceleradores cognitivos y de programación, facilitando la exploración de código computacional (NumPy, ReportLab, Vanilla JavaScript), la diagramación y la redacción estructurada.

3. **Responsabilidad de los Autores:**
   - De acuerdo con la normativa de IEEE, la Inteligencia Artificial no reúne los criterios de coautoría. Los autores humanos (**Diego Aristizábal** y **Ana María Suárez**) revisaron, validaron, contrastaron matemáticamente y asumieron la responsabilidad plena e indelegable sobre la exactitud, originalidad, integridad, supuestos numéricos y conclusiones de este trabajo.

---

## Referencias (References)

Las siguientes fuentes bibliográficas tradicionales sustentan el marco teórico, metodológico y de modelado de este proyecto, presentadas en estricto formato estándar **IEEE**:

```text
[1] J. D. Sterman, Business Dynamics: Systems Thinking and Modeling for a Complex World. Boston, MA, USA: Irwin/McGraw-Hill, 2000.

[2] J. W. Forrester, Industrial Dynamics. Cambridge, MA, USA: The MIT Press, 1961.

[3] J. W. Forrester, Principles of Systems, 2nd ed. Cambridge, MA, USA: Wright-Allen Press, 1968.

[4] A. K. S. Jardine and A. H. C. Tsang, Maintenance, Replacement, and Reliability: Theory and Applications, 2nd ed. Boca Raton, FL, USA: CRC Press, 2013.

[5] B. S. Blanchard, D. Verma, and E. L. Peterson, Maintainability: A Key to Effective Serviceability and Maintenance Management. New York, NY, USA: John Wiley & Sons, 1995.

[6] Ventana Systems, Vensim Modeling Guide: Version 10. Harvard, MA, USA: Ventana Systems, Inc., 2023. [Online]. Available: https://vensim.com/documentation/

[7] IEEE, "IEEE Author Guidelines for Artificial Intelligence (AI)-Generated Text," IEEE Author Center, 2023. [Online]. Available: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
```

---

### Mapeo de Conceptos Teóricos a las Referencias

- **Dinámica de Realimentación y Bucles Causales:** El modelado de bucles reforzadores (R1) y de balance con retardos materiales y de información (B1 y B2) se fundamenta en los capítulos 5 y 6 de Sterman **[1]** y en los principios originarios de Forrester **[2]**, **[3]**.
- **Modelado de Desgaste y Confiabilidad:** La función de degradación acelerada por sobrecarga operativa y los rendimientos decrecientes del mantenimiento preventivo se basan en los modelos de confiabilidad y reemplazo de Jardine & Tsang **[4]** y Blanchard et al. **[5]**.
- **Entorno de Simulación Vensim:** Las funciones de acumulación `INTEG`, de retardo de primer orden `DELAY1I` y el esquema numérico de Euler con $\Delta t = 0.25$ meses siguen las especificaciones técnicas oficiales de Ventana Systems **[6]**.
- **Ética en Publicaciones con IA:** El protocolo de declaración formal en la sección de agradecimientos sigue las pautas éticas del IEEE **[7]**.
