import json, os, sys

def T(headers, rows, start_row=1, cols="ABCDEFG"):
    """HTML table with Excel-like column letters and row numbers."""
    n = len(headers)
    h = "<table><tr><th></th>" + "".join(f"<th>{cols[i]}</th>" for i in range(n)) + "</tr>"
    h += f"<tr><th>{start_row}</th>" + "".join(f"<td><b>{x}</b></td>" for x in headers) + "</tr>"
    for i, r in enumerate(rows):
        h += f"<tr><th>{start_row+1+i}</th>" + "".join(f"<td>{'' if v is None else v}</td>" for v in r) + "</tr>"
    return h + "</table>"

def fmt(v):
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, int):
        return f"{v:,}".replace(",", " ") if v >= 10000 else str(v)
    return str(v)

items = []
def add(id_, sub, diff, prompt, options, correct, expl):
    options = [fmt(o) for o in options]
    c = fmt(correct)
    assert c in options, (id_, c, options)
    assert len(set(options)) == 4, (id_, options)
    items.append({"id": id_, "area": "excel", "subtype": sub, "difficulty": diff,
                  "prompt": prompt, "options": options, "answer": options.index(c), "explanation": expl})

# ---------- funciones_basicas ----------
turnos = ["Turno A", "Turno B", "Turno C", "Turno D", "Turno E"]
ton = [1250, 980, 1430, 1100, 1240]
tbl = T(["Turno", "Toneladas"], list(zip(turnos, ton)))
s = sum(ton)
add("x01", "funciones_basicas", "facil",
    f"La planta concentradora registra el mineral procesado por turno:<br>{tbl}<br>¿Qué resultado devuelve <code>=SUMA(B2:B6)</code>?",
    [5000, s, 6250, 4570], s,
    f"SUMA (SUM en inglés) suma todos los valores numéricos del rango: 1250+980+1430+1100+1240 = {s}.")
p = sum(ton) / len(ton)
add("x02", "funciones_basicas", "facil",
    f"Con la misma tabla de producción:<br>{tbl}<br>¿Qué devuelve <code>=PROMEDIO(B2:B6)</code>?",
    [1240, 1205, p, 1500], p,
    f"PROMEDIO (AVERAGE) = suma / cantidad de números = {s}/5 = {fmt(p)}. Ojo: no es la mediana (1240).")
r = max(ton) - min(ton)
add("x03", "funciones_basicas", "media",
    f"El supervisor quiere conocer el rango de variación entre turnos:<br>{tbl}<br>¿Qué devuelve <code>=MAX(B2:B6)-MIN(B2:B6)</code>?",
    [r, 330, 1430, 270], r,
    f"MAX (MAX) = 1430 y MIN (MIN) = 980; la diferencia es {r}.")
col = [45, "N/D", 38, None, 52, 41]
contar = sum(isinstance(v, (int, float)) for v in col)
contara = sum(v is not None for v in col)
add("x04", "funciones_basicas", "media",
    f"Viajes por camión en una guardia (B5 está vacía; B3 contiene el texto \"N/D\"):<br>{T(['Camión','Viajes'], [['CM-0'+str(i+1), v] for i, v in enumerate(col)])}<br>¿Qué devuelve <code>=CONTARA(B2:B7)-CONTAR(B2:B7)</code>?",
    [0, contara - contar, 2, 5], contara - contar,
    f"CONTAR (COUNT) cuenta solo celdas numéricas = {contar}. CONTARA (COUNTA) cuenta celdas no vacías, incluido texto = {contara}. Diferencia: {contara-contar} (la celda con \"N/D\").")
