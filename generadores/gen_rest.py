import json, sys
from collections import Counter

S = []
def sjt(comp, prompt, options, best, worst, expl):
    i = len(S) + 1
    assert len(options) == 4 and best != worst
    S.append({"id": f"s{i:02d}", "area": "competencias", "subtype": "sjt", "competencia": comp,
              "prompt": prompt, "options": options, "best": best, "worst": worst, "explanation": expl})

sjt("Seguridad",
    "Eres becario en la planta concentradora. Durante una ronda con un técnico notas que la guarda de protección de una faja transportadora está suelta y la faja sigue operando. El técnico te dice: \"Tranquilo, la reportamos al terminar el turno, falta poco\".",
    ["Aceptar su criterio porque tiene más experiencia y anotar la observación para el reporte de fin de turno.",
     "Plantearle con respeto que la condición es un riesgo de atrapamiento, pedir detener la faja o aislar la zona y avisar de inmediato al supervisor de turno.",
     "Tomar una foto de la guarda suelta y enviarla al grupo de WhatsApp del área para que alguien la atienda.",
     "Intentar ajustar tú mismo la guarda con la faja en movimiento para no interrumpir la producción."],
    1, 3,
    "La mejor aplica la autoridad para detener trabajo inseguro y el reporte inmediato: un atrapamiento en faja es un riesgo fatal (Fatal Risk Management) y ningún trabajo es tan urgente que no se pueda hacer de forma segura. La peor expone tu vida al intervenir un equipo en movimiento sin bloqueo (LOTO); posponer el reporte o delegarlo informalmente tampoco controla el riesgo.")
sjt("Seguridad",
    "Tu jefe de área necesita que un lote de muestras llegue al laboratorio antes de las 17:00. Para llegar a tiempo tendrías que cruzar una vía de acarreo por un punto no autorizado, ahorrando 15 minutos. Son las 16:40.",
    ["Cruzar por el punto no autorizado con mucho cuidado, verificando que no vengan camiones.",
     "Usar la ruta peatonal autorizada y avisar al jefe y al laboratorio que llegarás unos minutos tarde.",
     "Pedir a un conductor de camioneta que te lleve por la vía de acarreo sin informar al despacho.",
     "Esperar al día siguiente para entregar las muestras y no decir nada para evitar problemas."],
    1, 0,
    "La mejor respeta los controles (rutas segregadas peatón-equipo pesado) y comunica el retraso: la producción no justifica asumir un riesgo de interacción con equipos pesados, que es un riesgo fatal. La peor es cruzar por un punto no autorizado: \"con cuidado\" no es un control. Ocultar el retraso también falla en Compromiso, pero no te expone a la muerte.")
sjt("Seguridad",
    "Al inicio de la guardia, en la charla de 5 minutos, notas que un compañero tiene aliento a alcohol y se muestra somnoliento. Él va a operar un montacargas hoy.",
    ["No decir nada porque no estás seguro y podrías perjudicarlo.",
     "Hablar en privado con él y sugerirle que tome un café antes de empezar.",
     "Informar de manera discreta y respetuosa al supervisor para que evalúe si está apto para trabajar (fit for duty).",
     "Comentarlo con otros compañeros para ver si ellos también lo notaron antes de hacer algo."],
    2, 0,
    "Ser apto para el trabajo es una responsabilidad compartida; el supervisor tiene el procedimiento para evaluarlo sin juzgarlo públicamente. Lo peor es callar: si opera el montacargas en ese estado puede causar una fatalidad. Comentarlo con otros genera rumores y no controla el riesgo; el café no resuelve la falta de aptitud.")
sjt("Seguridad",
    "Mientras caminas por el taller tropiezas con una manguera mal ubicada y te tuerces levemente el tobillo. No hay lesión visible y te sientes capaz de seguir. Es tu segunda semana de prácticas y temes dar una mala imagen.",
    ["Reportar el incidente de inmediato al supervisor y acudir al tópico para evaluación, mencionando la manguera como condición insegura.",
     "Seguir trabajando y reportarlo solo si mañana el dolor aumenta.",
     "Reubicar la manguera para que nadie más se tropiece y no reportar nada porque fue algo menor.",
     "Contárselo a un compañero de confianza para que quede registro informal."],
    0, 1,
    "La cultura de Cerro Verde exige reporte inmediato de todo incidente, incluso menor: permite atención médica oportuna y corregir la condición (orden y limpieza) antes de que cause algo grave. No hay represalias por reportar. Lo peor es esperar: oculta el incidente, puede agravar la lesión y deja el peligro sin investigar. Reubicar la manguera ayuda, pero sin reporte se pierde el aprendizaje.")
