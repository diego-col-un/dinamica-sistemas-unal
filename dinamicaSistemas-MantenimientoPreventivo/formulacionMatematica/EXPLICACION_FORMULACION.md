# Guía Explicativa y Conceptual de la Formulación Matemática
## Modelo de Dinámica de Sistemas: Mantenimiento Preventivo vs. Correctivo

> **Universidad Nacional de Colombia**  
> **Curso:** Dinámica de Sistemas  
> **Documento PDF oficial compilado:** [Explicacion_Detallada_Formulacion_Matematica.pdf](file:///c:/Users/diego/Documents/UNAL-26-2/DINAMICA%20DE%20SISTEMAS/dinamica-sistemas-unal/dinamicaSistemas-MantenimientoPreventivo/formulacionMatematica/Explicacion_Detallada_Formulacion_Matematica.pdf)

---

## 1. La Filosofía del Modelo: ¿Por qué Dinámica de Sistemas?

En la administración e ingeniería convencional de mantenimiento, las evaluaciones suelen basarse en cálculos estáticos (e.g., multiplicar una tasa de fallas histórica constante por un costo medio). Sin embargo, un parque tecnológico es un **sistema complejo con realimentación y no linealidades**:
- Cuando los equipos fallan y superan la capacidad del taller, se acumulan en espera.
- Los equipos parados obligan a los equipos activos a absorber toda la carga operativa.
- Esta sobrecarga acelera la degradación y dispara una **cascada de fallas endógena**.

La Dinámica de Sistemas de Jay Forrester sustituye los cálculos lineales por la metáfora de **tanques de agua (Niveles o Stocks)** regulados por **válvulas (Flujos o Rates)**:
> **El Principio de la Bañera:** Un nivel acumula el efecto neto de sus flujos. No puede modificarse instantáneamente mediante una decisión gerencial; solo cambia gradualmente a medida que los flujos entran o salen. Esto le otorga inercia y memoria al sistema.

---

## 2. Explicación Detallada de las Ecuaciones de Balance (Niveles)

Una **Ecuación de Balance** expresa formalmente la ley de conservación:
$$\frac{d(\text{Nivel})}{dt} = \sum \text{Flujos Entrantes} - \sum \text{Flujos Salientes}$$

### 2.1. Eje Operativo: Equipos Operativos ($O$) y en Falla ($F$)
- $\frac{dO}{dt} = R(t) - F_{\text{flujo}}(t), \quad O(0) = 96$
- $\frac{dF}{dt} = F_{\text{flujo}}(t) - R(t), \quad F(0) = 4$

**¿Por qué su suma es constante ($O + F = 100$)?**
$$\frac{d(O + F)}{dt} = (R - F_{\text{flujo}}) + (F_{\text{flujo}} - R) = 0 \implies O(t) + F(t) = 100 \quad \forall t$$
Representa un **sistema cerrado**: no se adquieren nuevos equipos ni se descartan activos durante el horizonte de 60 meses.

### 2.2. Eje de Confiabilidad: Salud del Parque ($S$)
$$\frac{dS}{dt} = \text{Rec}_{\text{MP}}(t) - \text{Deg}(t), \quad S(0) = 0.85$$
La salud es una variable intensiva ($S \in [0, 1]$) que funciona como un "capital de confiabilidad". Disminuye por el envejecimiento natural y la sobrecarga, y aumenta con las intervenciones preventivas.

### 2.3. Eje Financiero: Costos Acumulados ($C_m$ y $C_i$)
- $\frac{dC_m}{dt} = c_{\text{mp}}(t) + c_{\text{mc}}(t), \quad C_m(0) = 0$
- $\frac{dC_i}{dt} = c_{\text{inact}}(t), \quad C_i(0) = 0$

Son **acumuladores contables (sumideros)**: no tienen flujos de salida porque representan la acumulación histórica del dinero gastado y de las pérdidas por inactividad.

### 2.4. Eje de Inercia de Política: Esfuerzo de MP Efectivo ($MP_e$)
$$\frac{d(MP_e)}{dt} = \frac{f_{\text{mp}} - MP_e(t)}{\tau_{\text{mp}}}, \quad MP_e(0) = 0, \quad \tau_{\text{mp}} = 3.0 \text{ meses}$$
En la práctica gerencial, instaurar un plan de MP no mejora el parque al día siguiente. Existe un **retraso de 3 meses** para programar técnicos, comprar repuestos y ejecutar las primeras rondas de mantenimiento.

---

## 3. Anatomía de las Ecuaciones de Flujo (Rates)

### 3.1. Flujo de Fallas: $F_{\text{flujo}} = O(t) \cdot \lambda(t)$
Solo los equipos *operativos* pueden fallar (población en riesgo). La tasa de fallas mensual $\lambda(S) = 0.02 \cdot [1 + 4(1 - S)]$ pasa de 2% mensual con salud óptima ($S=1$) a 10% mensual con salud crítica ($S=0$).

### 3.2. Flujo de Reparación: $R = \min\left( \frac{F}{1.5}, \; 4.0 \right)$
La ecuación no lineal más crítica:
- Si $F < 6$ equipos, el taller opera holgado y atiende las reparaciones al ritmo $F/1.5$.
- Si $F \ge 6$ equipos, el taller alcanza su **tope de 4 equipos/mes**. El exceso de fallas se acumula en una cola sin salida.

### 3.3. Degradación: $\text{Deg} = S \cdot 0.025 \cdot \left[ 1 + 2 \cdot \frac{F}{100} \right]$
El desgaste combina envejecimiento basal (2.5% mensual) y **sobrecarga operativa**: si 30 equipos están averiados, los 70 restantes trabajan más horas y más forzados, sufriendo un 60% más de desgaste.

### 3.4. Recuperación por MP: $\text{Rec}_{\text{MP}} = (1 - S) \cdot 0.6 \cdot MP_e$
Modela la **Ley de Rendimientos Decrecientes**:
- Si $S = 0.5$, la brecha es $(1 - 0.5) = 0.5$, y el mantenimiento genera un gran salto en salud.
- Si $S = 0.95$, la brecha es solo $0.05$, y hacer más preventivo apenas produce mejoras marginales.

### 3.5. Flujos Económicos
- $c_{\text{mp}} = f_{\text{mp}} \cdot O \cdot 120$ USD/mes (gasto preventivo programado).
- $c_{\text{mc}} = R \cdot 900$ USD/mes (reparar es **7.5 veces más costoso** que prevenir).
- $c_{\text{inact}} = F \cdot 600$ USD/mes (lucro cesante por equipo parado).

---

## 4. Dinámica de Bucles de Realimentación

1. **R1 (Reforzador - Bola de Nieve):**  
   Menor Salud $\rightarrow$ Mayor tasa de fallas $\rightarrow$ Más equipos parados $\rightarrow$ Mayor sobrecarga sobre los operativos $\rightarrow$ Mayor degradación $\rightarrow$ Menor salud.  
   *Es el bucle destructivo que colapsa el parque sin MP.*

2. **B1 (Balanceador - Control Preventivo):**  
   Menor Salud $\rightarrow$ Mayor brecha $(1 - S) \rightarrow$ Mayor recuperación efectiva por MP $\rightarrow$ Sube la salud.  
   *Actúa como termostato que estabiliza la condición del parque.*

3. **B2 (Balanceador con Saturación - Trampa del Taller):**  
   Más equipos en falla $\rightarrow$ Más reparaciones necesarias $\rightarrow$ Menos equipos en falla.  
   *Cuando las fallas superan 4 eq/mes, B2 se desactiva por saturación y R1 toma el control.*

---

## 5. Estabilidad Numérica y Paso de Integración ($\Delta t = 0.25$ meses)

Para el método explícito de Euler, el criterio de estabilidad matemática exige:
$$\Delta t \le \frac{\tau_{\min}}{2}$$
Dado que $T_{\text{rep}} = 1.5$ meses y $\tau_{\text{mp}} = 3.0$ meses, la constante de tiempo más rápida es $\tau_{\min} = 1.5$ meses. El límite crítico es:
$$\Delta t \le \frac{1.5}{2} = 0.75 \text{ meses}$$
Al seleccionar $\Delta t = 0.25$ meses ($1$ semana), se cumple holgadamente $\Delta t \le \frac{\tau_{\min}}{6}$, garantizando una **solución numérica incondicionalmente estable, sin oscilaciones espurias** y con coincidencia frente a Runge-Kutta 4.

---

## 6. Comparación de Políticas y Asimetría del Riesgo

| Política | Intervalo | Salud Final | Disp. Media | Costo Total (60m) | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Sin MP** | 0 m | 0.30 | 56.8 % | USD 1,607 k | **Colapso:** Taller saturado 52 meses; inactividad = 77% del costo. |
| **MP Baja** | 12 m | 0.48 | 66.1 % | USD 1,440 k | **Insuficiente:** Taller saturado 48 meses; costo sigue muy alto. |
| **MP Intermedia** | 6 m | 0.83 | 94.1 % | **USD 445 k** | **ÓPTIMO GLOBAL:** El taller nunca satura; ahorra 72% frente a Sin MP. |
| **MP Intensiva** | 3 m | 0.90 | 96.7 % | USD 475 k | **Sobregasto:** Gana solo 2.6% de disponibilidad pero cuesta USD 30 k más. |

### La Regla de Oro de la Asimetría del Riesgo:
- Equivocarse por exceso de mantenimiento (cada 3 meses en lugar de 6) incrementa el costo apenas un **+10%**.
- Equivocarse por defecto de mantenimiento (relajar el intervalo a 12 meses) incrementa el costo un **+223%**.
> **Conclusión:** En sistemas con restricciones de capacidad y bucles de sobrecarga, *el exceso de mantenimiento preventivo es un orden de magnitud más seguro y económico que el defecto*.
