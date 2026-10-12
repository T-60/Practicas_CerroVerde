#!/usr/bin/env python3
"""Genera banco de preguntas de razonamiento espacial (30 items) con SVG exactos."""
import json, math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "banco", "espacial.json")
RNG = random.Random(20261009)
A = 'var(--fig-a)'
B = 'var(--fig-b)'


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" '
            f'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" '
            f'stroke-linecap="round">{body}</svg>')


def fmt(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else str(v)


def pts(p):
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in p)


def text(x, y, s, size=16, weight="bold"):
    return (f'<text x="{fmt(x)}" y="{fmt(y)}" fill="currentColor" stroke="none" '
            f'font-family="sans-serif" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle" dominant-baseline="central">{s}</text>')


def shuffle_options(opts, correct_idx):
    """opts: list of (key, rendered). returns rendered list and new answer index."""
    order = list(range(len(opts)))
    RNG.shuffle(order)
    keys = [opts[i][0] for i in order]
    assert len(set(keys)) == len(keys), f"opciones repetidas: {keys}"
    return [opts[i][1] for i in order], order.index(correct_idx)


ITEMS = []


def add(subtype, diff, prompt, figure, opts, correct_idx, expl):
    rendered, ans = shuffle_options(opts, correct_idx)
    ITEMS.append({
        "id": f"e{len(ITEMS)+1:02d}", "area": "espacial", "subtype": subtype,
        "difficulty": diff, "prompt": prompt, "figure": figure,
        "options": rendered, "answer": ans, "explanation": expl,
    })

# ---------------------------------------------------------------- conteo cubos
C30 = math.cos(math.radians(30))


def iso_svg(H, s=26):
    X, Y = len(H), len(H[0])
    for x in range(X):
        for y in range(Y):
            if x + 1 < X:
                assert H[x][y] >= H[x+1][y], "no monotona"
            if y + 1 < Y:
                assert H[x][y] >= H[x][y+1], "no monotona"
    P = lambda x, y, z: ((x - y) * C30 * s, (x + y) * 0.5 * s - z * s)
    maxz = max(max(r) for r in H)
    allp = [P(x, y, z) for x in (0, X) for y in (0, Y) for z in (0, maxz)]
    minx = min(p[0] for p in allp) - 8
    miny = min(p[1] for p in allp) - 8
    maxx = max(p[0] for p in allp) + 8
    maxy = max(p[1] for p in allp) + 8
    T = lambda p: (p[0] - minx, p[1] - miny)
    Q = lambda x, y, z: T(P(x, y, z))
    body = []
    # piso con cuadricula punteada
    for i in range(X + 1):
        body.append(f'<line x1="{fmt(Q(i,0,0)[0])}" y1="{fmt(Q(i,0,0)[1])}" x2="{fmt(Q(i,Y,0)[0])}" y2="{fmt(Q(i,Y,0)[1])}" stroke-width="1" stroke-dasharray="3 3"/>')
    for j in range(Y + 1):
        body.append(f'<line x1="{fmt(Q(0,j,0)[0])}" y1="{fmt(Q(0,j,0)[1])}" x2="{fmt(Q(X,j,0)[0])}" y2="{fmt(Q(X,j,0)[1])}" stroke-width="1" stroke-dasharray="3 3"/>')
    cubes = [(x, y, z) for x in range(X) for y in range(Y) for z in range(H[x][y])]
    cubes.sort(key=lambda c: (c[0] + c[1] + c[2], c[2]))
    for x, y, z in cubes:
        top = [Q(x, y, z+1), Q(x+1, y, z+1), Q(x+1, y+1, z+1), Q(x, y+1, z+1)]
        right = [Q(x+1, y, z), Q(x+1, y+1, z), Q(x+1, y+1, z+1), Q(x+1, y, z+1)]
        left = [Q(x, y+1, z), Q(x+1, y+1, z), Q(x+1, y+1, z+1), Q(x, y+1, z+1)]
        body.append(f'<polygon points="{pts(left)}" fill="{B}"/>')
        body.append(f'<polygon points="{pts(right)}" fill="{B}"/>')
        body.append(f'<polygon points="{pts(right)}" fill="currentColor" fill-opacity="0.3" stroke="none"/>')
        body.append(f'<polygon points="{pts(right)}"/>')
        body.append(f'<polygon points="{pts(top)}" fill="{A}"/>')
    return svg(maxx - minx, maxy - miny, "".join(body))


SUPUESTO = ("Supón que no hay huecos: todo cubo que no se ve está debajo de otro, "
            "sosteniendo a los que están encima.")