sjt("Seguridad",
    "Un compañero becario con quien te llevas muy bien suele quitarse los lentes de seguridad en la zona de chancado porque \"se empañan\". Ya lo has visto hacerlo tres veces.",
    ["No intervenir; es adulto y responsable de su propia seguridad.",
     "Reportarlo directamente a Recursos Humanos para que lo sancionen.",
     "Hablar con él en el momento, recordarle el riesgo de proyección de partículas y sugerirle solicitar lentes antiempañantes; si persiste, informar al supervisor.",
     "Ponerte también sin lentes para demostrarle solidaridad mientras buscan una solución juntos."],
    2, 3,
    "La mejor combina cuidado activo por el compañero (\"soy guardián de mi hermano\"), solución a la causa raíz (EPP adecuado) y escalamiento si persiste. La peor duplica la exposición al riesgo. No intervenir normaliza el incumplimiento; ir directo a RR. HH. salta el diálogo y el canal operativo (supervisor).")
sjt("Integridad",
    "Un proveedor de repuestos con quien coordinas cotizaciones te ofrece entradas VIP para un concierto en Lima \"como agradecimiento por tu apoyo\". Tu área está evaluando su propuesta.",
    ["Aceptarlas porque no tienen relación directa con la decisión de compra y no tienes poder de aprobación.",
     "Agradecer y rechazar cortésmente, explicando la política de regalos, e informar a tu supervisor del ofrecimiento.",
     "Aceptarlas y regalarlas a un compañero para no quedar mal con el proveedor.",
     "Pedirle que, en lugar de entradas, haga una donación a la comunidad de tu parte."],
    1, 0,
    "Los Principios de Conducta Empresarial prohíben aceptar regalos que puedan influir o aparentar influir en una decisión, sobre todo durante una evaluación de proveedores. Rechazar y transparentarlo protege a ti y a la empresa. Lo peor es aceptar: genera conflicto de interés aunque no apruebes la compra. Regalarlas no elimina el beneficio recibido; pedir una donación \"de tu parte\" mezcla relaciones comerciales y comunitarias.")
sjt("Integridad",
    "Preparando el reporte semanal de indicadores, descubres que en la versión que ya enviaste a la gerencia un error tuyo de fórmula infló la recuperación metalúrgica en 1,5 puntos. Nadie se ha dado cuenta.",
    ["Corregir el archivo en silencio para las siguientes semanas.",
     "Esperar a ver si alguien pregunta y entonces explicar el error.",
     "Informar a tu supervisor de inmediato, enviar la versión corregida y explicar qué controles aplicarás para que no se repita.",
     "Pedir a un compañero que revise el archivo para ver si confirma que fue un error tuyo antes de decir algo."],
    2, 0,
    "Los informes veraces son un principio central: la gerencia puede tomar decisiones con datos inflados. Reconocer el error propio de inmediato muestra integridad y excelencia. Lo peor es corregirlo en silencio: los datos falsos siguen circulando y se oculta deliberadamente el problema.")
sjt("Integridad",
    "Un amigo que trabaja en una empresa contratista te pide que le compartas \"solo para referencia\" el presupuesto referencial de una licitación que viste en una carpeta compartida de tu área.",
    ["Negarte explicando que es información confidencial y, si insiste, comentarlo con tu supervisor.",
     "Compartirle solo los montos totales, sin el detalle.",
     "Decirle que no tienes acceso para evitar el conflicto con él.",
     "Consultar primero con otro practicante si eso está permitido."],
    0, 1,
    "La información de licitaciones es confidencial y filtrarla favorece injustamente a un competidor (riesgo de corrupción y conflicto de interés). Lo mejor es negarse con claridad y transparentar el pedido. Lo peor es compartir aunque sea parcialmente: es una fuga real. Mentir sobre el acceso evita el problema pero no es honesto ni alerta a la empresa.")
