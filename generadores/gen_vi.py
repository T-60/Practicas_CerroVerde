import json, random, sys

# Each tuple: (id, area, subtype, difficulty, prompt, [correct, *distractors], explanation)
TA = ("<p><i>En las zonas áridas del sur peruano, el agua es un recurso que condiciona tanto la agricultura como la industria. "
      "Por ello, algunas operaciones mineras han optado por tratar aguas residuales urbanas y emplearlas en sus procesos, en lugar de captar agua de ríos "
      "que también abastecen a los agricultores. Este enfoque tiene un doble beneficio: reduce la presión sobre las fuentes naturales y mejora la calidad "
      "del agua que retorna al ambiente, pues antes esos efluentes se vertían sin tratamiento. No obstante, los especialistas advierten que estas soluciones "
      "requieren inversiones elevadas y un monitoreo permanente para asegurar que los parámetros de calidad se cumplan de manera sostenida.</i></p>")
TB = ("<p><i>La fatiga es uno de los factores de riesgo menos visibles en la operación de grandes camiones mineros. Un operador cansado puede tardar más "
      "en reaccionar o incluso quedarse dormido unos segundos, tiempo suficiente para provocar un accidente grave. Para enfrentar este problema, varias "
      "empresas han instalado sistemas que, mediante cámaras en la cabina, detectan el parpadeo prolongado o la inclinación de la cabeza y emiten alertas "
      "sonoras y vibraciones en el asiento. Sin embargo, la tecnología no sustituye la gestión adecuada de turnos ni el descanso efectivo. Los expertos "
      "coinciden en que el dispositivo es una barrera adicional, no la solución de fondo.</i></p>")
E1 = ("<p><i><b>SAFETY NOTICE</b><br>Starting next Monday, all visitors to the concentrator plant must complete a 30-minute safety induction before "
      "entering the operational area. The induction will be held at the training center every day at 7:00 a.m. and 2:00 p.m. Visitors must bring a valid ID "
      "and wear safety boots; helmets, glasses and reflective vests will be provided at the entrance. Anyone who arrives late will have to wait for the next "
      "session. For more information, contact the Safety Department at extension 2045.</i></p>")
E2 = ("<p><i>Water recycling has become a priority for many mining companies operating in dry regions. In a typical copper concentrator, large amounts "
      "of water are needed to separate valuable minerals from waste rock. After this process, the water is sent to thickeners, where solid particles settle "
      "at the bottom. The clear water at the top is then pumped back to the plant and reused. Thanks to this system, some operations recover more than 80% "
      "of the water they use. However, recycling alone is not enough; companies must also reduce losses caused by evaporation and leaks.</i></p>")