vals = [12, None, 18, "pend.", 24]
nums = [v for v in vals if isinstance(v, (int, float))]
pr = sum(nums) / len(nums)
add("x05", "funciones_basicas", "dificil",
    f"Horas de mantenimiento registradas (B3 vacía, B5 con el texto \"pend.\"):<br>{T(['Equipo','Horas'], [[n, v] for n, v in zip(['Chancadora','Faja 1','Molino 1','Faja 2','Celda flot.'], vals)])}<br>¿Qué devuelve <code>=PROMEDIO(B2:B6)</code>?",
    [10.8, pr, 13.5, "#¡VALOR!"], pr,
    f"PROMEDIO (AVERAGE) ignora celdas vacías y texto dentro de un rango: (12+18+24)/3 = {fmt(pr)}. No divide entre 5 ni devuelve error.")

# ---------- condicionales ----------
add("x06", "condicionales", "facil",
    "La meta por turno es 1200 t. En B2 hay <b>1150</b>. ¿Qué devuelve <code>=SI(B2&gt;=1200;\"Meta\";\"Bajo\")</code>?",
    ["Meta", "Bajo", "FALSO", "1150"], "Bajo",
    "SI (IF) evalúa la prueba lógica 1150>=1200, que es FALSO, por lo que devuelve el tercer argumento: \"Bajo\".")
add("x07", "condicionales", "media",
    f"Control de aptitud para ingresar a operación:<br>{T(['Trabajador','Nota inducción','Examen médico'], [['Rojas',92,'No']])}<br>¿Qué devuelve <code>=SI(Y(B2&gt;=90;C2=\"Sí\");\"Apto\";\"No apto\")</code>?",
    ["Apto", "No apto", "VERDADERO", "#¿NOMBRE?"], "No apto",
    "Y (AND) exige que TODAS las condiciones sean verdaderas. B2>=90 es VERDADERO pero C2=\"Sí\" es FALSO, así que Y devuelve FALSO y SI (IF) devuelve \"No apto\".")
add("x08", "condicionales", "media",
    f"Monitoreo de un molino:<br>{T(['Equipo','Temperatura °C','Vibración mm/s'], [['Molino 2',80,9]])}<br>¿Qué devuelve <code>=SI(O(B2&gt;85;C2&gt;8);\"Alerta\";\"Normal\")</code>?",
    ["Normal", "Alerta", "FALSO", "#¡VALOR!"], "Alerta",
    "O (OR) devuelve VERDADERO si al menos una condición se cumple. 80>85 es FALSO, pero 9>8 es VERDADERO, por lo que SI (IF) devuelve \"Alerta\".")
est = ["Operativo", "Mantenimiento", "Operativo", "Standby", "Operativo", "Mantenimiento", "operativo"]
cnt = sum(e.lower() == "operativo" for e in est)
add("x09", "condicionales", "media",
    f"Estado de la flota de camiones:<br>{T(['Camión','Estado'], [['CM-'+str(i+11), e] for i, e in enumerate(est)])}<br>¿Qué devuelve <code>=CONTAR.SI(B2:B8;\"Operativo\")</code>?",
    [3, cnt, 2, 7], cnt,
    f"CONTAR.SI (COUNTIF) cuenta celdas que cumplen el criterio y NO distingue mayúsculas de minúsculas, por eso \"operativo\" (B8) también cuenta: total {cnt}.")
flota = [("CM-01", "CAT 797", 380), ("CM-02", "Komatsu 930", 290), ("CM-03", "CAT 797", 365), ("CM-04", "CAT 793", 240), ("CM-05", "Komatsu 930", 300), ("CM-06", "CAT 797", 372)]
ss = sum(t for _, m, t in flota if m == "CAT 797")
add("x10", "condicionales", "media",
    f"Toneladas acarreadas en la última hora:<br>{T(['Camión','Modelo','Toneladas'], flota)}<br>¿Qué devuelve <code>=SUMAR.SI(B2:B7;\"CAT 797\";C2:C7)</code>?",
    [ss, 1947, 3, 745], ss,
    f"SUMAR.SI (SUMIF) suma C2:C7 solo donde B2:B7 es \"CAT 797\": 380+365+372 = {ss}.")
