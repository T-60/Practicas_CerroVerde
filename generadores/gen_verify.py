import os
# -*- coding: utf-8 -*-
"""Genera y verifica el banco numerico/logico. Cada item trae 'check' que recalcula la respuesta."""
import json, itertools, random, math
from collections import Counter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "banco", "numerico_logico.json")

def f(n, dec=None):
    """Formato peruano simple: miles con espacio, decimales con punto."""
    if dec is not None:
        n = round(n, dec)
        s = f"{n:,.{dec}f}"
    else:
        if abs(n - round(n)) < 1e-9:
            s = f"{int(round(n)):,}"
        else:
            s = f"{n:,}"
    return s.replace(",", " ")

ALF = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
assert len(ALF) == 27
def L(i): return ALF[i - 1]
def P(c): return ALF.index(c) + 1
NOTA_ALF = "<br><i>(Considere el alfabeto español de 27 letras, incluida la Ñ.)</i>"

items = []
def add(id, area, sub, diff, prompt, correct, distractors, expl, check):
    items.append(dict(id=id, area=area, subtype=sub, difficulty=diff, prompt=prompt,
                      correct=correct, distractors=distractors, explanation=expl, check=check))

# ---------------- NUMERICO ----------------
A, Nn = "numerico", "logico"
add("n01", A, "operaciones", "facil",
    "Una planta concentradora produce <b>1 250 t</b> de concentrado de cobre por día. ¿Cuántas toneladas produce en <b>24 días</b>?",
    "30 000 t", ["28 000 t", "32 500 t", "29 500 t"],
    "1 250 × 24 = 30 000 t.", lambda: f(1250*24) + " t")
add("n02", A, "operaciones", "facil",
    "Tres camiones de <b>240 t</b> de capacidad cada uno realizan <b>7 viajes</b> por turno a plena carga. ¿Cuántas toneladas transportan en total en un turno?",
    "5 040 t", ["1 680 t", "4 800 t", "5 280 t"],
    "3 × 240 = 720 t por ronda; 720 × 7 = 5 040 t.", lambda: f(3*240*7) + " t")
add("n03", A, "operaciones", "facil",
    "Calcule: <b>18 ÷ 3 × 2 + 4² − 5 × (6 − 2)</b>",
    "8", ["3", "28", "−8"],
    "Paréntesis: 6 − 2 = 4. Potencia: 4² = 16. De izquierda a derecha: 18 ÷ 3 = 6; 6 × 2 = 12; 5 × 4 = 20. Luego 12 + 16 − 20 = 8.",
    lambda: f(18/3*2 + 4**2 - 5*(6-2)))
add("n04", A, "operaciones", "media",
    "Un tanque de agua de proceso contiene <b>84 000 L</b>. Se extraen <b>3 500 L/h</b> y, al mismo tiempo, ingresan <b>1 400 L/h</b>. ¿En cuántas horas se vacía el tanque?",
    "40 h", ["24 h", "60 h", "17 h"],
    "Salida neta = 3 500 − 1 400 = 2 100 L/h. Tiempo = 84 000 ÷ 2 100 = 40 h.", lambda: f(84000/(3500-1400)) + " h")
add("n05", A, "operaciones", "dificil",
    "Calcule: <b>(0,25 + 1/8) ÷ 0,375 × 2³ − √144</b>",
    "−4", ["4", "0", "−11", "20"],
    "0,25 + 0,125 = 0,375; 0,375 ÷ 0,375 = 1; 1 × 8 = 8; √144 = 12; 8 − 12 = −4.",
    lambda: f((0.25 + 1/8)/0.375*2**3 - math.sqrt(144)).replace("-", "−"))

add("n06", A, "porcentajes", "facil",
    "La producción trimestral de cátodos fue de <b>80 000 t</b>. Si el siguiente trimestre aumenta en <b>15 %</b>, ¿cuál será la nueva producción?",
    "92 000 t", ["95 000 t", "88 000 t", "12 000 t"],
    "15 % de 80 000 = 12 000. Nueva producción = 80 000 + 12 000 = 92 000 t.", lambda: f(80000*1.15) + " t")
add("n07", A, "porcentajes", "facil",
    "De los <b>1 200</b> trabajadores de una operación, el <b>35 %</b> labora en el turno noche. ¿Cuántos trabajadores hay en el turno noche?",
    "420", ["350", "380", "780"],
    "0,35 × 1 200 = 420 trabajadores.", lambda: f(0.35*1200))
add("n08", A, "porcentajes", "media",
    "El precio de un insumo sube <b>20 %</b> en enero y luego baja <b>20 %</b> en febrero. Respecto al precio inicial, el precio final:",
    "Disminuyó 4 %", ["No varió", "Aumentó 4 %", "Disminuyó 2 %", "Disminuyó 20 %"],
    "Factor total = 1,20 × 0,80 = 0,96, es decir, una disminución de 4 %.",
    lambda: "Disminuyó " + f(round((1 - 1.2*0.8)*100, 6)) + " %")
add("n09", A, "porcentajes", "media",
    "Un mineral tiene una ley de <b>0,45 % de cobre</b>. ¿Cuántas toneladas de cobre contienen <b>120 000 t</b> de mineral?",
    "540 t", ["5 400 t", "54 t", "450 t"],
    "0,45 % = 0,0045. 120 000 × 0,0045 = 540 t de cobre.", lambda: f(round(120000*0.0045, 6)) + " t")