sjt("Integridad",
    "Observas que un trabajador con más antigüedad registra horas extra que no trabajó. Cuando lo mencionas en broma, te dice: \"Aquí todos lo hacen, no te metas\".",
    ["Ignorarlo; como becario no te corresponde fiscalizar a nadie.",
     "Reportarlo por la Línea de Ética/canal de denuncias o a tu supervisor, describiendo solo los hechos observados.",
     "Confrontarlo frente al equipo para que todos vean que está mal.",
     "Advertirle que, si lo vuelve a hacer, lo reportarás."],
    1, 2,
    "Los Principios de Conducta Empresarial piden reportar posibles fraudes por los canales formales, que garantizan confidencialidad y no represalias. Lo peor es exponerlo públicamente: vulnera el respeto, genera conflicto y no activa una investigación. Ignorarlo es tolerar el fraude; advertirle negocia una falta que debe reportarse.")
sjt("Respeto",
    "En el comedor, un grupo de compañeros hace bromas reiteradas sobre el acento y la procedencia de una nueva técnica que viene de una comunidad de la zona. Ella se ríe, pero notas que se incomoda.",
    ["Reírte para no quedar fuera del grupo; si ella no se queja, no es un problema.",
     "Decir con calma que esas bromas pueden ofender, cambiar el tema y luego acercarte a ella para ofrecerle apoyo; si se repite, informar al supervisor.",
     "Esperar a que ella lo reporte, porque es su decisión.",
     "Dejar de almorzar con ese grupo para no involucrarte."],
    1, 0,
    "El respeto y la diversidad implican no tolerar burlas por origen o forma de hablar, aunque la persona no se queje (puede temer represalias). Intervenir con calma y escalar si persiste es lo adecuado. Lo peor es sumarte a las risas: refuerzas la discriminación. Alejarte o esperar no detiene el comportamiento.")
sjt("Respeto",
    "Acompañas al equipo de Relaciones Comunitarias a una reunión en un anexo. Un poblador, molesto, acusa a la empresa de contaminar su canal de riego y se dirige a ti en voz alta.",
    ["Explicarle técnicamente que la empresa cumple todos los estándares ambientales y que está equivocado.",
     "Escuchar con respeto, no comprometerte a nada que no te corresponde y derivar su inquietud al responsable de Relaciones Comunitarias para que quede registrada y se atienda.",
     "Prometerle que harás que alguien revise su canal esa misma semana para calmarlo.",
     "Retirarte de la reunión para no empeorar la situación."],
    1, 2,
    "En relaciones comunitarias, la escucha respetuosa y el uso del mecanismo formal de quejas construyen confianza. Lo peor es prometer algo que no puedes garantizar: dañar la credibilidad con la comunidad tiene consecuencias duraderas. Contradecirlo invalida su preocupación; retirarte puede leerse como desprecio.")
sjt("Trabajo en equipo",
    "En un proyecto grupal de becarios, un integrante no ha entregado su parte y faltan dos días para la presentación al gerente. Los demás proponen excluir su nombre del informe.",
    ["Aceptar la propuesta del grupo; quien no trabaja no debe figurar.",
     "Hacer tú su parte durante la noche sin decirle nada para asegurar el resultado.",
     "Conversar con él para entender qué pasa, redistribuir tareas si es necesario e informar al tutor del avance real si no se resuelve.",
     "Informar de inmediato al gerente que el compañero no está trabajando."],
    2, 0,
    "La mejor busca la causa, protege el resultado y mantiene la transparencia con el tutor. La peor excluye a alguien sin diálogo ni proceso, lo que rompe la confianza y el respeto en el equipo. Asumir su trabajo en silencio oculta el problema; escalar directo al gerente salta pasos.")