dias = [980, 1000, 1210, 999, 1450, 1000, 870]
c2 = sum(d >= 1000 for d in dias)
add("x11", "condicionales", "media",
    f"Producción diaria (t) de la semana:<br>{T(['Día','Toneladas'], list(zip(['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'], dias)))}<br>¿Qué devuelve <code>=CONTAR.SI(B2:B8;\"&gt;=1000\")</code>?",
    [2, c2, 5, 3], c2,
    f"El criterio \"&gt;=1000\" incluye los valores iguales a 1000 (Mar y Sáb). Cumplen: 1000, 1210, 1450, 1000 → {c2}. CONTAR.SI = COUNTIF.")
def nested(v):
    return "Óptimo" if v >= 95 else ("Aceptable" if v >= 85 else "Crítico")
add("x12", "condicionales", "dificil",
    "La disponibilidad mecánica de una pala está en B2 = <b>85</b>. ¿Qué devuelve <code>=SI(B2&gt;=95;\"Óptimo\";SI(B2&gt;85;\"Aceptable\";\"Crítico\"))</code>?",
    ["Óptimo", "Aceptable", "Crítico", "FALSO"], "Crítico",
    "SI anidado (nested IF): 85>=95 es FALSO, pasa al segundo SI; 85>85 también es FALSO (es mayor estricto, no mayor o igual), así que devuelve \"Crítico\". Revisa siempre si el límite usa &gt; o &gt;=.")

# ---------- busqueda ----------
eq = [("CM-01", "Camión CAT 797", 363), ("CM-02", "Camión Komatsu 930", 290), ("CM-03", "Camión CAT 793", 227), ("PL-01", "Pala P&amp;H 4100", 109), ("PL-02", "Pala CAT 7495", 98)]
eqt = T(["Código", "Equipo", "Capacidad (t)"], eq)
add("x13", "busqueda", "facil",
    f"Maestro de equipos:<br>{eqt}<br>¿Qué devuelve <code>=BUSCARV(\"CM-03\";A2:C6;3;FALSO)</code>?",
    ["Camión CAT 793", 227, 290, "#N/D"], 227,
    "BUSCARV (VLOOKUP) busca \"CM-03\" en la primera columna del rango, con FALSO exige coincidencia exacta y devuelve la 3.ª columna del rango: 227.")
add("x14", "busqueda", "media",
    f"Con el mismo maestro de equipos:<br>{eqt}<br>¿Qué devuelve <code>=BUSCARV(\"CM-03\";A2:C6;4;FALSO)</code>?",
    ["#N/D", "#¡REF!", "0", "#¡VALOR!"], "#¡REF!",
    "El rango A2:C6 solo tiene 3 columnas; pedir la columna 4 genera #¡REF! (#REF! en inglés). #N/D (#N/A) aparecería si el código no existiera.")
esc = [(0, "0%"), (1000, "2%"), (2000, "5%"), (3000, "8%")]
def aprox(x):
    res = None
    for k, v in esc:
        if k <= x:
            res = v
    return res
add("x15", "busqueda", "dificil",
    f"Tabla de bono por toneladas extra (ordenada ascendente):<br>{T(['Desde (t)','Bono'], esc)}<br>¿Qué devuelve <code>=BUSCARV(2500;A2:B5;2;VERDADERO)</code>?",
    ["8%", "5%", "2%", "#N/D"], aprox(2500),
    "Con VERDADERO, BUSCARV (VLOOKUP) hace coincidencia aproximada: toma el mayor valor menor o igual a 2500, que es 2000, y devuelve 5%. Requiere la primera columna ordenada ascendentemente.")
mol = [("Molino 1", "SAG", 4200), ("Molino 2", "Bolas", 3850), ("Molino 3", "Bolas", 3900), ("Molino 4", "SAG", 4100)]
add("x16", "busqueda", "media",
    f"Tratamiento por molino (t/h):<br>{T(['Equipo','Tipo','t/h'], mol)}<br>¿Qué devuelve <code>=BUSCARX(\"Molino 5\";A2:A5;C2:C5;\"No existe\")</code>?",
    ["#N/D", "No existe", 4100, 0], "No existe",
    "BUSCARX (XLOOKUP) permite un 4.º argumento [si_no_se_encuentra]. Como \"Molino 5\" no está en A2:A5, devuelve \"No existe\" en vez de #N/D.")