add("n10", A, "porcentajes", "facil",
    "El consumo diario de agua fresca bajó de <b>2 500 m³</b> a <b>2 150 m³</b> gracias a la recirculación. ¿En qué porcentaje se redujo?",
    "14 %", ["35 %", "16,3 %", "12 %"],
    "Reducción = 2 500 − 2 150 = 350 m³. 350 ÷ 2 500 = 0,14 = 14 %.", lambda: f(round((2500-2150)/2500*100, 6)) + " %")
add("n11", A, "porcentajes", "dificil",
    "Se desea obtener <b>396 t</b> de cobre fino. El mineral tiene una ley de <b>0,5 % Cu</b> y la recuperación metalúrgica de la planta es de <b>88 %</b>. ¿Cuántas toneladas de mineral se deben procesar?",
    "90 000 t", ["79 200 t", "87 120 t", "100 000 t", "45 000 t"],
    "Cobre recuperado por tonelada = 0,005 × 0,88 = 0,0044 t. Mineral = 396 ÷ 0,0044 = 90 000 t.",
    lambda: f(round(396/(0.005*0.88), 6)) + " t")

add("n12", A, "regla_de_tres", "facil",
    "Si <b>4 camiones</b> transportan <b>1 800 t</b> de mineral en un turno, ¿cuántas toneladas transportarán <b>7 camiones</b> iguales en el mismo turno?",
    "3 150 t", ["3 600 t", "2 700 t", "1 029 t"],
    "Regla de tres directa: 1 800 × 7 ÷ 4 = 3 150 t.", lambda: f(1800*7/4) + " t")
add("n13", A, "regla_de_tres", "facil",
    "<b>6 técnicos</b> realizan el mantenimiento de una faja en <b>15 días</b>. ¿En cuántos días lo harían <b>9 técnicos</b> con el mismo rendimiento?",
    "10 días", ["22,5 días", "12 días", "9 días"],
    "Regla de tres inversa: 6 × 15 ÷ 9 = 10 días.", lambda: f(6*15/9) + " días")
add("n14", A, "regla_de_tres", "media",
    "<b>8 perforadoras</b>, trabajando <b>6 h/día</b> durante <b>5 días</b>, perforan <b>480 taladros</b>. ¿Cuántos taladros perforarán <b>10 perforadoras</b>, trabajando <b>8 h/día</b> durante <b>4 días</b>?",
    "640", ["600", "512", "720", "480"],
    "Todas las magnitudes son directamente proporcionales a los taladros: 480 × (10/8) × (8/6) × (4/5) = 640.",
    lambda: f(round(480*(10/8)*(8/6)*(4/5), 6)))
add("n15", A, "regla_de_tres", "media",
    "Una faja transportadora traslada <b>2 700 t</b> en <b>45 minutos</b>. A ritmo constante, ¿cuántas toneladas traslada en <b>2 h 20 min</b>?",
    "8 400 t", ["6 300 t", "7 200 t", "8 100 t"],
    "2 h 20 min = 140 min. 2 700 ÷ 45 = 60 t/min. 60 × 140 = 8 400 t.", lambda: f(2700/45*140) + " t")
add("n16", A, "regla_de_tres", "dificil",
    "<b>12 obreros</b>, trabajando <b>8 h/día</b>, construyen <b>60 m</b> de canal de relaves en <b>10 días</b>. ¿Cuántos días necesitarán <b>16 obreros</b>, trabajando <b>6 h/día</b>, para construir <b>90 m</b> del mismo canal?",
    "15 días", ["10 días", "11,25 días", "20 días", "13,5 días"],
    "Días = 10 × (12/16) × (8/6) × (90/60). Más obreros → menos días (inversa); menos horas → más días (inversa); más metros → más días (directa). 10 × 0,75 × 4/3 × 1,5 = 15 días.",
    lambda: f(round(10*(12/16)*(8/6)*(90/60), 6)) + " días")

add("n17", A, "fracciones_proporciones", "facil",
    "De un lote de <b>6 400 t</b> de concentrado, los <b>3/8</b> se destinan a exportación. ¿Cuántas toneladas se exportan?",
    "2 400 t", ["4 000 t", "1 600 t", "2 133 t"],
    "6 400 ÷ 8 = 800; 800 × 3 = 2 400 t.", lambda: f(6400*3/8) + " t")
add("n18", A, "fracciones_proporciones", "media",
    "De la producción mensual de concentrado, <b>2/5</b> se embarca por el puerto; de lo que queda, <b>1/3</b> se envía a una refinería y el resto, <b>36 000 t</b>, se almacena. ¿Cuál fue la producción mensual?",
    "90 000 t", ["60 000 t", "108 000 t", "72 000 t"],
    "Tras embarcar quedan 3/5 P. Se envía 1/3 de eso y queda 2/3 × 3/5 P = 2/5 P = 36 000 → P = 90 000 t.",
    lambda: f(36000/((1-2/5)*(1-1/3))) + " t")
add("n19", A, "fracciones_proporciones", "facil",
    "En una solución de lixiviación, el agua y el reactivo están en razón <b>7 : 2</b>. Si se preparan <b>1 350 L</b> de solución, ¿cuántos litros son de reactivo?",
    "300 L", ["385 L", "1 050 L", "270 L"],
    "Partes totales = 7 + 2 = 9. 1 350 ÷ 9 = 150 L por parte. Reactivo = 2 × 150 = 300 L.", lambda: f(1350*2/9) + " L")