sjt("Trabajo en equipo",
    "Tu equipo de mantenimiento decidió usar un método de registro de órdenes de trabajo distinto al que tú propusiste. Crees que el tuyo era mejor.",
    ["Seguir usando tu método en tus registros para demostrar que es mejor.",
     "Aplicar el método acordado, registrar evidencia de su desempeño y proponer ajustes en la siguiente reunión de mejora.",
     "Usar el método acordado pero comentar con otros que no funcionará.",
     "Dejar de aportar ideas porque no te escuchan."],
    1, 0,
    "Comprometerse con la decisión del equipo y aportar mejoras con datos es colaboración madura. La peor rompe la estandarización: registros con métodos distintos generan errores en mantenimiento. Criticar a espaldas o desconectarse también dañan al equipo, pero no comprometen directamente la información.")
sjt("Orientación a resultados",
    "Te asignan actualizar el inventario de repuestos críticos en el sistema antes del viernes. El jueves descubres que hay 300 códigos con descripciones inconsistentes que te tomarían dos días adicionales corregir.",
    ["Entregar el viernes solo lo que alcanzaste, sin mencionar las inconsistencias.",
     "Avisar hoy a tu supervisor, proponer priorizar los repuestos críticos para el viernes y un plan para corregir el resto.",
     "Trabajar hasta la madrugada jueves y viernes para terminar todo sin avisar.",
     "Pedir una semana más de plazo sin explicar el motivo."],
    1, 0,
    "Orientarse a resultados es gestionar alcance, plazo y calidad con comunicación temprana. Priorizar lo crítico entrega valor y hace visible el problema. Lo peor es ocultar las inconsistencias: el equipo de mantenimiento podría confiar en datos erróneos. Trabajar sin descanso afecta tu aptitud (fit for duty) y no resuelve la falta de visibilidad.")
sjt("Orientación a resultados",
    "Notas que el reporte diario de paradas de planta se arma copiando datos manualmente de tres archivos, lo que toma 2 horas diarias. Crees que podrías automatizarlo con Power Query, aunque no es tu tarea asignada.",
    ["No proponerlo porque el proceso funciona y no te lo pidieron.",
     "Desarrollar la automatización a escondidas y reemplazar el reporte sin avisar para sorprender a todos.",
     "Hacer un prototipo en tus tiempos disponibles, mostrarlo a tu supervisor con el ahorro estimado y validarlo con los usuarios antes de implementarlo.",
     "Comentar a los demás que el proceso actual es ineficiente."],
    2, 1,
    "La excelencia incluye proponer mejoras con evidencia y validarlas con los usuarios y el responsable (gestión del cambio). La peor reemplaza un reporte oficial sin control: si tiene errores, afecta decisiones de planta. Criticar sin proponer o callar no aportan valor.")
sjt("Aprendizaje",
    "Te piden usar un software de modelamiento de minas que nunca has visto, y la persona que lo domina está de vacaciones dos semanas.",
    ["Decir que no puedes hacer la tarea hasta que regrese.",
     "Buscar los manuales y cursos internos, practicar con datos de prueba, consultar a otros usuarios del área y reportar avances y dudas a tu supervisor.",
     "Intentar aprenderlo solo sin decirle a nadie que no lo conoces.",
     "Pedir a un amigo externo que lo haga por ti enviándole los archivos del proyecto."],
    1, 3,
    "La disposición a aprender con recursos disponibles y transparencia sobre el avance es lo que se espera de un becario. Lo peor es enviar archivos de la empresa a un tercero: viola la confidencialidad. Ocultar que no lo conoces puede generar errores; negarte frena el trabajo.")
sjt("Aprendizaje",
    "En la retroalimentación de mitad de programa, tu tutor señala que tus informes son desordenados y difíciles de seguir. Tú sentías que estaban bien.",
    ["Agradecer, pedir ejemplos concretos y un modelo de informe, y pedirle revisar el siguiente para verificar tu mejora.",
     "Explicarle que en tu universidad te enseñaron otro formato y que así está correcto.",
     "Aceptar el comentario sin preguntar nada y seguir igual.",
     "Pedir a otro practicante que redacte tus informes."],
    0, 3,
    "Recibir retroalimentación con apertura y convertirla en un plan de mejora verificable demuestra aprendizaje. La peor delega tu responsabilidad y no desarrolla la competencia (además falsea la autoría). Justificarte o aceptar sin cambiar no generan mejora.")