op = [("Quispe", "Turno A", 96), ("Mamani", "Turno B", 91), ("Flores", "Turno C", 98), ("Huamán", "Turno A", 94), ("Torres", "Turno B", 89)]
mx = max(op, key=lambda r: r[2])[0]
add("x17", "busqueda", "dificil",
    f"Índice de cumplimiento de checklist preuso por operador:<br>{T(['Operador','Turno','Cumplimiento %'], op)}<br>¿Qué devuelve <code>=INDICE(A2:A6;COINCIDIR(MAX(C2:C6);C2:C6;0))</code>?",
    ["Quispe", mx, 98, 3], mx,
    "MAX (MAX) da 98; COINCIDIR (MATCH) con 0 encuentra su posición exacta (3) dentro de C2:C6; INDICE (INDEX) devuelve el 3.º elemento de A2:A6: \"Flores\". INDICE/COINCIDIR puede buscar hacia la izquierda, a diferencia de BUSCARV.")

# ---------- referencias ----------
add("x18", "referencias", "facil",
    "En C2 está <code>=B2*$E$1</code> (E1 contiene la ley de cobre). Si copias C2 hasta C5, ¿qué fórmula queda en C5?",
    ["=B5*$E$1", "=B5*$E$4", "=B2*$E$1", "=E5*$B$1"], "=B5*$E$1",
    "B2 es referencia relativa: al bajar 3 filas pasa a B5. $E$1 es absoluta (fija columna y fila), no cambia.")
add("x19", "referencias", "dificil",
    "En C3 está <code>=$A3*B$1</code>. Copias C3 y la pegas en D5. ¿Qué fórmula queda en D5?",
    ["=$A5*C$1", "=$A5*B$1", "=$B5*C$1", "=$A3*C$3"], "=$A5*C$1",
    "Se desplaza +1 columna y +2 filas. En $A3 la columna está fija y la fila es relativa → $A5. En B$1 la fila está fija y la columna es relativa → C$1. Son referencias mixtas.")
add("x20", "referencias", "media",
    "En B4 está <code>=SUMA(A1:A3)</code>. Si copias B4 a C6, ¿qué fórmula queda en C6?",
    ["=SUMA(A1:A3)", "=SUMA(B3:B5)", "=SUMA(B1:B3)", "=SUMA(A3:A5)"], "=SUMA(B3:B5)",
    "Todo el rango es relativo: +1 columna y +2 filas, así que A1:A3 se convierte en B3:B5. SUMA = SUM.")
add("x21", "referencias", "media",
    "Escribes <code>=A1</code> y, con el cursor sobre la referencia, presionas <b>F4</b> dos veces. ¿Qué referencia obtienes?",
    ["$A$1", "A$1", "$A1", "A1"], "A$1",
    "F4 rota: A1 → $A$1 (1.ª vez) → A$1 (2.ª, fila fija) → $A1 (3.ª, columna fija) → A1 (4.ª).")

# ---------- formato_datos ----------
add("x22", "formato_datos", "facil",
    "Tienes 5 000 filas con fecha, turno, guardia, equipo y toneladas. Necesitas un resumen de toneladas totales por turno y por mes que puedas reorganizar rápido. ¿Qué herramienta es la más adecuada?",
    ["Formato condicional", "Tabla dinámica", "Validación de datos", "Ordenar de A a Z"], "Tabla dinámica",
    "La tabla dinámica (PivotTable) agrupa y resume (suma, cuenta, promedia) grandes volúmenes por varias dimensiones y se reorganiza arrastrando campos.")
add("x23", "formato_datos", "media",
    "En un registro de inspecciones quieres que la columna \"Turno\" solo acepte \"Día\" o \"Noche\" mediante una lista desplegable. ¿Qué usas?",
    ["Datos &gt; Validación de datos &gt; Lista", "Inicio &gt; Formato condicional", "Datos &gt; Quitar duplicados", "Insertar &gt; Segmentación de datos"], "Datos &gt; Validación de datos &gt; Lista",
    "La validación de datos (Data Validation) con tipo Lista restringe la entrada a valores permitidos y muestra una lista desplegable, evitando errores de digitación.")