V = [
 ("sinonimos","facil","Señale el sinónimo de <b>PERENNE</b>.",["perpetuo","efímero","frágil","breve","variable"],"Perenne significa que dura siempre o de forma continua; su sinónimo es perpetuo."),
 ("sinonimos","media","Señale el sinónimo de <b>ACUCIOSO</b>.",["diligente","indolente","agresivo","ingenuo","ruidoso"],"Acucioso se aplica a quien actúa con diligencia, esmero y prontitud."),
 ("sinonimos","facil","Señale el sinónimo de <b>MITIGAR</b>.",["atenuar","agravar","ocultar","medir","provocar"],"Mitigar es moderar o disminuir la intensidad de algo, es decir, atenuar."),
 ("sinonimos","media","Señale el sinónimo de <b>EXIGUO</b>.",["escaso","abundante","extenso","sutil","ruidoso"],"Exiguo significa insuficiente o escaso."),
 ("sinonimos","dificil","Señale el sinónimo de <b>CONSPICUO</b>.",["sobresaliente","oculto","mezquino","dudoso","torpe"],"Conspicuo se dice de lo ilustre, visible o sobresaliente."),
 ("antonimos","facil","Señale el antónimo de <b>ESCASEZ</b>.",["abundancia","carestía","penuria","falta","pobreza"],"Escasez es falta de algo; su opuesto es abundancia. Las demás opciones son sinónimos."),
 ("antonimos","media","Señale el antónimo de <b>DILIGENTE</b>.",["negligente","hábil","presto","activo","atento"],"Diligente es quien actúa con cuidado y prontitud; lo contrario es negligente."),
 ("antonimos","facil","Señale el antónimo de <b>AUMENTAR</b>.",["reducir","ampliar","crecer","elevar","acrecentar"],"Aumentar es hacer mayor algo; su opuesto es reducir. Las demás son sinónimos."),
 ("antonimos","media","Señale el antónimo de <b>INOCUO</b>.",["nocivo","inofensivo","leve","benigno","sano"],"Inocuo significa que no hace daño; su antónimo es nocivo."),
 ("antonimos","dificil","Señale el antónimo de <b>PRÓDIGO</b>.",["mezquino","generoso","dadivoso","derrochador","espléndido"],"Pródigo es quien gasta o da sin medida; lo opuesto es mezquino (tacaño)."),
 ("analogias","facil","<b>CASCO : CABEZA ::</b>",["guantes : manos","lentes : montura","botas : suela","chaleco : bolsillo","overol : tela"],"El casco protege la cabeza, así como los guantes protegen las manos (relación protector–parte del cuerpo)."),
 ("analogias","facil","<b>MINERAL : CONCENTRADORA ::</b>",["trigo : molino","harina : pan","leche : vaca","agua : río","madera : bosque"],"El mineral es la materia prima que se procesa en la concentradora, como el trigo se procesa en el molino."),
 ("analogias","media","<b>TERMÓMETRO : TEMPERATURA ::</b>",["manómetro : presión","martillo : clavo","reloj : pulsera","regla : madera","microscopio : laboratorio"],"El termómetro mide la temperatura; el manómetro mide la presión (instrumento–magnitud que mide)."),
 ("analogias","media","<b>SEQUÍA : AGUA ::</b>",["hambruna : alimento","inundación : lluvia","incendio : fuego","frío : invierno","oscuridad : noche"],"La sequía es la carencia de agua, así como la hambruna es la carencia de alimento."),
 ("analogias","dificil","<b>ESCORIA : FUNDICIÓN ::</b>",["aserrín : carpintería","acero : horno","cobre : mina","pan : panadería","vino : bodega"],"La escoria es el residuo que deja la fundición, como el aserrín es el residuo del trabajo de carpintería."),
 ("analogias","dificil","<b>ARQUITECTO : PLANO ::</b>",["compositor : partitura","pintor : pincel","médico : hospital","escritor : editorial","cocinero : cocina"],"El arquitecto elabora planos, el compositor elabora partituras (autor–documento que crea para plasmar su obra)."),
 ("oraciones_incompletas","facil","Antes de ingresar a la zona de voladura, todo trabajador debe esperar la ________ del supervisor.",["autorización","reprimenda","indiferencia","ausencia","renuncia"],"En un contexto de seguridad, el ingreso a una zona de riesgo requiere la autorización del supervisor."),
 ("oraciones_incompletas","media","El informe fue tan ________ que, en solo una página, resumió los hallazgos de seis meses de monitoreo.",["conciso","extenso","ambiguo","redundante","confuso"],"Resumir mucha información en una página indica brevedad y precisión, es decir, un informe conciso."),
 ("oraciones_incompletas","media","La empresa invirtió en una planta de tratamiento para ________ el consumo de agua fresca y ________ el agua de proceso.",["reducir – reutilizar","aumentar – desechar","duplicar – contaminar","mantener – desperdiciar","ignorar – reciclar"],"Una planta de tratamiento busca reducir el uso de agua fresca y reutilizar el agua de proceso; es la única pareja coherente."),
 ("oraciones_incompletas","facil","A pesar de las ________ condiciones climáticas, la cuadrilla terminó el mantenimiento a tiempo.",["adversas","favorables","óptimas","ideales","apacibles"],"«A pesar de» introduce una dificultad; solo «adversas» expresa condiciones desfavorables."),
 ("oraciones_incompletas","dificil","Si bien la nueva tecnología ________ los costos operativos, su implementación ________ una capacitación intensiva del personal, lo que ________ su adopción inmediata.",["reduce – exige – dificulta","incrementa – evita – facilita","reduce – elimina – acelera","eleva – requiere – impide","mantiene – omite – favorece"],"«Si bien» plantea una ventaja (reduce costos) frente a una desventaja (exige capacitación), que a su vez dificulta la adopción inmediata."),
 ("conectores","facil","El equipo no superó la inspección; ________, fue retirado de operación.",["por consiguiente","sin embargo","aunque","además","en cambio"],"El retiro del equipo es consecuencia de no superar la inspección, por lo que se requiere un conector consecutivo."),
 ("conectores","media","________ el yacimiento tiene baja ley, su gran volumen lo hace económicamente viable.",["Si bien","Porque","Dado que","Por lo tanto","Así que"],"Se oponen una desventaja (baja ley) y una ventaja (gran volumen); «si bien» es el conector concesivo adecuado."),
 ("conectores","media","Los trabajadores recibieron capacitación en primeros auxilios; ________, se les entregó un manual de procedimientos.",["asimismo","no obstante","por el contrario","aunque","o sea"],"La segunda acción se suma a la primera, por lo que corresponde un conector aditivo como «asimismo»."),
 ("conectores","dificil","La presa cumple los estándares internacionales; ________, se realizan monitoreos diarios, ________ cualquier anomalía pueda detectarse a tiempo.",["aun así – de modo que","por lo tanto – aunque","es decir – porque","en cambio – sin que","además – pero"],"«Aun así» indica que, pese a cumplir estándares, se sigue monitoreando; «de modo que» expresa la finalidad de detectar anomalías."),
 ("termino_excluido","facil","Señale el término que no guarda relación con los demás.",["granito","cobre","molibdeno","plata","oro"],"Cobre, molibdeno, plata y oro son metales; el granito es una roca."),
 ("termino_excluido","media","Señale el término que no guarda relación con los demás.",["temeridad","precaución","prudencia","cautela","cuidado"],"Todos los términos aluden a actuar con cuidado, excepto temeridad, que es exposición imprudente al peligro."),
 ("termino_excluido","dificil","Señale el término que no guarda relación con los demás.",["diáfano","lóbrego","sombrío","tenebroso","oscuro"],"Lóbrego, sombrío, tenebroso y oscuro aluden a falta de luz; diáfano significa claro o transparente."),
 ("comprension_lectora","media",TA+"¿Cuál es la idea principal del texto?",["El tratamiento de aguas residuales urbanas para uso minero alivia la presión sobre las fuentes naturales, aunque exige inversión y control constante.","La agricultura es la principal consumidora de agua en el sur peruano.","Las operaciones mineras están obligadas por ley a dejar de usar agua de ríos.","Los efluentes urbanos no pueden ser tratados de manera eficaz.","El monitoreo de la calidad del agua es innecesario si la inversión es alta."],"El texto presenta el uso de aguas residuales tratadas, sus beneficios y sus exigencias (inversión y monitoreo); las demás opciones son parciales o contradicen el texto."),
 ("comprension_lectora","dificil",TA+"Del texto se infiere que, antes de aplicarse este enfoque,",["los efluentes urbanos afectaban el ambiente al verterse sin tratamiento.","la minería no requería agua para sus procesos.","los agricultores utilizaban aguas residuales tratadas.","los ríos de la zona tenían un caudal abundante.","el monitoreo de la calidad del agua era permanente."],"El texto afirma que el enfoque «mejora la calidad del agua» porque antes los efluentes se vertían sin tratamiento, lo que implica un impacto ambiental previo."),
 ("comprension_lectora","facil",TB+"Según el texto, ¿cuál es la función de los sistemas instalados en la cabina?",["Detectar signos de somnolencia y alertar al operador.","Controlar automáticamente la velocidad del camión.","Reemplazar al operador en los turnos nocturnos.","Programar los turnos de trabajo del personal.","Grabar los accidentes para su posterior investigación."],"El texto indica que las cámaras detectan parpadeo prolongado o inclinación de la cabeza y emiten alertas sonoras y vibraciones."),
 ("comprension_lectora","media",TB+"¿Con cuál de las siguientes afirmaciones estaría de acuerdo el autor?",["Los sistemas de detección deben complementarse con una buena gestión de turnos y descanso.","La tecnología elimina por completo el riesgo asociado a la fatiga.","La fatiga es el riesgo más visible en la operación minera.","Los operadores cansados reaccionan más rápido ante emergencias.","Las alertas sonoras resultan inútiles para prevenir accidentes."],"El autor sostiene que el dispositivo es una barrera adicional que no sustituye la gestión de turnos ni el descanso."),
]