sjt("Comunicación",
    "Un ingeniero de operaciones (cliente interno) te llama molesto porque el dashboard que mantienes muestra datos de ayer y tiene una reunión con gerencia en una hora.",
    ["Explicarle que el problema es de la base de datos de TI y no tuyo.",
     "Escuchar, confirmar qué necesita para la reunión, darle un tiempo realista de solución o un respaldo alternativo (exportación manual) y luego informar la causa.",
     "Prometerle que estará listo en 10 minutos aunque no sabes la causa.",
     "Decirle que lo revisarás y empezar a investigar sin volver a contactarlo hasta resolverlo."],
    1, 2,
    "Una buena comunicación con el cliente interno prioriza su necesidad inmediata, da expectativas realistas y ofrece alternativas. Lo peor es prometer un plazo sin base: si fallas, pierde la reunión y la confianza. Culpar a otra área o desaparecer sin actualizaciones tampoco ayudan.")
sjt("Comunicación",
    "En una reunión de seguridad, el supervisor explica un nuevo procedimiento de bloqueo (LOTO) y no entiendes un paso clave. Todos parecen haberlo entendido.",
    ["Quedarte callado y preguntar a un compañero después.",
     "Preguntar en ese momento de forma concreta cuál es el paso y por qué se hace así.",
     "Buscar el procedimiento en internet luego.",
     "Asumir que lo entenderás cuando lo apliques en campo."],
    1, 3,
    "En procedimientos críticos (aislamiento de energías), entender cada paso antes de aplicarlo es obligatorio; preguntar también ayuda a otros con la misma duda. Lo peor es aprender \"en campo\": un error de bloqueo puede ser fatal. Preguntar luego a un compañero o en internet puede darte una versión incorrecta.")
sjt("Adaptabilidad",
    "Por una emergencia en la planta, tu supervisor te pide dejar tu proyecto de análisis de datos y apoyar durante una semana al área de almacén en el conteo de inventario.",
    ["Aceptar, entender las prioridades del almacén, informar el estado de tu proyecto y acordar cuándo retomarlo.",
     "Aceptar pero hacer el mínimo, ya que no es parte de tu formación.",
     "Negarte porque tu proyecto tiene un plazo y es tu prioridad.",
     "Aceptar y seguir avanzando tu proyecto a escondidas durante el conteo."],
    0, 3,
    "La adaptabilidad implica responder a prioridades cambiantes cuidando la continuidad de lo propio. La peor es la menos transparente: divide tu atención, afecta la calidad del conteo y no comunica la situación real. Hacer el mínimo o negarte muestran bajo compromiso.")
sjt("Compromiso",
    "Llevas tres semanas con más tareas de las que puedes completar: tu tutor, otro ingeniero y el área de capacitación te asignan trabajos sin coordinar entre ellos. Empiezas a quedarte hasta tarde y a dormir poco.",
    ["Seguir así hasta terminar el programa; es una oportunidad para demostrar tu compromiso.",
     "Hacer una lista de tareas con plazos, presentarla a tu tutor y pedirle ayuda para priorizar y coordinar con los demás.",
     "Dejar de responder las solicitudes que no vengan de tu tutor.",
     "Bajar la calidad de todas las tareas para cumplir con las fechas."],
    1, 0,
    "Comprometerse también significa gestionar la carga de forma visible y cuidar tu aptitud: la fatiga es un factor de riesgo reconocido en minería. Lo peor es normalizar el agotamiento (riesgo para tu seguridad y calidad). Ignorar solicitudes o bajar la calidad sin acordarlo dañan la confianza.")