def count_item(H, diff, mode="total", target=None):
    total = sum(map(sum, H))
    fig = iso_svg(H)
    if mode == "total":
        ans = total
        prompt = f"¿Cuántos cubos forman la pila? {SUPUESTO}"
        rows = "; ".join("-".join(str(v) for v in r) for r in H)
        expl = (f"Cuenta columna por columna (altura de cada posición sobre el piso). "
                f"Alturas por filas, del fondo al frente: {rows}. Suma = {total} cubos.")
    else:
        X, Y, Z = target
        ans = X * Y * Z - total
        prompt = (f"¿Cuántos cubos como mínimo faltan para completar un bloque macizo de "
                  f"{X}×{Y}×{Z}? {SUPUESTO}")
        expl = (f"El bloque completo tiene {X}×{Y}×{Z} = {X*Y*Z} cubos. La pila tiene "
                f"{total} (suma de alturas por columna). Faltan {X*Y*Z} − {total} = {ans}.")
    deltas = RNG.sample([-3, -2, -1, 1, 2, 3], 3)
    opts = [(ans, str(ans))] + [(ans + d, str(ans + d)) for d in deltas]
    add("conteo_cubos", diff, prompt, fig, opts, 0, expl)


count_item([[3, 2], [2, 1]], "facil")
count_item([[3, 2, 1], [2, 1, 1], [1, 1, 0]], "facil")
count_item([[3, 3, 2], [3, 2, 1], [2, 1, 1]], "media")
count_item([[4, 3, 2, 1], [3, 2, 2, 1], [2, 1, 1, 0]], "media")
count_item([[4, 4, 3, 2], [4, 3, 2, 1], [3, 2, 2, 1], [2, 1, 1, 0]], "dificil")
count_item([[3, 3, 2], [3, 2, 1], [2, 1, 0]], "dificil", mode="faltan", target=(3, 3, 3))

# ---------------------------------------------------------- figuras rot/espejo
TR = {
    "id": lambda x, y: (x, y),
    "r90": lambda x, y: (-y, x),      # horario (pantalla, y hacia abajo)
    "r180": lambda x, y: (-x, -y),
    "r270": lambda x, y: (y, -x),     # antihorario 90
    "mv": lambda x, y: (-x, y),       # espejo eje vertical
    "mh": lambda x, y: (x, -y),       # espejo eje horizontal
}


def compose(*names):
    def f(x, y):
        for n in names:
            x, y = TR[n](x, y)
        return x, y
    return f


class Fig:
    def __init__(self, cells=(), tris=(), dots=(), segs=(), frame=None):
        self.cells = [(x + .5, y + .5) for x, y in cells]  # centros
        self.tris = [list(t) for t in tris]
        self.dots = list(dots)
        self.segs = [list(s) for s in segs]
        self.frame = frame  # tamaño n (marco n x n) o None

    def allpts(self):
        p = []
        for cx, cy in self.cells:
            p += [(cx - .5, cy - .5), (cx + .5, cy + .5)]
        for t in self.tris:
            p += t
        p += self.dots
        for s in self.segs:
            p += s
        return p

    def apply(self, f):
        g = Fig(frame=self.frame)
        if self.frame:
            c = self.frame / 2
            ff = lambda p: tuple(v + c for v in f(p[0] - c, p[1] - c))
        else:
            ff = lambda p: f(*p)
        g.cells = [ff(p) for p in self.cells]
        g.tris = [[ff(p) for p in t] for t in self.tris]
        g.dots = [ff(p) for p in self.dots]
        g.segs = [[ff(p) for p in s] for s in self.segs]
        if not self.frame:
            ap = g.allpts()
            mx, my = min(p[0] for p in ap), min(p[1] for p in ap)
            sh = lambda p: (p[0] - mx, p[1] - my)
            g.cells = [sh(p) for p in g.cells]
            g.tris = [[sh(p) for p in t] for t in g.tris]
            g.dots = [sh(p) for p in g.dots]
            g.segs = [[sh(p) for p in s] for s in g.segs]
        return g

    def key(self):
        r = lambda p: (round(p[0], 4) + 0.0, round(p[1], 4) + 0.0)
        return (tuple(sorted(r(p) for p in self.cells)),
                tuple(sorted(tuple(sorted(r(p) for p in t)) for t in self.tris)),
                tuple(sorted(r(p) for p in self.dots)),
                tuple(sorted(tuple(sorted(r(p) for p in s)) for s in self.segs)))

    def size(self):
        if self.frame:
            return self.frame, self.frame
        ap = self.allpts()
        return max(p[0] for p in ap), max(p[1] for p in ap)

    def body(self, k, ox, oy):
        T = lambda p: (ox + p[0] * k, oy + p[1] * k)
        b = []
        if self.frame:
            n = self.frame
            b.append(f'<rect x="{fmt(ox)}" y="{fmt(oy)}" width="{fmt(n*k)}" height="{fmt(n*k)}" fill="{A}"/>')
            for i in range(n + 1):
                for j in range(n + 1):
                    x, y = T((i, j))
                    b.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="2.5" fill="{B}" stroke="none"/>')
        for cx, cy in self.cells:
            x, y = T((cx - .5, cy - .5))
            b.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(k)}" height="{fmt(k)}" fill="{A}"/>')
        for s in self.segs:
            (x1, y1), (x2, y2) = T(s[0]), T(s[1])
            b.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
        for t in self.tris:
            b.append(f'<polygon points="{pts([T(p) for p in t])}" fill="currentColor"/>')
        for d in self.dots:
            x, y = T(d)
            b.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(k*0.16)}" fill="currentColor" stroke="none"/>')
        return b

    def render(self, box=110, unit=None):
        w, h = self.size()
        k = unit or min((box - 16) / w, (box - 16) / h, 26)
        ox, oy = (box - w * k) / 2, (box - h * k) / 2
        return svg(box, box, "".join(self.body(k, ox, oy)))