add("n20", A, "fracciones_proporciones", "dificil",
    "Un bono de <b>S/ 7 200</b> se reparte entre tres cuadrillas en forma <b>directamente proporcional</b> a 2, 3 y 4 e <b>inversamente proporcional</b> a 1, 3 y 2, respectivamente. ¿Cuánto recibe la segunda cuadrilla?",
    "S/ 1 440", ["S/ 2 400", "S/ 2 880", "S/ 1 800", "S/ 960"],
    "Índices: 2/1 = 2; 3/3 = 1; 4/2 = 2. Suma = 5. Cada unidad = 7 200 ÷ 5 = 1 440. La segunda recibe 1 × 1 440 = S/ 1 440.",
    lambda: "S/ " + f(7200*(3/3)/(2/1+3/3+4/2)))

add("n21", A, "problemas", "facil",
    "Un supervisor tiene el triple de la edad de su hijo. Dentro de <b>12 años</b> tendrá el doble de la edad que tenga su hijo. ¿Qué edad tiene hoy el supervisor?",
    "36 años", ["24 años", "48 años", "42 años"],
    "Hijo = x, supervisor = 3x. 3x + 12 = 2(x + 12) → x = 12. Supervisor = 36 años.",
    lambda: f(next(3*x for x in range(1, 100) if 3*x + 12 == 2*(x + 12))) + " años")
add("n22", A, "problemas", "media",
    "La bomba A vacía una poza en <b>12 h</b> y la bomba B la vacía en <b>18 h</b>. Si ambas trabajan juntas, ¿en cuánto tiempo vacían la poza?",
    "7 h 12 min", ["15 h", "7 h 30 min", "6 h 48 min", "8 h"],
    "Juntas: 1/12 + 1/18 = 5/36 de poza por hora. Tiempo = 36/5 = 7,2 h = 7 h 12 min.",
    lambda: (lambda t: f"{int(t)} h {round((t-int(t))*60)} min")(1/(1/12+1/18)))
add("n23", A, "problemas", "media",
    "Dos camionetas parten al mismo tiempo desde dos campamentos separados <b>99 km</b> y avanzan una hacia la otra a <b>30 km/h</b> y <b>36 km/h</b>. ¿En cuánto tiempo se encuentran?",
    "1 h 30 min", ["1 h 39 min", "1 h 15 min", "2 h", "3 h 18 min"],
    "Velocidad de acercamiento = 30 + 36 = 66 km/h. Tiempo = 99 ÷ 66 = 1,5 h = 1 h 30 min.",
    lambda: (lambda t: f"{int(t)} h {round((t-int(t))*60)} min")(99/(30+36)))
add("n24", A, "problemas", "media",
    "Se mezclan <b>400 t</b> de mineral con ley <b>0,60 % Cu</b> y <b>600 t</b> de mineral con ley <b>0,35 % Cu</b>. ¿Cuál es la ley de la mezcla?",
    "0,45 % Cu", ["0,475 % Cu", "0,50 % Cu", "0,40 % Cu"],
    "Cobre: 400 × 0,006 = 2,4 t; 600 × 0,0035 = 2,1 t. Total 4,5 t en 1 000 t → 0,45 %.",
    lambda: f((400*0.6 + 600*0.35)/1000, 2).replace(".", ",") + " % Cu")
add("n25", A, "problemas", "dificil",
    "Un camión sube cargado por una rampa a <b>20 km/h</b> y baja vacío por la misma rampa a <b>30 km/h</b>. ¿Cuál es su velocidad media en el viaje completo de ida y vuelta?",
    "24 km/h", ["25 km/h", "26 km/h", "22,5 km/h"],
    "Sea d la longitud. Tiempo = d/20 + d/30 = d/12. Velocidad media = 2d ÷ (d/12) = 24 km/h (media armónica).",
    lambda: f(2/(1/20 + 1/30)) + " km/h")
add("n26", A, "problemas", "media",
    "Los equipos A y B juntos terminan un trabajo en <b>8 días</b>; A solo lo terminaría en <b>12 días</b>. Trabajan juntos <b>3 días</b> y luego B termina solo el resto. ¿Cuántos días adicionales trabaja B?",
    "15 días", ["10 días", "24 días", "12 días", "9 días"],
    "B solo: 1/8 − 1/12 = 1/24 por día. En 3 días juntos hacen 3/8; faltan 5/8. Días de B = (5/8) ÷ (1/24) = 15.",
    lambda: f(round((1 - 3/8)/(1/8 - 1/12), 6)) + " días")

TAB_A = ("<table><tr><th>Mes</th><th>Concentrado (t)</th></tr>"
         "<tr><td>Enero</td><td>42 000</td></tr><tr><td>Febrero</td><td>38 500</td></tr>"
         "<tr><td>Marzo</td><td>45 500</td></tr><tr><td>Abril</td><td>44 000</td></tr></table>")
prodA = [42000, 38500, 45500, 44000]
add("n27", A, "interpretacion_tablas", "facil",
    "<p>Producción de concentrado de cobre:</p>" + TAB_A + "<p>¿Cuál fue la producción mensual promedio?</p>",
    "42 500 t", ["42 000 t", "43 000 t", "44 000 t"],
    "Total = 42 000 + 38 500 + 45 500 + 44 000 = 170 000 t. Promedio = 170 000 ÷ 4 = 42 500 t.",
    lambda: f(sum(prodA)/4) + " t")
add("n28", A, "interpretacion_tablas", "media",
    "<p>Producción de concentrado de cobre:</p>" + TAB_A + "<p>¿En qué porcentaje aproximado aumentó la producción de febrero a marzo?</p>",
    "18,2 %", ["15,4 %", "7,0 %", "20,0 %"],
    "Aumento = 45 500 − 38 500 = 7 000. 7 000 ÷ 38 500 ≈ 0,1818 → 18,2 %.",
    lambda: f((45500-38500)/38500*100, 1).replace(".", ",") + " %")