I = [
 ("gramatica","facil","Choose the correct option:<br><b>She works as ___ engineer at a copper mine.</b>",["an","a","the","Ø (no article)"],"Se usa «an» antes de palabras que empiezan con sonido vocálico, como «engineer»."),
 ("gramatica","facil","Choose the correct option:<br><b>___ Andes are the longest continental mountain range in the world.</b>",["The","A","An","Ø (no article)"],"Las cordilleras (nombres de cadenas montañosas en plural) llevan el artículo definido «the»."),
 ("gramatica","facil","Choose the correct option:<br><b>Every morning, the supervisor ___ the safety checklist before the shift starts.</b>",["reviews","review","reviewing","have reviewed"],"Para rutinas se usa el presente simple; con sujeto en tercera persona singular el verbo lleva «-s»."),
 ("gramatica","media","Choose the correct option:<br><b>The plant ___ since 2015 without a major accident.</b>",["has operated","operates","is operating","operated"],"«Since» con un punto de inicio que llega hasta el presente exige el presente perfecto."),
 ("gramatica","media","Choose the correct option:<br><b>While the technicians ___ the conveyor belt, the power suddenly went out.</b>",["were repairing","are repairing","repair","have repaired"],"Una acción en progreso en el pasado interrumpida por otra se expresa con el pasado continuo."),
 ("gramatica","facil","Choose the correct option:<br><b>The meeting is scheduled ___ Monday ___ 8 a.m.</b>",["on – at","in – on","at – in","on – in"],"Se usa «on» con días de la semana y «at» con horas exactas."),
 ("gramatica","media","Choose the correct option:<br><b>The new procedure is very different ___ the old one.</b>",["from","of","at","with"],"La forma estándar es «different from»."),
 ("gramatica","media","Choose the correct option:<br><b>If the sensor detects high temperatures, the system ___ automatically.</b>",["shuts down","would shut down","shut down","had shut down"],"Es un condicional cero (hecho general): «if» + presente simple, presente simple en la otra cláusula."),
 ("gramatica","dificil","Choose the correct option:<br><b>If the operator ___ the warning, the accident would not have happened.</b>",["had followed","followed","has followed","would follow"],"El tercer condicional (situación pasada irreal) usa «if» + pasado perfecto y «would have» + participio."),
 ("gramatica","dificil","Choose the correct option:<br><b>The deeper the pit gets, ___ it becomes to transport the ore.</b>",["the more expensive","more expensive","the most expensive","most expensive"],"La estructura comparativa doble es «the + comparativo…, the + comparativo»."),
 ("vocabulario","facil","A <b>helmet</b> is used to protect your:",["head","hands","feet","eyes"],"«Helmet» es casco, que protege la cabeza."),
 ("vocabulario","facil","Choose the opposite of <b>safe</b>:",["dangerous","secure","careful","protected"],"«Safe» significa seguro; su opuesto es «dangerous» (peligroso)."),
 ("vocabulario","media","Which word means <i>a machine that breaks large rocks into smaller pieces</i>?",["crusher","conveyor","drill","pump"],"«Crusher» es la chancadora o trituradora."),
 ("vocabulario","media","Workers must wear <b>goggles</b> in this area. Goggles protect the:",["eyes","ears","lungs","knees"],"«Goggles» son gafas o lentes de protección para los ojos."),
 ("vocabulario","media","Choose the word closest in meaning to <b>shortage</b>:<br><i>There is a water shortage in the region.</i>",["lack","excess","flood","quality"],"«Shortage» significa escasez, es decir, «lack» (falta)."),
 ("vocabulario","dificil","Maintenance report: <i>“The pump failed due to excessive <b>wear</b>.”</i> In this sentence, <b>wear</b> means:",["gradual damage caused by use and friction","clothing used for work","a type of lubricant","an electrical overload"],"En contexto técnico, «wear» es el desgaste progresivo por uso y fricción."),
 ("vocabulario","facil","A <b>conveyor belt</b> is used to:",["move materials from one place to another","measure the temperature","drill holes in rock","store water"],"La faja transportadora («conveyor belt») traslada materiales de un punto a otro."),
 ("comprension","facil",E1+"How long is the safety induction?",["30 minutes","2 hours","7 hours","45 minutes"],"El aviso indica «a 30-minute safety induction»."),
 ("comprension","facil",E1+"What must visitors bring or wear themselves?",["A valid ID and safety boots","A helmet and safety glasses","A reflective vest","Nothing; everything is provided"],"El texto dice que deben traer un documento válido y usar botas de seguridad; casco, lentes y chaleco se entregan en la entrada."),
 ("comprension","media",E1+"What happens if a visitor arrives late to the 7:00 a.m. session?",["They must wait for the 2:00 p.m. session.","They can join the session already in progress.","They cannot visit the plant that week.","They must call extension 2045 to enter."],"Quien llega tarde debe esperar la siguiente sesión, que es la de las 2:00 p.m."),
 ("comprension","media",E1+"In the notice, the word <b>provided</b> is closest in meaning to:",["supplied","required","removed","checked"],"«Will be provided» significa que serán entregados o suministrados («supplied»)."),
 ("comprension","media",E2+"What is the main purpose of the thickeners?",["To separate solid particles from the water","To evaporate the water","To crush the waste rock","To pump fresh water from rivers"],"En los espesadores los sólidos se asientan en el fondo y el agua clara se recupera, es decir, separan sólidos del agua."),
 ("comprension","media",E2+"According to the text, which statement is TRUE?",["Some operations recover more than 80% of the water they use.","All the water used in the process is recovered.","Evaporation helps companies recover more water.","Water recycling is only important in wet regions."],"El texto afirma que algunas operaciones recuperan más del 80% del agua que usan."),
 ("comprension","dificil",E2+"What can be inferred from the last sentence?",["Even with recycling, some water is still lost.","Water recycling is not useful for mining companies.","Leaks are the only cause of water loss.","Evaporation does not affect mining operations."],"Al decir que reciclar «no es suficiente» y que hay pérdidas por evaporación y fugas, se infiere que parte del agua se pierde pese al reciclaje."),
]

def place(items, n, seed, prefix, area):
    rng = random.Random(seed)
    pos = [i % n for i in range(len(items))]
    rng.shuffle(pos)
    out = []
    for k, (st, d, p, opts, ex) in enumerate(items):
        assert len(opts) == n
        correct, rest = opts[0], opts[1:]
        t = pos[k]
        o = rest[:t] + [correct] + rest[t:]
        out.append({"id": f"{prefix}{k+1:02d}", "area": area, "subtype": st, "difficulty": d,
                    "prompt": p, "options": o, "answer": t, "explanation": ex})
    return out

data = place(V, 5, 11, "v", "verbal") + place(I, 4, 23, "i", "ingles")
json.dump(data, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