def tri_in(cx, cy, d):
    """triángulo dentro de la celda (cx,cy esquina sup-izq) apuntando d."""
    c = (cx + .5, cy + .5)
    v = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}[d]
    n = (-v[1], v[0])
    tip = (c[0] + v[0] * .32, c[1] + v[1] * .32)
    b1 = (c[0] - v[0] * .25 + n[0] * .28, c[1] - v[1] * .25 + n[1] * .28)
    b2 = (c[0] - v[0] * .25 - n[0] * .28, c[1] - v[1] * .25 - n[1] * .28)
    return [tip, b1, b2]


NOMBRE = {"r90": "rotación de 90° en sentido horario",
          "r270": "rotación de 90° en sentido antihorario",
          "r180": "rotación de 180°",
          "mv": "reflejo respecto a un eje vertical",
          "mh": "reflejo respecto a un eje horizontal",
          "id": "la figura original sin cambios"}


def transform_item(subtype, diff, fig, prompt, correct, distract, expl, main=None):
    names = [correct] + distract
    figs = [fig.apply(compose(*n.split("+"))) for n in names]
    keys = [f.key() for f in figs]
    assert len(set(keys)) == len(keys), f"transformaciones no distinguibles {names}"
    # evitar que alguna opción coincida con la figura original salvo que sea intencional
    box = 110
    # misma escala para todas
    sizes = [f.size() for f in figs] + [fig.size()]
    mx = max(max(s) for s in sizes)
    unit = min((box - 16) / mx, 26)
    opts = [(keys[i], figs[i].render(box, unit)) for i in range(len(figs))]
    figure = main if main is not None else fig.render(140, unit)
    add(subtype, diff, prompt, figure, opts, 0, expl)


def mirror_main(fig, axis):
    """figura con eje de espejo punteado al lado."""
    w, h = fig.size()
    k = min(80 / max(w, h), 26)
    pad = 14
    if axis == "v":
        W, Hh = w * k + 2 * pad + 40, h * k + 2 * pad
        b = fig.body(k, pad, pad)
        ax = w * k + pad + 20
        b.append(f'<line x1="{fmt(ax)}" y1="4" x2="{fmt(ax)}" y2="{fmt(Hh-4)}" stroke-dasharray="6 4"/>')
    else:
        W, Hh = w * k + 2 * pad, h * k + 2 * pad + 40
        b = fig.body(k, pad, pad)
        ay = h * k + pad + 20
        b.append(f'<line x1="4" y1="{fmt(ay)}" x2="{fmt(W-4)}" y2="{fmt(ay)}" stroke-dasharray="6 4"/>')
    return svg(W, Hh, "".join(b))


# --- rotacion
f1 = Fig(cells=[(0, 0), (0, 1), (0, 2), (1, 2)], tris=[tri_in(0, 0, "R")])
transform_item("rotacion", "facil", f1,
               "¿Cuál de las opciones muestra la figura girada 90° en sentido horario?",
               "r90", ["r270", "mv", "r180"],
               "Al girar 90° horario, lo que estaba arriba pasa a la derecha y la flecha que apuntaba a la derecha ahora apunta hacia abajo. Las demás son un giro antihorario, un giro de 180° y un reflejo.")

f2 = Fig(cells=[(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)], dots=[(2.5, 0.5)], tris=[tri_in(1, 2, "D")])
transform_item("rotacion", "media", f2,
               "¿Cuál de las opciones es la figura girada 180°?",
               "r180", ["mh", "mv", "r90"],
               "Un giro de 180° equivale a voltear arriba-abajo Y derecha-izquierda a la vez: el punto (arriba a la derecha) queda abajo a la izquierda y la flecha que apuntaba abajo apunta arriba. Los reflejos solo invierten una de las dos direcciones.")