add("n32", A, "interpretacion_tablas", "facil",
    "<p>Producción de concentrado de cobre:</p>" + TAB_A + "<p>¿Cuál es la diferencia entre el mes de mayor y el de menor producción?</p>",
    "7 000 t", ["3 500 t", "5 500 t", "6 000 t"],
    "Mayor: marzo (45 500 t). Menor: febrero (38 500 t). Diferencia = 7 000 t.",
    lambda: f(max(prodA) - min(prodA)) + " t")
TAB_B = ("<table><tr><th>Turno</th><th>Agua consumida (m³)</th><th>Mineral procesado (t)</th></tr>"
         "<tr><td>A</td><td>3 600</td><td>12 000</td></tr><tr><td>B</td><td>2 940</td><td>10 500</td></tr>"
         "<tr><td>C</td><td>2 880</td><td>9 000</td></tr></table>")
turnos = {"Turno A": (3600, 12000), "Turno B": (2940, 10500), "Turno C": (2880, 9000)}
add("n29", A, "interpretacion_tablas", "media",
    "<p>Consumo de agua por turno en la concentradora:</p>" + TAB_B + "<p>¿Qué turno tuvo el <b>menor consumo de agua por tonelada</b> procesada?</p>",
    "Turno B", ["Turno A", "Turno C", "Los tres consumieron igual"],
    "A: 3 600/12 000 = 0,30 m³/t; B: 2 940/10 500 = 0,28 m³/t; C: 2 880/9 000 = 0,32 m³/t. El menor es el turno B.",
    lambda: min(turnos, key=lambda k: turnos[k][0]/turnos[k][1]))
TAB_C = ("<table><tr><th>Camión</th><th>Horas programadas</th><th>Horas operativas</th></tr>"
         "<tr><td>C-01</td><td>720</td><td>612</td></tr><tr><td>C-02</td><td>720</td><td>648</td></tr>"
         "<tr><td>C-03</td><td>720</td><td>576</td></tr><tr><td>C-04</td><td>720</td><td>684</td></tr></table>")
add("n30", A, "interpretacion_tablas", "media",
    "<p>Horas registradas por la flota de acarreo en un mes:</p>" + TAB_C + "<p>La disponibilidad se calcula como horas operativas ÷ horas programadas. ¿Cuál es la disponibilidad de la flota completa?</p>",
    "87,5 %", ["85,0 %", "90,0 %", "88,5 %"],
    "Operativas = 612 + 648 + 576 + 684 = 2 520 h. Programadas = 4 × 720 = 2 880 h. 2 520 ÷ 2 880 = 0,875 = 87,5 %.",
    lambda: f((612+648+576+684)/2880*100, 1).replace(".", ",") + " %")
TAB_D = ("<table><tr><th>Zona del tajo</th><th>Mineral (t)</th><th>Ley (% Cu)</th></tr>"
         "<tr><td>Norte</td><td>50 000</td><td>0,40</td></tr><tr><td>Sur</td><td>30 000</td><td>0,60</td></tr>"
         "<tr><td>Este</td><td>20 000</td><td>0,50</td></tr></table>")
add("n31", A, "interpretacion_tablas", "dificil",
    "<p>Mineral enviado a la chancadora en una semana:</p>" + TAB_D + "<p>¿Cuál es la ley promedio ponderada del mineral enviado?</p>",
    "0,48 % Cu", ["0,50 % Cu", "0,46 % Cu", "0,52 % Cu"],
    "Cobre contenido: 50 000 × 0,004 = 200 t; 30 000 × 0,006 = 180 t; 20 000 × 0,005 = 100 t. Total 480 t en 100 000 t → 0,48 %. (El promedio simple, 0,50 %, es incorrecto porque los tonelajes difieren.)",
    lambda: f((50000*0.40 + 30000*0.60 + 20000*0.50)/100000, 2).replace(".", ",") + " % Cu")

# ---------------- LOGICO ----------------
B = "logico"
def nxt(seq_fn, n):  # helper
    return seq_fn(n)

s = [3 + 4*i for i in range(6)]
add("l01", B, "series_numericas", "facil", "¿Qué número continúa la serie?<br><b>3, 7, 11, 15, 19, ...</b>",
    "23", ["21", "24", "25"], "Se suma 4 cada vez: 19 + 4 = 23.", lambda: str(s[5]))
s2 = [2*3**i for i in range(5)]
add("l02", B, "series_numericas", "facil", "¿Qué número continúa la serie?<br><b>2, 6, 18, 54, ...</b>",
    "162", ["108", "72", "216"], "Cada término se multiplica por 3: 54 × 3 = 162.", lambda: str(s2[4]))
add("l03", B, "series_numericas", "media", "¿Qué número continúa la serie?<br><b>2, 5, 10, 17, 26, ...</b>",
    "37", ["35", "36", "39"], "Cada término es n² + 1 (n = 1, 2, 3...): 6² + 1 = 37. También: diferencias 3, 5, 7, 9, 11.",
    lambda: str(6**2 + 1))
add("l04", B, "series_numericas", "facil", "¿Qué número continúa la serie?<br><b>5, 6, 8, 11, 15, ...</b>",
    "20", ["19", "21", "18"], "Diferencias: +1, +2, +3, +4, +5. 15 + 5 = 20.", lambda: str(15 + 5))