fil = [("Lun", "Día", 600), ("Lun", "Noche", 550), ("Mar", "Día", 620), ("Mar", "Noche", 580)]
vis = sum(t for _, g, t in fil if g == "Día")
add("x24", "formato_datos", "dificil",
    f"Aplicas un Autofiltro para mostrar solo la guardia \"Día\":<br>{T(['Día','Guardia','Toneladas'], fil)}<br>¿Qué fórmula devuelve <b>{vis}</b> (solo las filas visibles)?",
    ["=SUMA(C2:C5)", "=SUBTOTALES(9;C2:C5)", "=CONTAR(C2:C5)", "=SUMAR(C2:C5)"], "=SUBTOTALES(9;C2:C5)",
    f"SUBTOTALES (SUBTOTAL) con función 9 (suma) ignora las filas ocultas por un filtro: 600+620 = {vis}. SUMA (SUM) sumaría todas ({sum(t for *_, t in fil)}). \"SUMAR\" no existe.")
add("x25", "formato_datos", "dificil",
    "Quieres resaltar en rojo TODA la fila (A2:F100) cuando la disponibilidad en la columna D sea menor a 85%. En Formato condicional &gt; Usar una fórmula, seleccionando A2:F100, ¿qué fórmula escribes?",
    ["=$D2&lt;0,85", "=D2&lt;0,85", "=$D$2&lt;0,85", "=D$2&lt;0,85"], "=$D2&lt;0,85",
    "Hay que fijar la columna D ($D) para que todas las celdas de la fila miren la disponibilidad, y dejar la fila relativa (2) para que cada fila se evalúe a sí misma. $D$2 aplicaría la fila 2 a todo el rango. (En Excel en español el decimal es coma: 0,85.)")

# ---------- graficos ----------
add("x26", "graficos", "facil",
    "Debes mostrar la evolución mensual de la producción de cobre fino durante los últimos 12 meses. ¿Qué gráfico es el más adecuado?",
    ["Circular", "Líneas", "Dispersión", "Radial"], "Líneas",
    "El gráfico de líneas (Line chart) muestra tendencias en el tiempo con categorías ordenadas (meses). El circular sirve para partes de un todo.")
add("x27", "graficos", "media",
    "Quieres analizar si existe relación entre la dureza del mineral (eje X) y el consumo de energía del molino en kWh/t (eje Y) para 200 muestras. ¿Qué gráfico usas?",
    ["Columnas agrupadas", "Circular", "Dispersión (XY)", "Áreas apiladas"], "Dispersión (XY)",
    "El gráfico de dispersión (Scatter chart) muestra la relación entre dos variables numéricas; permite añadir línea de tendencia y R².")
add("x28", "graficos", "dificil",
    "Tienes las horas de parada de la planta por causa (falla eléctrica, atoro de chute, cambio de liners, etc.) y quieres identificar el 20% de causas que generan ~80% de las horas perdidas. ¿Qué gráfico es el más útil?",
    ["Pareto (columnas ordenadas + línea acumulada)", "Circular 3D", "Líneas con marcadores", "Anillo"], "Pareto (columnas ordenadas + línea acumulada)",
    "El diagrama de Pareto (Pareto chart, en Excel: Histograma &gt; Pareto) ordena causas de mayor a menor y añade el porcentaje acumulado, ideal para priorizar acciones de mejora.")

# rotate answer positions for variety (deterministic shuffle keeping verified correct)
import random
rng = random.Random(7)
for it in items:
    correct = it["options"][it["answer"]]
    opts = it["options"][:]
    rng.shuffle(opts)
    it["options"] = opts
    it["answer"] = opts.index(correct)

json.dump(items, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(len(items), [it["answer"] for it in items])