sjt("Compromiso",
    "Tu supervisor te pide subir al sistema los resultados de una inspección que hizo otro practicante, pero notas que faltan las firmas y dos ítems están en blanco. Te dice: \"Súbelo así, luego se completa; necesitamos cerrar el indicador hoy\".",
    ["Subirlo tal como está porque es una instrucción directa.",
     "Completar tú los ítems en blanco con lo que consideres más probable.",
     "Explicar respetuosamente que el registro está incompleto, proponer contactar hoy al practicante para completarlo y, si no es posible, registrar el indicador como pendiente con la observación.",
     "No hacer nada y esperar que tu supervisor se olvide."],
    2, 1,
    "Integridad y compromiso: los registros de inspección deben ser verídicos y completos; se puede buscar cerrar hoy sin falsear. Lo peor es inventar datos: es falsificación de un registro de seguridad. Subirlo incompleto cumple el pedido pero compromete la calidad del indicador; ignorarlo es evasivo.")

# ---------- personalidad ----------
P = []
def pair(trait, a, b, note, lie=False):
    """a: directo (reverse False), b: invertido (reverse True). Ordenes alternados."""
    k = len(P) // 2 + 1
    pid = f"P{k:02d}"
    for st, rev in ((a, False), (b, True)):
        P.append({"statement": st, "trait": trait, "pair": pid, "reverse": rev, "lie": lie, "note": note})

pair("responsabilidad", "Cumplo mis compromisos en el plazo acordado, aunque implique organizarme con anticipación.",
     "Con frecuencia dejo las tareas para el último momento.",
     "Mide confiabilidad y planificación. Las mineras buscan personas que cumplan plazos de forma predecible; sé coherente entre ambas respuestas.")
pair("responsabilidad", "Reviso mi trabajo antes de entregarlo para detectar errores.",
     "Si una tarea parece terminada, prefiero entregarla sin revisarla de nuevo.",
     "Mide minuciosidad. En operaciones un error de dato o de procedimiento tiene impacto; se valora el autocontrol de calidad.")
pair("seguridad", "Detendría una tarea si considero que no se puede realizar de forma segura, aunque eso retrase la producción.",
     "Cuando hay presión por cumplir la meta, es aceptable saltarse algún paso del procedimiento.",
     "Mide adhesión a la cultura de seguridad y stop-work. Es uno de los rasgos más críticos para una minera; las respuestas deben ser claras y coherentes.")
pair("seguridad", "Uso todo el equipo de protección personal requerido, incluso para trabajos cortos.",
     "Para tareas de pocos minutos, usar todo el EPP me parece exagerado.",
     "Mide disciplina con el EPP. La empresa busca cumplimiento constante, sin excepciones por duración de la tarea.")
pair("seguridad", "Reporto los incidentes y casi accidentes, aunque nadie más los haya visto.",
     "Si un incidente no causó daño, prefiero no reportarlo para evitar trámites.",
     "Mide cultura de reporte. Los casi accidentes son la base de la prevención; se busca a quien reporta con transparencia.")
pair("trabajo_en_equipo", "Disfruto colaborar con personas de distintas áreas para lograr un objetivo común.",
     "Rindo mejor cuando no tengo que coordinar con otros.",
     "Mide orientación colaborativa. En una mina casi todo depende de otros turnos y áreas; no se espera que odies trabajar solo, sino que valores la colaboración.")
pair("trabajo_en_equipo", "Ofrezco ayuda a mis compañeros cuando veo que están sobrecargados.",
     "Me concentro solo en mis tareas; lo que hagan los demás no es asunto mío.",
     "Mide apoyo mutuo. Se valora el compromiso con el resultado del equipo, no solo el individual.")
pair("apertura_aprendizaje", "Me entusiasma aprender herramientas o tecnologías nuevas.",
     "Prefiero seguir usando los métodos que ya conozco antes que aprender otros nuevos.",
     "Mide disposición al aprendizaje. En un programa de becarios es clave; ser coherente no implica rechazar lo conocido, sino mostrar apertura.")
pair("apertura_aprendizaje", "Pido retroalimentación sobre mi desempeño para mejorar.",
     "Las críticas a mi trabajo suelen molestarme más de lo que me ayudan.",
     "Mide receptividad al feedback. Se busca alguien que use la retroalimentación para crecer.")
pair("estabilidad_emocional", "Mantengo la calma cuando surgen problemas inesperados en el trabajo.",
     "Me altero con facilidad cuando las cosas no salen como lo planeé.",
     "Mide manejo de la presión. En operaciones con turnos, emergencias y metas exigentes se valora la serenidad para decidir bien.")