s5 = [3]
for k in range(1, 6): s5.append(s5[-1] + k*k)
assert s5[:5] == [3, 4, 8, 17, 33]
add("l05", B, "series_numericas", "media", "¿Qué número continúa la serie?<br><b>3, 4, 8, 17, 33, ...</b>",
    "58", ["49", "56", "66"], "Se suman cuadrados perfectos: +1, +4, +9, +16, +25. 33 + 25 = 58.", lambda: str(s5[5]))
s6 = [2]
for k in range(5): s6.append(s6[-1] + 2**k)
assert s6[:5] == [2, 3, 5, 9, 17]
add("l06", B, "series_numericas", "facil", "¿Qué número continúa la serie?<br><b>2, 3, 5, 9, 17, ...</b>",
    "33", ["25", "34", "31"], "Diferencias: +1, +2, +4, +8, +16 (se duplican). 17 + 16 = 33.", lambda: str(s6[5]))
s7 = []
for i in range(4): s7 += [4*2**i, 20 - 3*i]
assert s7[:7] == [4, 20, 8, 17, 16, 14, 32]
add("l07", B, "series_numericas", "dificil", "¿Qué número continúa la serie?<br><b>4, 20, 8, 17, 16, 14, 32, ...</b>",
    "11", ["64", "12", "10"],
    "Son dos series intercaladas. Posiciones impares: 4, 8, 16, 32 (×2). Posiciones pares: 20, 17, 14, ... (−3). El término pedido es par: 14 − 3 = 11.",
    lambda: str(s7[7]))
s8 = [2]
for k in range(1, 6): s8.append(s8[-1]*k + 1)
assert s8[:5] == [2, 3, 7, 22, 89]
add("l08", B, "series_numericas", "dificil", "¿Qué número continúa la serie?<br><b>2, 3, 7, 22, 89, ...</b>",
    "446", ["356", "445", "534", "447"],
    "Regla: ×1 + 1, ×2 + 1, ×3 + 1, ×4 + 1, ×5 + 1. Entonces 89 × 5 + 1 = 446.", lambda: str(s8[5]))

add("l09", B, "series_letras", "facil", "¿Qué letra continúa la serie?<br><b>A, C, E, G, ...</b>" + NOTA_ALF,
    "I", ["H", "J", "K"], "Se avanza de 2 en 2 (se salta una letra): A, C, E, G, I.",
    lambda: L(P("G") + 2))
add("l10", B, "series_letras", "facil", "¿Qué letra continúa la serie?<br><b>B, E, H, K, ...</b>" + NOTA_ALF,
    "N", ["Ñ", "M", "O"], "Posiciones 2, 5, 8, 11 (+3). Sigue la posición 14: N.",
    lambda: L(P("K") + 3))
assert [P(c) for c in "ZXUQ"] == [27, 25, 22, 18]
add("l11", B, "series_letras", "media", "¿Qué letra continúa la serie?<br><b>Z, X, U, Q, ...</b>" + NOTA_ALF,
    "M", ["L", "N", "Ñ"], "Posiciones 27, 25, 22, 18: se resta 2, 3, 4 y luego 5. 18 − 5 = 13 → M.",
    lambda: L(18 - 5))
assert [P(c) for c in "DFIM"] == [4, 6, 9, 13]
add("l12", B, "series_letras", "media", "¿Qué letra continúa la serie?<br><b>D, F, I, M, ...</b>" + NOTA_ALF,
    "Q", ["P", "R", "O"], "Posiciones 4, 6, 9, 13: +2, +3, +4, +5. 13 + 5 = 18 → Q (en el alfabeto de 27 letras, P es 17 y Q es 18).",
    lambda: L(13 + 5))
assert [P(c) for c in "AZCXEV"] == [1, 27, 3, 25, 5, 23]
add("l13", B, "series_letras", "dificil", "¿Qué par de letras continúa la serie?<br><b>A, Z, C, X, E, V, ...</b>" + NOTA_ALF,
    "G, T", ["G, U", "F, T", "H, S"],
    "Dos series intercaladas: A, C, E, ... avanza de 2 en 2 → G (7). Z, X, V, ... retrocede de 2 en 2 → posición 21 → T.",
    lambda: f"{L(5+2)}, {L(23-2)}")

add("l14", B, "series_alfanumericas", "facil", "¿Qué término continúa la serie?<br><b>A2, C4, E6, G8, ...</b>" + NOTA_ALF,
    "I10", ["H10", "I9", "J10"], "Letras de 2 en 2 (A, C, E, G, I) y números pares (+2): I10.",
    lambda: f"{L(P('G')+2)}{8+2}")
add("l15", B, "series_alfanumericas", "media", "¿Qué término continúa la serie?<br><b>1B, 4D, 9F, 16H, ...</b>" + NOTA_ALF,
    "25J", ["25I", "20J", "36J"], "Números: cuadrados 1, 4, 9, 16, 25. Letras de 2 en 2: B, D, F, H, J. Resultado: 25J.",
    lambda: f"{5**2}{L(P('H')+2)}")
assert [P(c) for c in "ZWS"] == [27, 24, 20]
add("l16", B, "series_alfanumericas", "media", "¿Qué término continúa la serie?<br><b>Z1, W3, S6, ...</b>" + NOTA_ALF,
    "Ñ10", ["O10", "N10", "Ñ9"],
    "Letras: posiciones 27, 24, 20 (−3, −4) → 20 − 5 = 15 → Ñ. Números: 1, 3, 6 (+2, +3) → 6 + 4 = 10. Resultado: Ñ10.",
    lambda: f"{L(20-5)}{6+4}")

