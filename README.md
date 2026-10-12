# Prácticas Cerro Verde

Simulador que armé para prepararme para la primera etapa del **Programa de Becarios de Sociedad Minera Cerro Verde** (evaluada por TECSUP): el Examen de Competencias y el Examen de Aptitudes.

No encontré un temario oficial, así que junté lo que dicen el correo de convocatoria, el curso en Canvas, foros de postulantes de años anteriores y guías de tests psicotécnicos, y a partir de eso hice bancos de preguntas propios para practicar.

## Qué tiene

- **Práctica por área**, con la respuesta y la explicación al instante:
  - razonamiento verbal, numérico, lógico (incluye parentesco) y espacial
  - inglés y Excel
- **Simulacro con reloj** de 20, 40 o 60 preguntas:
  - navegador de preguntas y opción para marcar las que quieres revisar
  - nota por área al final
  - contador de salidas de pestaña, para practicar como en el examen supervisado
- **Competencias**:
  - casos de juicio situacional (elegir la mejor y la peor acción)
  - cuestionario de personalidad que revisa la consistencia entre preguntas parecidas
- **Plan de estudio** y guía de entrevista con datos de la empresa.

El progreso se guarda en el `localStorage` del navegador.

## Uso

Abrir `index.html` en el navegador. No necesita servidor.

## Estructura

```
index.html          simulador (generado)
banco/              preguntas en JSON
generadores/        scripts que generan y verifican cada banco
build/template.html página sin datos
build/build.py      valida los bancos y los inserta en index.html
docs/               resumen de la investigación sobre el proceso
```

Para regenerar la página después de cambiar preguntas:

```bash
python3 build/build.py
```

Los generadores de numérico, lógico, espacial y Excel recalculan cada respuesta antes de escribir el JSON. En espacial, las figuras se generan desde coordenadas y los cubos se pliegan por simulación. `generadores/render_check.py` pasa los SVG a PNG para revisarlos a ojo.

## Formato de una pregunta

```json
{
  "id": "n01",
  "area": "numerico",
  "subtype": "porcentajes",
  "difficulty": "media",
  "prompt": "texto (admite <b>, <table>, ...)",
  "figure": "<svg>…</svg>",
  "options": ["…", "…", "…", "…"],
  "answer": 2,
  "explanation": "…"
}
```

`figure` solo existe en las preguntas de espacial.

## Nota

Todas las preguntas son de práctica y las escribí para este proyecto; no son preguntas reales del examen. El formato y la cantidad del examen real pueden ser distintos.