pair("estabilidad_emocional", "Puedo trabajar bajo presión sin que eso afecte mi rendimiento.",
     "Cuando tengo mucha carga de trabajo me bloqueo y no sé por dónde empezar.",
     "Mide tolerancia al estrés. Responde según tu realidad: la coherencia entre ambas es lo que se evalúa.")
pair("integridad", "Digo la verdad aunque me traiga consecuencias negativas.",
     "A veces es justificable ocultar un error si nadie resulta afectado.",
     "Mide honestidad, alineada con los Principios de Conducta Empresarial (informes veraces, reconocer errores).")
pair("integridad", "Rechazaría un regalo de un proveedor si pudiera parecer que influye en mi trabajo.",
     "Aceptar pequeños favores de proveedores es normal y no afecta las decisiones.",
     "Mide criterio frente a conflictos de interés y anticorrupción, muy sensibles en la industria minera.")
pair("orientacion_resultados", "Me fijo metas exigentes y trabajo con constancia para alcanzarlas.",
     "Me conformo con cumplir lo mínimo que se me pide.",
     "Mide motivación de logro. Se busca alguien que aspire a la excelencia, siempre sin sacrificar la seguridad.")
pair("orientacion_resultados", "Busco formas de hacer mi trabajo más eficiente.",
     "Si algo funciona, no veo necesidad de mejorarlo.",
     "Mide mejora continua. Las mineras valoran propuestas de innovación con datos y validadas.")
pair("adaptabilidad", "Me adapto con facilidad a cambios de horario, de tareas o de lugar de trabajo.",
     "Me cuesta mucho trabajar cuando cambian los planes a último momento.",
     "Mide flexibilidad. En operación minera hay turnos, campamento y prioridades cambiantes.")
pair("comunicacion", "Cuando no entiendo una instrucción, pregunto hasta tenerla clara.",
     "Prefiero no hacer preguntas para no parecer que no sé.",
     "Mide comunicación asertiva. En seguridad, preguntar a tiempo evita errores graves.")
pair("deseabilidad_social", "Nunca he dicho una mentira, ni siquiera pequeña.",
     "Alguna vez he exagerado algo para quedar bien.",
     "Escala de deseabilidad social (\"mentira\"). Responder 5 a la directa o 1 a la invertida sugiere que intentas dar una imagen perfecta; lo creíble es admitir imperfecciones normales.", lie=True)
pair("deseabilidad_social", "Jamás me he molestado con nadie.",
     "En ocasiones me he sentido irritado con alguna persona.",
     "Escala de deseabilidad social. Todos nos molestamos alguna vez; negarlo por completo resta credibilidad al resto del perfil.", lie=True)
pair("deseabilidad_social", "Siempre cumplo absolutamente todas las normas, sin excepción, en todos los ámbitos de mi vida.",
     "Alguna vez he llegado tarde o he olvidado algo que debía hacer.",
     "Escala de deseabilidad social. Se espera responsabilidad, no perfección absoluta; las respuestas extremas levantan sospecha de falta de sinceridad.", lie=True)

# intercalar para que los pares no queden contiguos: primero todas las 'a', luego las 'b' en otro orden
firsts = P[0::2]
seconds = P[1::2]
order = firsts + seconds[10:] + seconds[:10]
for i, it in enumerate(order):
    it["id"] = f"p{i+1:02d}"
pers = [{k: it[k] for k in ("id", "statement", "trait", "pair", "reverse", "lie", "note")} for it in order]

import random
rng = random.Random(11)
for k, it in enumerate(S):
    b, w = it["options"][it["best"]], it["options"][it["worst"]]
    perm = list(range(4))
    while True:
        rng.shuffle(perm)
        if perm.index(it["best"]) == k % 4: break
    it["options"] = [it["options"][j] for j in perm]
    it["best"], it["worst"] = it["options"].index(b), it["options"].index(w)
excel = json.load(open(sys.argv[1]))
out = {"excel": excel, "sjt": S, "personalidad": pers}
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(excel), len(S), len(pers))
print("best", Counter(s["best"] for s in S), "worst", Counter(s["worst"] for s in S))