# Silogismos: verificados por modelos de conjuntos (fuerza bruta sobre universos pequenos)
def valid(premises, concl, nsets, U=3):
    """Valida silogismo: para todo modelo (cada elemento pertenece o no a cada conjunto), premisas => conclusion."""
    elems = list(itertools.product([0, 1], repeat=nsets))
    for assign in itertools.product(range(len(elems)), repeat=U):
        world = [elems[a] for a in assign]
        if all(p(world) for p in premises) and not concl(world):
            return False
    return True
def todos(a, b): return lambda w: all(e[b] for e in w if e[a])
def ningun(a, b): return lambda w: not any(e[a] and e[b] for e in w)
def algun(a, b): return lambda w: any(e[a] and e[b] for e in w)
def alguno_no(a, b): return lambda w: any(e[a] and not e[b] for e in w)
def todos_v(a, b): return lambda w: all(e[b] for e in w if e[a])

# l19: Todos I son C (0->1). Algunos C son V (1,2). Ninguna conclusion de I-V es valida
prem19 = [todos(0, 1), algun(1, 2)]
for c in [algun(0, 2), ningun(0, 2), todos(2, 0), alguno_no(0, 2)]:
    assert not valid(prem19, c, 3)
# l20: Todos S son I; algunos S son G => algunos I son G
assert valid([todos(0, 1), algun(0, 2)], algun(1, 2), 3)
assert not valid([todos(0, 1), algun(0, 2)], todos(1, 2), 3)
assert not valid([todos(0, 1), algun(0, 2)], todos(2, 0), 3)
assert not valid([todos(0, 1), algun(0, 2)], alguno_no(1, 2), 3)
# l21: Ningun P es V; todos B son P => ningun B es V
assert valid([ningun(0, 1), todos(2, 0)], ningun(2, 1), 3)
assert not valid([ningun(0, 1), todos(2, 0)], todos(0, 2), 3)
assert not valid([ningun(0, 1), todos(2, 0)], algun(2, 1), 3)
# l22: Todos A son L; ningun E es L => ningun A es E
assert valid([todos(0, 1), ningun(2, 1)], ningun(0, 2), 3)
assert not valid([todos(0, 1), ningun(2, 1)], todos(1, 0), 3)
assert not valid([todos(0, 1), ningun(2, 1)], algun(2, 0), 3)

add("l17", B, "silogismos", "facil",
    "<b>Premisa 1:</b> Todos los operadores de camión tienen licencia de conducir categoría A-IIIc.<br><b>Premisa 2:</b> Julio es operador de camión.<br>¿Qué conclusión se deduce?",
    "Julio tiene licencia categoría A-IIIc.",
    ["Todos los que tienen licencia A-IIIc son operadores de camión.", "Julio no tiene licencia A-IIIc.", "Solo Julio tiene licencia A-IIIc."],
    "Si todos los operadores tienen esa licencia y Julio es operador, Julio la tiene. Las demás no se deducen de las premisas.",
    lambda: "Julio tiene licencia categoría A-IIIc.")
add("l18", B, "silogismos", "facil",
    "<b>Premisa 1:</b> Ningún equipo en mantenimiento está operativo.<br><b>Premisa 2:</b> La pala P-03 está en mantenimiento.<br>¿Qué conclusión se deduce?",
    "La pala P-03 no está operativa.",
    ["La pala P-03 está operativa.", "Todos los equipos no operativos están en mantenimiento.", "Ninguna pala está operativa."],
    "Lo que está en mantenimiento no está operativo; P-03 está en mantenimiento, por tanto no está operativa.",
    lambda: "La pala P-03 no está operativa.")
add("l19", B, "silogismos", "media",
    "<b>Premisa 1:</b> Todos los ingenieros de turno usan casco blanco.<br><b>Premisa 2:</b> Algunas personas que usan casco blanco son visitantes.<br>¿Qué conclusión se deduce <i>necesariamente</i>?",
    "No se puede concluir nada seguro sobre la relación entre ingenieros y visitantes.",
    ["Algunos ingenieros de turno son visitantes.", "Ningún ingeniero de turno es visitante.", "Todos los visitantes son ingenieros de turno."],
    "El término medio (usar casco blanco) no se distribuye en ninguna premisa: los visitantes con casco pueden o no coincidir con los ingenieros. Ninguna relación es necesaria.",
    lambda: "No se puede concluir nada seguro sobre la relación entre ingenieros y visitantes.")
add("l20", B, "silogismos", "media",
    "<b>Premisa 1:</b> Todos los supervisores son ingenieros.<br><b>Premisa 2:</b> Algunos supervisores son geólogos.<br>¿Qué conclusión es válida?",
    "Algunos ingenieros son geólogos.",
    ["Todos los ingenieros son geólogos.", "Todos los geólogos son supervisores.", "Algunos ingenieros no son geólogos."],
    "Los supervisores que son geólogos también son ingenieros (premisa 1); por tanto, existen ingenieros que son geólogos.",
    lambda: "Algunos ingenieros son geólogos.")
add("l21", B, "silogismos", "facil",
    "<b>Premisa 1:</b> Ningún practicante ejecuta voladuras.<br><b>Premisa 2:</b> Todos los becarios son practicantes.<br>¿Qué conclusión se deduce?",
    "Ningún becario ejecuta voladuras.",
    ["Algunos becarios ejecutan voladuras.", "Todos los practicantes son becarios.", "Solo los becarios no ejecutan voladuras."],
    "Los becarios están incluidos en los practicantes, y ningún practicante ejecuta voladuras; luego ningún becario lo hace.",
    lambda: "Ningún becario ejecuta voladuras.")