f3 = Fig(cells=[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)], tris=[tri_in(0, 0, "D")])
transform_item("rotacion", "media", f3,
               "Tres de las opciones son la misma figura girada. ¿Cuál NO se puede obtener girando la figura (es un reflejo)?",
               "mv", ["r90", "r180", "r270"],
               "Las opciones correctas por giro conservan el orden relativo de la flecha respecto a la forma. La figura reflejada (espejo) invierte ese orden y ningún giro la puede producir.")

f4 = Fig(cells=[(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (2, 2)],
         tris=[tri_in(0, 0, "U")], dots=[(2.5, 2.5)])
transform_item("rotacion", "dificil", f4,
               "¿Cuál de las opciones muestra la figura girada 90° en sentido ANTIHORARIO?",
               "r270", ["r90", "mh", "mv+r270"],
               "En un giro antihorario de 90°, la derecha pasa arriba y lo de arriba pasa a la izquierda: la flecha que apuntaba arriba ahora apunta a la izquierda y el punto (abajo) queda a la derecha. Una opción es el giro horario y las otras son reflejos.")

f5 = Fig(cells=[(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
         tris=[tri_in(0, 1, "L")])
transform_item("rotacion", "dificil", f5,
               "Tres opciones son giros de la figura. ¿Cuál es un reflejo (imagen de espejo) y NO un giro?",
               "mh+r90", ["r90", "r180", "r270"],
               "Ojo: la opción reflejada además está girada para despistar. Para detectarla, recorre la figura en sentido horario desde la flecha: en los giros el orden de las celdas se mantiene; en el reflejo aparece invertido.")

f6 = Fig(frame=3, segs=[[(0, 0), (1, 1)], [(1, 1), (3, 1)], [(2, 1), (2, 3)]], dots=[(0.5, 2.5)])
transform_item("rotacion", "media", f6,
               "La figura está dibujada en un marco cuadrado. ¿Cuál opción muestra la figura girada 90° en sentido horario?",
               "r90", ["r270", "mv", "mh"],
               "Gira todo el marco 90° horario: la esquina superior izquierda pasa a ser la superior derecha y la inferior izquierda pasa a la superior izquierda. Así el punto (abajo-izquierda) queda arriba-izquierda.")

# --- espejo
m1 = Fig(cells=[(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)], tris=[tri_in(0, 0, "R")])
transform_item("espejo", "facil", m1,
               "¿Cuál es la imagen de la figura en un espejo colocado en la línea punteada vertical?",
               "mv", ["mh", "r180", "id"],
               "Con un espejo vertical se invierte izquierda-derecha y se conserva arriba-abajo: la celda con flecha pasa a la esquina superior derecha y la flecha apunta a la izquierda.",
               main=mirror_main(m1, "v"))

m2 = Fig(cells=[(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], tris=[tri_in(2, 2, "R")], dots=[(0.5, 0.5)])
transform_item("espejo", "media", m2,
               "La línea punteada es la superficie de un lago. ¿Cuál es el reflejo de la figura en el agua?",
               "mh", ["mv", "r180", "r90"],
               "Un reflejo en el agua (eje horizontal) invierte arriba-abajo y conserva izquierda-derecha: el punto pasa abajo a la izquierda y la flecha sigue apuntando a la derecha, ahora en la fila superior.",
               main=mirror_main(m2, "h"))

m3 = Fig(frame=3, segs=[[(0, 3), (0, 1)], [(0, 1), (2, 0)], [(1, 2), (3, 2)]], dots=[(2.5, 0.5)])
transform_item("espejo", "media", m3,
               "¿Cuál es la imagen especular de la figura respecto a la línea punteada vertical?",
               "mv", ["mh", "r180", "r90"],
               "Refleja cada punto a la misma distancia del eje, del otro lado: el trazo pegado al borde izquierdo pasa al borde derecho y el punto de arriba-derecha pasa a arriba-izquierda. Arriba y abajo no cambian.",
               main=mirror_main(m3, "v"))

m4 = Fig(frame=3, segs=[[(0, 0), (3, 3)], [(1, 0), (1, 2)], [(1, 2), (2, 2)]], dots=[(0.5, 2.5)], tris=[])
transform_item("espejo", "dificil", m4,
               "¿Cuál es la imagen especular de la figura respecto a la línea punteada horizontal?",
               "mh", ["mv", "r180", "r270"],
               "Con eje horizontal se invierte arriba-abajo: la diagonal que bajaba de izquierda a derecha ahora sube, el trazo vertical cuelga desde abajo y el punto pasa de abajo-izquierda a arriba-izquierda. El giro de 180° también invierte izquierda-derecha, por eso no sirve.",
               main=mirror_main(m4, "h"))

# ------------------------------------------------------------- desarrollos cubo


def fold(cells):
    """cells: lista de (x,y). Devuelve dict celda->normal o None si no forma cubo."""
    cells = list(cells)
    if len(cells) != 6:
        return None
    cs = set(cells)
    start = cells[0]
    state = {start: ((0, 0, -1), (1, 0, 0), (0, 1, 0))}
    queue = [start]
    neg = lambda v: tuple(-a for a in v)
    while queue:
        c = queue.pop(0)
        n, u, v = state[c]
        for d, nb in (("+x", (c[0]+1, c[1])), ("-x", (c[0]-1, c[1])),
                      ("+y", (c[0], c[1]+1)), ("-y", (c[0], c[1]-1))):
            if nb in cs and nb not in state:
                if d == "+x":
                    st = (u, neg(n), v)
                elif d == "-x":
                    st = (neg(u), n, v)
                elif d == "+y":
                    st = (v, u, neg(n))
                else:
                    st = (neg(v), u, n)
                state[nb] = st
                queue.append(nb)
    if len(state) != 6:
        return None
    normals = {c: state[c][0] for c in cells}
    if len(set(normals.values())) != 6:
        return None
    return normals


def opposites(net):
    """net: dict (x,y)->letra."""
    nm = fold(net.keys())
    assert nm is not None, "desarrollo inválido"
    inv = {v: net[c] for c, v in nm.items()}
    res = {}
    for c, v in nm.items():
        res[net[c]] = inv[tuple(-a for a in v)]
    return res


def net_svg(cells, labels=None, k=34, box=None):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    w, h = (max(xs) + 1) * k, (max(ys) + 1) * k
    pad = 6
    W, H = (box, box) if box else (w + 2 * pad, h + 2 * pad)
    ox, oy = (W - w) / 2, (H - h) / 2
    b = []
    for c in cells:
        x, y = ox + c[0] * k, oy + c[1] * k
        b.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{k}" height="{k}" fill="{A}"/>')
        if labels:
            b.append(text(x + k / 2, y + k / 2, labels[c], size=k * 0.5))
    return svg(W, H, "".join(b))


def parse_net(rows):
    net = {}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                net[(x, y)] = ch
    return net


def pares(op):
    seen, out = set(), []
    for a in sorted(op):
        if a not in seen:
            out.append(f"{a}–{op[a]}")
            seen |= {a, op[a]}
    return ", ".join(out)


def opposite_item(rows, ask, diff, extra):
    net = parse_net(rows)
    op = opposites(net)
    ans = op[ask]
    others = [l for l in sorted(op) if l not in (ask, ans)]
    distract = RNG.sample(others, 3)
    opts = [(ans, ans)] + [(d, d) for d in distract]
    for d in distract:  # verificación: distractores son adyacentes
        assert op[ask] != d
    add("desarrollo_cubo", diff,
        f"Al plegar este desarrollo para formar un cubo, ¿qué cara queda OPUESTA a la cara {ask}?",
        net_svg(list(net), net), opts, 0,
        f"{extra} Pares opuestos al plegar: {pares(op)}. Por tanto, opuesta a {ask} está {ans}.")


opposite_item([".A..", "BCDE", ".F.."], "B", "facil",
              "En un desarrollo en cruz, dos caras de la misma fila separadas por una cara intermedia quedan opuestas.")
opposite_item(["AB..", ".CDE", "...F"], "B", "media",
              "Toma C como base: en la fila C-D-E, C y E quedan opuestas (base y tapa). B se levanta como pared trasera y F, al colgar de la tapa E, cae como pared delantera; A queda a la izquierda, frente a D.")
opposite_item(["PQ..", ".RS.", "..TU"], "Q", "dificil",
              "En un desarrollo en escalera (2-2-2), cada cara es opuesta a la que está tres pasos más adelante en el recorrido P→Q→R→S→T→U.")

# validos / invalidos
VALID_SHAPES = {
    "v1": ["X...", "XXXX", "..X."],
    "v2": ["XX..", ".XXX", "...X"],
    "v4": [".X.", "XXX", ".X.", ".X."],
    "v5": ["XX..", ".XX.", "..XX"],
}
INVALID_SHAPES = {
    "i1": ["XXX", "XXX"],
    "i2": ["XXXXX", "..X.."],
    "i3": ["XXXX", "X..X"],
    "i4": ["XX", "XX", "X.", "X."],
    "i5": ["XXX.", "..XX", "..X."],
}


def shape_cells(rows):
    return sorted(parse_net(rows).keys())


def check_shapes():
    for k, r in VALID_SHAPES.items():
        cs = shape_cells(r)
        if len(cs) == 6:
            assert fold(cs) is not None, f"{k} debía ser válido"
    for k, r in INVALID_SHAPES.items():
        assert fold(shape_cells(r)) is None, f"{k} debía ser inválido"


check_shapes()


def shape_opt(rows):
    cs = shape_cells(rows)
    return (tuple(cs), net_svg(cs, k=22, box=110))


def validity_item(diff, valid_keys, invalid_keys, want_valid):
    if want_valid:
        corr = [VALID_SHAPES[valid_keys[0]]]
        dis = [INVALID_SHAPES[k] for k in invalid_keys]
        prompt = "¿Cuál de estos desarrollos SÍ se puede plegar para formar un cubo cerrado?"
        expl = ("Las demás fallan: un bloque de 2×3 (o un cuadrado 2×2 dentro del desarrollo) superpone caras, "
                "una fila de 5 cuadrados da la vuelta y se tapa a sí misma, y dos cuadrados del mismo lado en los extremos "
                "de una fila de 4 caen sobre la misma cara. La opción correcta tiene 4 caras en fila con una cara a cada lado, sin superposiciones.")
    else:
        corr = [INVALID_SHAPES[invalid_keys[0]]]
        dis = [VALID_SHAPES[k] for k in valid_keys]
        prompt = "Tres de estos desarrollos forman un cubo al plegarse. ¿Cuál NO forma un cubo?"
        expl = ("En la opción correcta, al plegar, dos cuadrados terminan ocupando la misma cara del cubo "
                "(se superponen) y otra cara queda abierta. Las otras tres son desarrollos válidos de cubo (escalera, 1-4-1 y 2-3-1).")
    for r in corr + dis:
        assert len(shape_cells(r)) == 6
    opts = [shape_opt(r) for r in corr + dis]
    add("desarrollo_cubo", diff, prompt, "", opts, 0, expl)


validity_item("media", ["v1"], ["i1", "i2", "i3"], True)
validity_item("media", ["v5", "v4", "v2"], ["i5"], False)


def corner_item(rows, diff):
    net = parse_net(rows)
    op = opposites(net)
    letters = sorted(op)
    from itertools import combinations
    good, bad = [], []
    for t in combinations(letters, 3):
        ok = all(op[a] != b for a in t for b in t if a != b)
        (good if ok else bad).append(t)
    g = RNG.choice(good)
    bads = RNG.sample(bad, 3)
    opts = [(g, ", ".join(g))] + [(b, ", ".join(b)) for b in bads]
    add("desarrollo_cubo", diff,
        "Al plegar este desarrollo en un cubo, ¿cuáles tres caras se tocan en una misma esquina (vértice)?",
        net_svg(list(net), net), opts, 0,
        f"Tres caras comparten un vértice solo si ninguna es opuesta a otra. Pares opuestos: {pares(op)}. "
        f"Solo {', '.join(g)} no contiene ningún par opuesto; cada una de las otras opciones incluye un par opuesto.")


corner_item(["M...", "NOP.", "..QR"], "dificil")
# verificación extra del item corner: valida el desarrollo
assert fold(parse_net(["M...", "NOP.", "..QR"]).keys()) is not None

# ----------------------------------------------------------------- series
PANEL = 80


def frame_rect():
    return f'<rect x="2" y="2" width="{PANEL-4}" height="{PANEL-4}" rx="4" fill="none"/>'


def series_main(bodies):
    gap = 10
    n = len(bodies) + 1
    W = n * PANEL + (n - 1) * gap
    out = []
    for i, b in enumerate(bodies + [None]):
        x = i * (PANEL + gap)
        if b is None:
            out.append(f'<g transform="translate({x},0)"><rect x="2" y="2" width="{PANEL-4}" height="{PANEL-4}" rx="4" stroke-dasharray="5 4"/>{text(40, 40, "?", 30)}</g>')
        else:
            out.append(f'<g transform="translate({x},0)">{frame_rect()}{b}</g>')
    return svg(W, PANEL, "".join(out))


def panel(b):
    return svg(PANEL, PANEL, frame_rect() + b)


def series_item(diff, prompt, params, draw, answer_params, distract_params, expl):
    fig = series_main([draw(p) for p in params])
    opts = [(tuple(answer_params), panel(draw(answer_params)))] + \
           [(tuple(d), panel(draw(d))) for d in distract_params]
    add("series_figuras", diff, prompt, fig, opts, 0, expl)


CORN = [(17, 17), (63, 17), (63, 63), (17, 63)]
MIDS = [(40, 17), (63, 40), (40, 63), (17, 40)]


def draw_s1(p):
    b, w = p
    (bx, by), (wx, wy) = CORN[b % 4], MIDS[w % 4]
    return (f'<circle cx="{bx}" cy="{by}" r="8" fill="currentColor" stroke="none"/>'
            f'<circle cx="{wx}" cy="{wy}" r="8" fill="none"/>')


seq = [((k) % 4, (2 - k) % 4) for k in range(5)]
series_item("media", "¿Qué figura continúa la serie?", seq[:4], draw_s1, seq[4],
            [(1, 2), (0, 0), (3, 2)],
            "El círculo negro avanza una esquina en sentido horario en cada paso; el círculo blanco avanza un punto medio de lado en sentido antihorario. Tras la 4.ª figura, el negro vuelve a la esquina superior izquierda y el blanco queda en el lado inferior.")


def reg_poly(n, cx=40, cy=42, r=26):
    return [(cx + r * math.sin(2 * math.pi * i / n), cy - r * math.cos(2 * math.pi * i / n)) for i in range(n)]


def draw_s2(p):
    n, filled = p
    return f'<polygon points="{pts(reg_poly(n))}" fill="{B if filled else "none"}"/>'


series_item("media", "¿Qué figura continúa la serie?", [(3, 1), (4, 0), (5, 1), (6, 0)], draw_s2, (7, 1),
            [(7, 0), (8, 1), (6, 1)],
            "Hay dos reglas a la vez: el número de lados aumenta en 1 (3, 4, 5, 6 → 7) y el sombreado se alterna (sombreado, vacío, sombreado, vacío → sombreado). La respuesta es un heptágono sombreado.")


def arrow(angle, L=26):
    a = math.radians(angle)
    d = (math.sin(a), -math.cos(a))
    n = (-d[1], d[0])
    c = (40, 40)
    tail = (c[0] - d[0] * L, c[1] - d[1] * L)
    tip = (c[0] + d[0] * L, c[1] + d[1] * L)
    base = (c[0] + d[0] * (L - 12), c[1] + d[1] * (L - 12))
    h1 = (base[0] + n[0] * 8, base[1] + n[1] * 8)
    h2 = (base[0] - n[0] * 8, base[1] - n[1] * 8)
    return (f'<line x1="{fmt(tail[0])}" y1="{fmt(tail[1])}" x2="{fmt(base[0])}" y2="{fmt(base[1])}"/>'
            f'<polygon points="{pts([tip, h1, h2])}" fill="currentColor"/>')


def draw_s3(p):
    return arrow(p[0])


series_item("facil", "¿Qué figura continúa la serie?", [(0,), (45,), (90,), (135,)], draw_s3, (180,),
            [(225,), (135,), (270,)],
            "La flecha gira 45° en sentido horario en cada paso: arriba, diagonal, derecha, diagonal… La siguiente apunta hacia abajo (180°).")

PER = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]


def draw_s4(p):
    s, d = p
    b = []
    for i in range(3):
        for j in range(3):
            fill = B if PER[s % 8] == (i, j) else "none"
            b.append(f'<rect x="{10+i*20}" y="{10+j*20}" width="20" height="20" fill="{fill}"/>')
    dx, dy = PER[d % 8]
    b.append(f'<circle cx="{20+dx*20}" cy="{20+dy*20}" r="5" fill="currentColor" stroke="none"/>')
    return "".join(b)


seq4 = [((2 * k) % 8, (5 - k) % 8) for k in range(5)]
series_item("dificil", "¿Qué figura continúa la serie?", seq4[:4], draw_s4, seq4[4],
            [(0, 3), (7, 1), (0, 2)],
            "Por el borde de la cuadrícula se mueven dos elementos: la casilla sombreada avanza 2 casillas en sentido horario y el punto avanza 1 casilla en sentido antihorario. En el 5.º paso la sombra llega a la esquina superior izquierda y el punto a la casilla superior central.")


def draw_s5(p):
    a1, a2 = p
    r1, r2 = math.radians(a1), math.radians(a2)
    c = 40
    x1, y1 = c + 26 * math.sin(r1), c - 26 * math.cos(r1)
    x2, y2 = c + 15 * math.sin(r2), c - 15 * math.cos(r2)
    return (f'<circle cx="40" cy="40" r="33" fill="{A}"/>'
            f'<line x1="40" y1="40" x2="{fmt(x1)}" y2="{fmt(y1)}"/>'
            f'<line x1="40" y1="40" x2="{fmt(x2)}" y2="{fmt(y2)}"/>'
            f'<circle cx="{fmt(x2)}" cy="{fmt(y2)}" r="4.5" fill="currentColor" stroke="none"/>'
            f'<circle cx="40" cy="40" r="3" fill="currentColor" stroke="none"/>')


seq5 = [((90 * k) % 360, (90 - 45 * k) % 360) for k in range(5)]
series_item("dificil", "¿Qué figura continúa la serie?", seq5[:4], draw_s5, seq5[4],
            [(0, 90), (90, 270), (0, 315)],
            "La aguja larga gira 90° en sentido horario en cada paso (arriba, derecha, abajo, izquierda → arriba). La aguja corta con punto gira 45° en sentido antihorario (derecha, diagonal, arriba, diagonal → izquierda).")

# ----------------------------------------------------------------- matrices
CELL = 64


def shape_body(kind, fill, cx, cy, r):
    if kind == "circ":
        return f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}"/>'
    if kind == "sq":
        return f'<rect x="{fmt(cx-r*.85)}" y="{fmt(cy-r*.85)}" width="{fmt(1.7*r)}" height="{fmt(1.7*r)}" fill="{fill}"/>'
    if kind == "tri":
        return f'<polygon points="{pts(reg_poly(3, cx, cy + r*.15, r*1.1))}" fill="{fill}"/>'
    raise ValueError


def matrix_main(draw, cells):
    g = 6
    W = 3 * CELL + 2 * g
    out = []
    for i in range(3):
        for j in range(3):
            x, y = j * (CELL + g), i * (CELL + g)
            if (i, j) == (2, 2):
                out.append(f'<g transform="translate({x},{y})"><rect x="1" y="1" width="{CELL-2}" height="{CELL-2}" stroke-dasharray="5 4"/>{text(CELL/2, CELL/2, "?", 26)}</g>')
            else:
                out.append(f'<g transform="translate({x},{y})"><rect x="1" y="1" width="{CELL-2}" height="{CELL-2}"/>{draw(cells[i][j])}</g>')
    return svg(W, W, "".join(out))


def mcell(draw, p):
    return svg(CELL, CELL, f'<rect x="1" y="1" width="{CELL-2}" height="{CELL-2}"/>' + draw(p))


def matrix_item(diff, cells, answer, distract, draw, expl):
    assert cells[2][2] == answer
    fig = matrix_main(draw, cells)
    opts = [(repr(answer), mcell(draw, answer))] + [(repr(d), mcell(draw, d)) for d in distract]
    add("matrices", diff, "¿Qué figura completa la matriz (casilla con «?»)?", fig, opts, 0, expl)


SHP = ["circ", "sq", "tri"]


def draw_m1(p):
    kind, n = p
    posx = {1: [32], 2: [20, 44], 3: [14, 32, 50]}[n]
    return "".join(shape_body(kind, B, x, 32, 8) for x in posx)


m1c = [[(SHP[i], j + 1) for j in range(3)] for i in range(3)]
matrix_item("facil", m1c, ("tri", 3), [("tri", 2), ("sq", 3), ("circ", 3)], draw_m1,
            "Cada fila usa una sola forma (círculos, cuadrados, triángulos) y en cada fila la cantidad crece 1, 2, 3. Falta: 3 triángulos.")

FILLS = ["none", B, "currentColor"]


def draw_m2(p):
    k, f = p
    return shape_body(SHP[k], FILLS[f], 32, 32, 18)


m2c = [[((i + j) % 3, (i + 2 * j) % 3) for j in range(3)] for i in range(3)]
assert m2c[2][2] == (1, 0)
matrix_item("media", m2c, (1, 0), [(1, 1), (0, 0), (2, 2)], draw_m2,
            "En cada fila y en cada columna aparecen una vez cada forma (círculo, cuadrado, triángulo) y una vez cada relleno (blanco, gris, negro). A la última fila le falta el cuadrado y el relleno blanco.")

LINES = {"d1": (10, 10, 54, 54), "d2": (54, 10, 10, 54), "v": (32, 8, 32, 56), "h": (8, 32, 56, 32)}


def draw_m3(p):
    return "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in (LINES[k] for k in sorted(p)))


rowsAB = [({"d1", "v"}, {"v", "h"}), ({"d2", "h"}, {"h", "d1"}), ({"v", "d2"}, {"d2", "d1", "h"})]
m3c = [[tuple(sorted(a)), tuple(sorted(b)), tuple(sorted(a ^ b))] for a, b in rowsAB]
a3, b3 = rowsAB[2]
matrix_item("dificil", m3c, tuple(sorted(a3 ^ b3)),
            [tuple(sorted(a3 | b3)), tuple(sorted(a3 & b3)), tuple(sorted({"v", "d1"}))], draw_m3,
            "En cada fila, la 3.ª figura se obtiene superponiendo la 1.ª y la 2.ª, pero las líneas que aparecen en ambas se borran (solo quedan las no comunes). En la última fila la diagonal común desaparece y quedan la vertical, la horizontal y la otra diagonal.")

# ----------------------------------------------------------------- salida
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(ITEMS, fh, ensure_ascii=False, indent=1)
print(len(ITEMS), "items ->", OUT)
