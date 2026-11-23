# Formulación Matemática y Ecuaciones de Balance
## Modelo de Dinámica de Sistemas (Jay Forrester)
### Gestión de un Parque Tecnológico: Mantenimiento Preventivo vs. Correctivo

> **Universidad Nacional de Colombia**  
> **Curso:** Dinámica de Sistemas  
> **Documento PDF oficial compilado:** [Formulacion_Matematica_Dinamica_Sistemas.pdf](file:///c:/Users/diego/Documents/UNAL-26-2/DINAMICA%20DE%20SISTEMAS/dinamica-sistemas-unal/dinamicaSistemas-MantenimientoPreventivo/formulacionMatematica/Formulacion_Matematica_Dinamica_Sistemas.pdf)

---

## 1. Fundamentación Teórica del Principio de Balance

En el paradigma de Dinámica de Sistemas fundado por Jay W. Forrester, cualquier sistema dinámico complejo se conceptualiza mediante una ontología de **Niveles (Stocks)** y **Flujos (Rates)**:

- **Variables de Nivel ($X_i$):** Acumulaciones que definen el estado interno del sistema en un instante $t$ y le otorgan memoria e inercia.
- **Variables de Flujo ($\Phi$):** Tasas de variación por unidad de tiempo que alimentan o drenan a los niveles.
- **Variables Auxiliares ($A$):** Funciones algebraicas que transforman información de niveles o parámetros para regular las válvulas de flujo.

### Ecuación General de Balance de Forrester
$$\frac{d X_i(t)}{dt} = \sum \Phi_{\text{in}, i}(t) - \sum \Phi_{\text{out}, i}(t)$$

En su forma acumulativa integral:
$$X_i(t) = X_i(t_0) + \int_{t_0}^t \left[ \sum \Phi_{\text{in}, i}(\tau) - \sum \Phi_{\text{out}, i}(\tau) \right] d\tau, \quad X_i(t_0) = X_{i,0}$$

En diferencias finitas (método de Euler con paso $\Delta t$):
$$X_i(t + \Delta t) = X_i(t) + \Delta t \cdot \left[ \sum \Phi_{\text{in}, i}(t) - \sum \Phi_{\text{out}, i}(t) \right]$$

---

## 2. Ecuaciones de Balance de los Niveles (Stocks)

El modelo cuenta con **5 variables de nivel principales** y **1 nivel interno de retardo de primer orden**.

### 2.1. Equipos Operativos ($O$)
- **Significado:** Equipos en servicio activo y productivo.
- **Entrada:** Flujo de Reparación ($R$).
- **Salida:** Flujo de Fallas ($F_{\text{flujo}}$).
- **Ecuación diferencial de balance:**
  $$\frac{dO(t)}{dt} = R(t) - F_{\text{flujo}}(t)$$
- **Condición inicial:**
  $$O(0) = N - F(0) = 100 - 4 = 96 \quad [\text{equipos}]$$

### 2.2. Equipos en Falla ($F$)
- **Significado:** Equipos fuera de servicio esperando o recibiendo reparación correctiva en el taller.
- **Entrada:** Flujo de Fallas ($F_{\text{flujo}}$).
- **Salida:** Flujo de Reparación ($R$).
- **Ecuación diferencial de balance:**
  $$\frac{dF(t)}{dt} = F_{\text{flujo}}(t) - R(t)$$
- **Condición inicial:**
  $$F(0) = 4 \quad [\text{equipos}]$$

#### Teorema de Conservación de Masa / Equipos (Parque Cerrado)
$$\frac{d}{dt}\big[ O(t) + F(t) \big] = \frac{dO}{dt} + \frac{dF}{dt} = \big(R - F_{\text{flujo}}\big) + \big(F_{\text{flujo}} - R\big) = 0$$
$$\implies O(t) + F(t) = O(0) + F(0) = 96 + 4 = 100 \text{ equipos} = N \quad (\text{Constante } \forall t)$$

---

### 2.3. Salud del Parque ($S$)
- **Significado:** Índice normalizado de condición física y confiabilidad del hardware ($S \in [0, 1]$).
- **Entrada:** Recuperación por Mantenimiento Preventivo ($\text{Rec}_{\text{MP}}$).
- **Salida:** Degradación ($\text{Deg}$).
- **Ecuación diferencial de balance:**
  $$\frac{dS(t)}{dt} = \text{Rec}_{\text{MP}}(t) - \text{Deg}(t)$$
- **Condición inicial:**
  $$S(0) = 0.85 \quad [\text{adimensional}]$$

---

### 2.4. Costo Acumulado de Mantenimiento ($C_m$)
- **Significado:** Nivel acumulador del gasto financiero directo en actividades preventivas y correctivas.
- **Entradas:** Tasa de Costo MP ($c_{\text{mp}}$) + Tasa de Costo MC ($c_{\text{mc}}$).
- **Ecuación diferencial de balance:**
  $$\frac{dC_m(t)}{dt} = c_{\text{mp}}(t) + c_{\text{mc}}(t)$$
- **Condición inicial:**
  $$C_m(0) = 0 \quad [\text{USD}]$$

---

### 2.5. Costo Acumulado de Inactividad ($C_i$)
- **Significado:** Nivel financiero acumulador de pérdidas por lucro cesante y parada de equipos.
- **Entrada:** Tasa de Costo de Inactividad ($c_{\text{inact}}$).
- **Ecuación diferencial de balance:**
  $$\frac{dC_i(t)}{dt} = c_{\text{inact}}(t)$$
- **Condición inicial:**
  $$C_i(0) = 0 \quad [\text{USD}]$$

---

### 2.6. Esfuerzo de MP Efectivo ($MP_e$) &mdash; Nivel del Retardo
En Vensim se formula mediante `DELAY1I(Frecuencia MP, Retraso efecto MP, 0)`. Matemáticamente equivale a un filtro pasa-bajos o retardo de información de 1er orden:
$$\frac{d(MP_e(t))}{dt} = \frac{f_{\text{mp}}(t) - MP_e(t)}{\tau_{\text{mp}}}$$
- **Condición inicial:** $MP_e(0) = 0 \quad [1/\text{mes}]$
- **Constante de tiempo:** $\tau_{\text{mp}} = 3.0$ meses.

---

## 3. Formulación de las Ecuaciones de Flujo (Rates)

| Flujo | Ecuación Matemática | Unidades | Significado Dinámico |
| :--- | :--- | :---: | :--- |
| **Fallas ($F_{\text{flujo}}$)** | $F_{\text{flujo}}(t) = O(t) \cdot \lambda(t)$ | equipos / mes | Equipos que pasan de servicio activo a falla mensual. |
| **Reparación ($R$)** | $R(t) = \min\left( \frac{F(t)}{T_{\text{rep}}}, \; C_{\text{taller}} \right)$ | equipos / mes | Restauración por el taller con saturación no lineal ($C_{\text{taller}} = 4$). |
| **Degradación ($\text{Deg}$)** | $\text{Deg}(t) = S(t) \cdot \delta_0 \cdot \left[ 1 + \alpha \cdot \frac{F(t)}{N} \right]$ | $1 / \text{mes}$ | Desgaste natural ($\delta_0 = 0.025$) amplificado por sobrecarga ($\alpha = 2$). |
| **Recuperación MP ($\text{Rec}_{\text{MP}}$)** | $\text{Rec}_{\text{MP}}(t) = (1 - S(t)) \cdot \eta_{\text{mp}} \cdot MP_e(t)$ | $1 / \text{mes}$ | Mejora de salud proporcional a la brecha $(1 - S)$ (rendimientos decrecientes). |
| **Costo MP ($c_{\text{mp}}$)** | $c_{\text{mp}}(t) = f_{\text{mp}} \cdot O(t) \cdot U_{\text{mp}}$ | USD / mes | Flujo de gasto en intervenciones preventivas ($U_{\text{mp}} = 120$ USD). |
| **Costo MC ($c_{\text{mc}}$)** | $c_{\text{mc}}(t) = R(t) \cdot U_{\text{mc}}$ | USD / mes | Flujo de gasto en reparaciones correctivas ($U_{\text{mc}} = 900$ USD). |
| **Costo Inactividad ($c_{\text{inact}}$)** | $c_{\text{inact}}(t) = F(t) \cdot U_{\text{inact}}$ | USD / mes | Flujo de pérdida por equipos detenidos ($U_{\text{inact}} = 600$ USD/eq-mes). |

---

## 4. Ecuaciones Auxiliares y Funciones de Decisión

1. **Tasa de Fallas Endógena ($\lambda$):**
   $$\lambda(t) = \lambda_0 \cdot \Big[ 1 + \sigma \cdot (1 - S(t)) \Big] \quad \left[\frac{1}{\text{mes}}\right]$$
   - $\lambda_0 = 0.02$, $\sigma = 4.0$. Si $S=1 \implies \lambda = 0.02$; si $S=0 \implies \lambda = 0.10$.

2. **Fracción en Falla ($\phi_F$):**
   $$\phi_F(t) = \frac{F(t)}{N} \quad [\text{adimensional}]$$

3. **Frecuencia de Mantenimiento Preventivo ($f_{\text{mp}}$):**
   $$f_{\text{mp}} = \begin{cases} 0, & \text{si } I_{\text{mp}} = 0 \\ \frac{1}{I_{\text{mp}}}, & \text{si } I_{\text{mp}} > 0 \end{cases} \quad \left[\frac{1}{\text{mes}}\right]$$
   - Escenarios de intervalo $I_{\text{mp}} \in \{0, 12, 6, 3\}$ meses.

4. **Indicadores de Desempeño (KPIs):**
   - **Disponibilidad:** $\text{Disp}(t) = \frac{O(t)}{N}$
   - **Inactividad porcentual:** $\text{Inact}(t) = 100 \cdot \frac{F(t)}{N}$
   - **Costo Total Acumulado:** $C_{\text{total}}(t) = C_m(t) + C_i(t)$

---

## 5. Matriz de Consistencia Dimensional

$$\left[ \frac{d(\text{Stock})}{dt} \right] = [\text{Entradas}] - [\text{Salidas}] = \frac{[\text{Unidades de Stock}]}{[\text{Tiempo}]}$$

| Ecuación de Balance | Unidad Nivel | Unidad Tiempo | Unidad Flujo ($dS/dt$) | Verificación Dimensional |
| :--- | :---: | :---: | :---: | :--- |
| $\frac{dO}{dt} = R - F_{\text{flujo}}$ | equipos | mes | equipos / mes | $\text{eq/mes} - \text{eq}\cdot(1/\text{mes}) = \text{eq/mes}$ $\checkmark$ |
| $\frac{dF}{dt} = F_{\text{flujo}} - R$ | equipos | mes | equipos / mes | $\text{eq/mes} - \text{eq/mes} = \text{eq/mes}$ $\checkmark$ |
| $\frac{dS}{dt} = \text{Rec}_{\text{MP}} - \text{Deg}$ | Dmnl (0-1) | mes | $1 / \text{mes}$ | $\text{Dmnl}\cdot(1/\text{mes}) - \text{Dmnl}\cdot(1/\text{mes}) = 1/\text{mes}$ $\checkmark$ |
| $\frac{dC_m}{dt} = c_{\text{mp}} + c_{\text{mc}}$ | USD | mes | USD / mes | $(1/\text{mes})\cdot\text{eq}\cdot(\text{USD/eq}) + (\text{eq/mes})\cdot(\text{USD/eq}) = \text{USD/mes}$ $\checkmark$ |
| $\frac{dC_i}{dt} = c_{\text{inact}}$ | USD | mes | USD / mes | $\text{eq}\cdot(\text{USD}/(\text{eq}\cdot\text{mes})) = \text{USD/mes}$ $\checkmark$ |
| $\frac{d(MP_e)}{dt} = \frac{f_{\text{mp}} - MP_e}{\tau_{\text{mp}}}$ | $1 / \text{mes}$ | mes | $1 / \text{mes}^2$ | $\frac{1/\text{mes} - 1/\text{mes}}{\text{mes}} = \frac{1}{\text{mes}^2}$ $\checkmark$ |

---

## 6. Esquema Matricial y Algoritmo de Integración

El sistema se define mediante el vector de estado $\vec{y}(t) \in \mathbb{R}^6$:
$$\vec{y}(t) = \begin{bmatrix} O(t) \\ F(t) \\ S(t) \\ C_m(t) \\ C_i(t) \\ MP_e(t) \end{bmatrix}, \quad \vec{y}(0) = \begin{bmatrix} 96.0 \\ 4.0 \\ 0.85 \\ 0.0 \\ 0.0 \\ 0.0 \end{bmatrix}$$

El campo vectorial de derivadas temporales $\frac{d\vec{y}}{dt} = \vec{f}(\vec{y}, t)$ se resuelve mediante integración numérica de Euler:
$$\vec{y}_{k+1} = \vec{y}_k + \Delta t \cdot \vec{f}(\vec{y}_k, \vec{p})$$
con $\Delta t = 0.25$ meses ($1$ semana), $t_k = k \cdot \Delta t$ para $k = 0, 1, \dots, 240$ pasos ($T_{\text{final}} = 60$ meses).