add("l22", B, "silogismos", "dificil",
    "<b>Premisa 1:</b> Todos los camiones autónomos tienen sensor LiDAR.<br><b>Premisa 2:</b> Ningún equipo de modelo antiguo tiene sensor LiDAR.<br>¿Qué conclusión es válida?",
    "Ningún camión autónomo es un equipo de modelo antiguo.",
    ["Algunos equipos de modelo antiguo son camiones autónomos.", "Todos los equipos con LiDAR son camiones autónomos.", "Algunos camiones autónomos no tienen LiDAR.", "No se puede concluir nada."],
    "Si un camión autónomo fuera de modelo antiguo, tendría LiDAR (P1) y no lo tendría (P2): contradicción. Por tanto, ningún camión autónomo es de modelo antiguo.",
    lambda: "Ningún camión autónomo es un equipo de modelo antiguo.")

# Ordenamiento: fuerza bruta con unicidad
def unique(perms, cond):
    sols = [p for p in perms if cond(p)]
    assert len(sols) == 1, sols
    return sols[0]

# l23: ranking produccion (mayor a menor)
sol = unique(itertools.permutations("ABCD"),
             lambda p: p.index("A") < p.index("B") and p.index("C") > p.index("B") and p.index("D") < p.index("A"))
add("l23", B, "ordenamiento", "facil",
    "En un mes, la pala A cargó más toneladas que la pala B; la pala C cargó menos que la B; y la pala D cargó más que la A. ¿Qué pala cargó <b>menos</b> toneladas?",
    "Pala C", ["Pala B", "Pala A", "Pala D"],
    "Orden de mayor a menor: D > A > B > C. La que cargó menos es la C.", lambda: "Pala " + sol[-1])
# l24: fila de 5 asientos (1 izquierda ... 5 derecha)
sol24 = unique(itertools.permutations(["Ana", "Beto", "Carla", "Dante", "Elsa"]),
               lambda p: p[2] == "Carla" and p.index("Ana") == 1 and p[4] == "Beto"
               and abs(p.index("Elsa") - p.index("Beto")) != 1)
add("l24", B, "ordenamiento", "media",
    "Cinco becarios se sientan en una fila de 5 asientos numerados del 1 (extremo izquierdo) al 5 (extremo derecho):<br>• Carla está en el asiento central.<br>• Ana está junto a Carla, a su izquierda.<br>• Beto está en el extremo derecho.<br>• Elsa no está junto a Beto.<br>¿Quién ocupa el asiento 1?",
    "Elsa", ["Dante", "Ana", "Beto"],
    "Carla = 3, Ana = 2, Beto = 5. Quedan 1 y 4 para Dante y Elsa. Elsa no puede estar en 4 (junto a Beto), así que Elsa = 1 y Dante = 4.",
    lambda: sol24[0])
sol25 = unique(itertools.permutations("PQRST"),
               lambda p: p.index("P") < p.index("Q") and p.index("R") < p.index("P") and p.index("S") > p.index("Q") and p.index("T") < p.index("R"))
add("l25", B, "ordenamiento", "facil",
    "En la evaluación de seguridad, Pablo obtuvo más puntos que Quispe pero menos que Ríos. Salas obtuvo menos que Quispe y Torres obtuvo más que Ríos. ¿Quién ocupó el <b>tercer lugar</b>?",
    "Pablo", ["Quispe", "Ríos", "Torres"],
    "Orden de mayor a menor: Torres > Ríos > Pablo > Quispe > Salas. Tercer lugar: Pablo.",
    lambda: {"P": "Pablo", "Q": "Quispe", "R": "Ríos", "S": "Salas", "T": "Torres"}[sol25[2]])
areas = ["Logística", "Seguridad", "Mantenimiento", "RRHH", "Geología"]
def c26(p):  # p[i] = area en piso i+1
    fl = {a: p.index(a) + 1 for a in areas}
    return (fl["Mantenimiento"] == 2 and fl["Logística"] == fl["Geología"] + 1
            and fl["Seguridad"] not in (1, 5) and fl["RRHH"] < fl["Seguridad"])
sol26 = unique(itertools.permutations(areas), c26)
add("l26", B, "ordenamiento", "dificil",
    "Un edificio administrativo tiene 5 pisos (1 = el más bajo) y cada uno lo ocupa un área distinta: Logística, Seguridad, Mantenimiento, RRHH y Geología.<br>• Mantenimiento está en el piso 2.<br>• Logística está inmediatamente encima de Geología.<br>• Seguridad no está ni en el primer ni en el último piso.<br>• RRHH está en un piso más bajo que Seguridad.<br>¿Qué área está en el <b>piso 3</b>?",
    "Seguridad", ["Geología", "RRHH", "Logística"],
    "Geología–Logística deben ser pisos consecutivos sin usar el 2: (3,4) o (4,5). Si fueran 3 y 4, Seguridad quedaría en 1 o 5 (prohibido). Entonces Geología = 4, Logística = 5; quedan 1 y 3: Seguridad = 3 y RRHH = 1 (más bajo que Seguridad).",
    lambda: sol26[2])
names27 = {"N": "Nora", "L": "Luis", "M": "Mario", "O": "Óscar", "P": "Pedro"}
sol27 = unique(itertools.permutations("NLMOP"),
               lambda p: p.index("N") < p.index("L") < p.index("M") and p.index("O") == p.index("M") + 1
               and p.index("N") < p.index("P") < p.index("L"))
add("l27", B, "ordenamiento", "media",
    "Cinco operadores llegan a la charla de seguridad. Nora llegó antes que Luis, y Luis antes que Mario. Óscar llegó inmediatamente después de Mario. Pedro llegó después de Nora pero antes de Luis. ¿Quién llegó en <b>cuarto</b> lugar?",
    "Mario", ["Luis", "Óscar", "Pedro"],
    "Nora < Pedro < Luis < Mario, y Óscar justo después de Mario: Nora, Pedro, Luis, Mario, Óscar. Cuarto: Mario.",
    lambda: names27[sol27[3]])

# Verdad / mentira / deduccion
add("l28", B, "verdad_mentira_o_deduccion", "media",
    "Se sabe que: «<i>Solo los trabajadores que aprobaron la inducción pueden ingresar al tajo.</i>» Rosa ingresó al tajo esta mañana. ¿Qué se deduce con certeza?",
    "Rosa aprobó la inducción.",
    ["Rosa es supervisora.", "Todos los que aprobaron la inducción ingresaron al tajo.", "Rosa no aprobó la inducción."],
    "«Solo los que aprobaron pueden ingresar» equivale a: si ingresa, entonces aprobó. Rosa ingresó, luego aprobó la inducción.",
    lambda: "Rosa aprobó la inducción.")
add("l29", B, "verdad_mentira_o_deduccion", "facil",
    "Carlos es más alto que Diego. Diego es más alto que Eva. ¿Cuál afirmación es <b>necesariamente</b> verdadera?",
    "Carlos es más alto que Eva.", ["Eva es más alta que Carlos.", "Diego es el más alto.", "Eva y Carlos tienen la misma estatura."],
    "Por transitividad: Carlos > Diego > Eva, luego Carlos > Eva.", lambda: "Carlos es más alto que Eva.")
def culprit3():
    sols = []
    for c in "ABC":
        st = [c == "B", c != "B", c != "C"]  # A: fue B; B: yo no fui; C: yo no fui
        if sum(st) == 1: sols.append(c)
    assert len(sols) == 1
    return sols[0]
add("l30", B, "verdad_mentira_o_deduccion", "media",
    "Uno de tres operadores (A, B o C) dejó encendido un equipo al terminar el turno. Al preguntarles:<br>• A: «Fue B».<br>• B: «Yo no fui».<br>• C: «Yo no fui».<br>Si <b>solo uno</b> dice la verdad, ¿quién dejó encendido el equipo?",
    "C", ["A", "B", "No se puede determinar"],
    "Si fue A: B y C dicen verdad (2). Si fue B: A y C dicen verdad (2). Si fue C: solo B dice verdad (1). Por tanto, fue C.",
    lambda: culprit3())
def culprit4():
    sols = []
    for c in "PQRS":
        q_true = (c == "S")
        st = [c == "Q", q_true, c != "R", not q_true]
        if st.count(False) == 1: sols.append(c)
    assert len(sols) == 1
    return sols[0]
add("l31", B, "verdad_mentira_o_deduccion", "dificil",
    "Una de cuatro personas (P, Q, R o S) movió una muestra del laboratorio sin registrarla. Declaran:<br>• P: «Fue Q».<br>• Q: «Fue S».<br>• R: «Yo no fui».<br>• S: «Q miente».<br>Si <b>solo una</b> persona miente, ¿quién movió la muestra?",
    "Q", ["P", "R", "S"],
    "Q y S se contradicen, así que el mentiroso es uno de ellos y P y R dicen la verdad. P dice la verdad → fue Q. Verificación: Q miente (no fue S), S dice verdad, R dice verdad. Exactamente un mentiroso.",
    lambda: culprit4())
add("l32", B, "verdad_mentira_o_deduccion", "media",
    "Regla de la operación: «<i>Si un equipo aprueba la inspección pre-uso, entonces puede operar en el turno.</i>» El cargador CF-12 <b>no</b> puede operar en el turno. ¿Qué se deduce?",
    "El cargador CF-12 no aprobó la inspección pre-uso.",
    ["El cargador CF-12 aprobó la inspección pre-uso.", "Ningún cargador puede operar en el turno.", "Si un equipo no aprueba la inspección, igual puede operar.", "El cargador CF-12 está en mantenimiento correctivo."],
    "Modus tollens: si p → q y no q, entonces no p. Como CF-12 no puede operar, no aprobó la inspección.",
    lambda: "El cargador CF-12 no aprobó la inspección pre-uso.")

# ---------------- ARMADO + VERIFICACION ----------------
rng = random.Random(2026)
out = []
pos_count = Counter()
for it in sorted(items, key=lambda x: (x["area"] != "numerico", x["id"])):
    got = it["check"]()
    assert got == it["correct"], (it["id"], got, it["correct"])
    opts = list(it["distractors"])
    assert it["correct"] not in opts and len(set(opts)) == len(opts), it["id"]
    n = len(opts) + 1
    assert n in (4, 5), it["id"]
    k = rng.randrange(n)
    opts.insert(k, it["correct"])
    pos_count[k] += 1
    out.append(dict(id=it["id"], area=it["area"], subtype=it["subtype"], difficulty=it["difficulty"],
                    prompt=it["prompt"], options=opts, answer=k, explanation=it["explanation"]))

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

# Re-lectura y validacion
data = json.load(open(OUT, encoding="utf-8"))
assert len(data) == 64 and len({d["id"] for d in data}) == 64
for d in data:
    assert 0 <= d["answer"] < len(d["options"])
print("OK", len(data))
print(Counter((d["area"], d["subtype"]) for d in data))
print(Counter((d["area"], d["difficulty"]) for d in data))
print("posiciones respuesta:", sorted(pos_count.items()))
