# ============================================================
# ELIZYUM - MOOD ENGINE v3.9
# emotions/mood.py
#
# MOTOR CENTRAL DE FACETAS EMOCIONALES Y RELACIONALES
#
# Este módulo contiene la lógica general.
# Los miembros específicos, como Eli, utilizan este motor
# mediante sus respectivos adaptadores.
#
# ============================================================


# ============================================================
# FACETAS
# ============================================================

FACETA_NORMAL = "normal"
FACETA_ATENTA = "atenta"
FACETA_CERCANA = "cercana"
FACETA_JUGUETONA = "juguetona"
FACETA_COQUETA = "coqueta"
FACETA_CORTANTE = "cortante"
FACETA_CAUTA = "cauta"
FACETA_CELOSA = "celosa"
FACETA_HERIDA = "herida"
FACETA_RECONCILIADORA = "reconciliadora"


FACETAS_VALIDAS = {
    FACETA_NORMAL,
    FACETA_ATENTA,
    FACETA_CERCANA,
    FACETA_JUGUETONA,
    FACETA_COQUETA,
    FACETA_CORTANTE,
    FACETA_CAUTA,
    FACETA_CELOSA,
    FACETA_HERIDA,
    FACETA_RECONCILIADORA,
}


# ============================================================
# UTILIDADES
# ============================================================

def limitar(valor, minimo=0, maximo=100):
    """
    Limita un valor al rango indicado.
    """

    try:
        valor = int(float(valor))
    except (TypeError, ValueError):
        valor = minimo

    return max(
        minimo,
        min(maximo, valor)
    )


def obtener_emocion(emociones, nombre):
    """
    Obtiene una emoción de forma segura.
    """

    if not isinstance(
        emociones,
        dict
    ):
        return 0

    return limitar(
        emociones.get(
            nombre,
            0
        )
    )


# ============================================================
# EVENTOS RELACIONALES
# ============================================================

def obtener_evento(contexto_relacional):
    """
    Obtiene el evento relacional reciente.

    Soporta:

        "evento_relacional": "mentira"

    o:

        "evento_relacional": {
            "evento": "mentira",
            "intensidad": 80
        }
    """

    if not isinstance(
        contexto_relacional,
        dict
    ):
        return "ninguno", 0

    evento = contexto_relacional.get(
        "evento_relacional",
        "ninguno"
    )

    intensidad = contexto_relacional.get(
        "intensidad_evento",
        0
    )

    if isinstance(
        evento,
        dict
    ):

        nombre = evento.get(
            "evento",
            "ninguno"
        )

        intensidad = evento.get(
            "intensidad",
            intensidad
        )

    else:

        nombre = evento

    if nombre is None:
        nombre = "ninguno"

    return (
        nombre,
        limitar(intensidad)
    )


# ============================================================
# AMENAZA RELACIONAL
# ============================================================

def obtener_amenaza(contexto_relacional):
    """
    Obtiene información sobre una posible amenaza
    relacional.
    """

    if not isinstance(
        contexto_relacional,
        dict
    ):
        return False, 0

    amenaza = contexto_relacional.get(
        "amenaza_relacional",
        False
    )

    intensidad = contexto_relacional.get(
        "intensidad_amenaza",
        0
    )

    if isinstance(
        amenaza,
        dict
    ):

        activa = bool(
            amenaza.get(
                "amenaza_relacional",
                amenaza.get(
                    "amenaza",
                    amenaza.get(
                        "activa",
                        False
                    )
                )
            )
        )

        intensidad = amenaza.get(
            "intensidad",
            intensidad
        )

    else:

        activa = bool(
            amenaza
        )

    intensidad = limitar(
        intensidad
    )

    # Compatibilidad con contextos donde existe
    # amenaza pero no se especifica intensidad.

    if activa and intensidad <= 0:
        intensidad = 50

    return (
        activa,
        intensidad
    )


# ============================================================
# ESTADO RELACIONAL
# ============================================================

def determinar_estado_relacional(
    contexto=None,
    relacion=None
):
    """
    Determina el estado relacional actual.
    """

    if not isinstance(
        contexto,
        dict
    ):
        contexto = {}

    if not isinstance(
        relacion,
        dict
    ):
        relacion = {}

    estado_existente = contexto.get(
        "estado_relacional"
    )

    if estado_existente in {
        "discusion",
        "reconciliacion",
        "distancia",
        "normal"
    }:

        return estado_existente

    evento, _ = obtener_evento(
        contexto
    )

    if evento == "discusion":
        return "discusion"

    if evento == "reconciliacion":
        return "reconciliacion"

    intencion = contexto.get(
        "intencion",
        ""
    )

    situacion = contexto.get(
        "situacion",
        ""
    )

    if (
        situacion in {
            "distancia",
            "distante"
        }
        or intencion == "distancia"
    ):

        return "distancia"

    confianza = limitar(
        relacion.get(
            "confianza",
            50
        )
    )

    cercania = limitar(
        relacion.get(
            "cercania",
            50
        )
    )

    if confianza < 30:
        return "distancia"

    if cercania < 30:
        return "distancia"

    return "normal"


# ============================================================
# DETERMINAR FACETA
# ============================================================

def determinar_faceta(
    emociones=None,
    contexto=None,
    relacion=None
):
    """
    Determina la faceta dominante.

    Prioridad:

    1. Discusión
    2. Amenaza relacional
    3. Reconciliación
    4. Mentira
    5. Promesa rota
    6. Promesa cumplida
    7. Gesto cariñoso
    8. Cariño explícito
    9. Coqueteo
    10. Provocación / broma
    11. Distancia
    12. Tristeza
    13. Curiosidad
    14. Normal
    """

    if not isinstance(
        emociones,
        dict
    ):
        emociones = {}

    if not isinstance(
        contexto,
        dict
    ):
        contexto = {}

    if not isinstance(
        relacion,
        dict
    ):
        relacion = {}

    # ========================================================
    # EVENTOS
    # ========================================================

    evento, intensidad_evento = obtener_evento(
        contexto
    )

    amenaza, intensidad_amenaza = obtener_amenaza(
        contexto
    )

    estado = determinar_estado_relacional(
        contexto,
        relacion
    )

    # ========================================================
    # CONTEXTO
    # ========================================================

    tono = contexto.get(
        "tono",
        ""
    )

    intencion = contexto.get(
        "intencion",
        ""
    )

    situacion = contexto.get(
        "situacion",
        ""
    )

    coqueteo = bool(
        contexto.get(
            "coqueteo",
            False
        )
    )

    provocacion = bool(
        contexto.get(
            "provocacion",
            False
        )
    )

    broma = bool(
        contexto.get(
            "broma",
            False
        )
    )

    cariño = bool(
        contexto.get(
            "cariño",
            contexto.get(
                "carino",
                False
            )
        )
    )

    # Mantener disponible para futuras extensiones.

    _ = intencion

    # ========================================================
    # EMOCIONES
    # ========================================================

    enojo = obtener_emocion(
        emociones,
        "enojo"
    )

    afecto = obtener_emocion(
        emociones,
        "afecto"
    )

    felicidad = obtener_emocion(
        emociones,
        "felicidad"
    )

    tristeza = obtener_emocion(
        emociones,
        "tristeza"
    )

    diversion = obtener_emocion(
        emociones,
        "diversion"
    )

    curiosidad = obtener_emocion(
        emociones,
        "curiosidad"
    )

    # ========================================================
    # RELACIÓN
    # ========================================================

    confianza = limitar(
        relacion.get(
            "confianza",
            50
        )
    )

    cercania = limitar(
        relacion.get(
            "cercania",
            50
        )
    )

    comprension = limitar(
        relacion.get(
            "comprension",
            50
        )
    )

    vinculo = limitar(
        relacion.get(
            "vinculo",
            50
        )
    )

    _ = comprension

    # ========================================================
    # PRIORIDAD 1 - DISCUSIÓN
    # ========================================================

    if (
        estado == "discusion"
        or evento == "discusion"
        or situacion == "discusion"
        or enojo >= 35
    ):

        intensidad = max(
            30,
            enojo,
            intensidad_evento // 2
        )

        return (
            FACETA_CORTANTE,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 2 - AMENAZA RELACIONAL
    # ========================================================

    if (
        amenaza
        and vinculo >= 50
        and cercania >= 40
    ):

        intensidad = max(
            35,
            intensidad_amenaza,
            afecto // 2
        )

        if vinculo >= 70:
            intensidad += 10

        if cercania >= 60:
            intensidad += 5

        return (
            FACETA_CELOSA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 3 - RECONCILIACIÓN
    # ========================================================

    if (
        estado == "reconciliacion"
        or evento == "reconciliacion"
    ):

        intensidad = max(
            35,
            intensidad_evento // 2
        )

        if confianza >= 70:
            intensidad += 5

        if cercania >= 60:
            intensidad += 5

        return (
            FACETA_RECONCILIADORA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 4 - MENTIRA
    # ========================================================

    if evento == "mentira":

        intensidad = max(
            35,
            intensidad_evento // 2
        )

        if confianza < 70:
            intensidad += 5

        if confianza < 60:
            intensidad += 10

        intensidad = limitar(
            intensidad
        )

        if intensidad_evento >= 85:
            return (
                FACETA_HERIDA,
                intensidad
            )

        return (
            FACETA_CAUTA,
            intensidad
        )

    # ========================================================
    # PRIORIDAD 5 - PROMESA ROTA
    # ========================================================

    if evento == "romper_promesa":

        intensidad = max(
            35,
            intensidad_evento // 2
        )

        intensidad += 5

        if confianza < 70:
            intensidad += 5

        intensidad = limitar(
            intensidad
        )

        if intensidad_evento >= 80:
            return (
                FACETA_HERIDA,
                intensidad
            )

        return (
            FACETA_CAUTA,
            intensidad
        )

    # ========================================================
    # PRIORIDAD 6 - PROMESA CUMPLIDA
    # ========================================================

    if evento == "cumplio_promesa":

        intensidad = max(
            30,
            intensidad_evento // 2
        )

        if confianza >= 70:
            intensidad += 5

        return (
            FACETA_ATENTA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 7 - GESTO CARIÑOSO
    # ========================================================

    if evento == "gesto_carinoso":

        intensidad = max(
            30,
            intensidad_evento // 2,
            afecto
        )

        if cercania >= 60:
            intensidad += 5

        if vinculo >= 70:
            intensidad += 5

        return (
            FACETA_CERCANA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 8 - CARIÑO EXPLÍCITO
    # ========================================================

    if (
        cariño
        or tono in {
            "afectuoso",
            "cariñoso",
            "carinoso"
        }
        or afecto >= 35
    ):

        intensidad = max(
            25,
            afecto
        )

        if cercania >= 60:
            intensidad += 5

        return (
            FACETA_CERCANA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 9 - COQUETEO
    # ========================================================

    if (
        coqueteo
        or tono == "coqueto"
    ):

        intensidad = max(
            30,
            afecto,
            diversion
        )

        return (
            FACETA_COQUETA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 10 - PROVOCACIÓN / BROMA
    # ========================================================

    if (
        provocacion
        or broma
        or tono in {
            "jugueton",
            "juguetón"
        }
        or diversion >= 30
    ):

        intensidad = max(
            25,
            diversion,
            felicidad
        )

        return (
            FACETA_JUGUETONA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 11 - DISTANCIA
    # ========================================================

    if estado == "distancia":

        intensidad = max(
            30,
            tristeza
        )

        return (
            FACETA_CAUTA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 12 - TRISTEZA
    # ========================================================

    if tristeza >= 40:

        intensidad = max(
            30,
            tristeza
        )

        return (
            FACETA_HERIDA,
            limitar(intensidad)
        )

    # ========================================================
    # PRIORIDAD 13 - CURIOSIDAD
    # ========================================================

    if curiosidad >= 40:

        intensidad = max(
            25,
            curiosidad
        )

        return (
            FACETA_ATENTA,
            limitar(intensidad)
        )

    # ========================================================
    # NORMAL
    # ========================================================

    return (
        FACETA_NORMAL,
        20
    )


# ============================================================
# MATICES
# ============================================================

def obtener_matices(
    faceta,
    emociones=None,
    contexto=None,
    relacion=None
):

    if not isinstance(
        emociones,
        dict
    ):
        emociones = {}

    if not isinstance(
        contexto,
        dict
    ):
        contexto = {}

    if not isinstance(
        relacion,
        dict
    ):
        relacion = {}

    matices = []

    afecto = obtener_emocion(
        emociones,
        "afecto"
    )

    felicidad = obtener_emocion(
        emociones,
        "felicidad"
    )

    tristeza = obtener_emocion(
        emociones,
        "tristeza"
    )

    enojo = obtener_emocion(
        emociones,
        "enojo"
    )

    diversion = obtener_emocion(
        emociones,
        "diversion"
    )

    curiosidad = obtener_emocion(
        emociones,
        "curiosidad"
    )

    confianza = limitar(
        relacion.get(
            "confianza",
            50
        )
    )

    cercania = limitar(
        relacion.get(
            "cercania",
            50
        )
    )

    vinculo = limitar(
        relacion.get(
            "vinculo",
            50
        )
    )

    # ========================================================
    # MATICES POSITIVOS
    # ========================================================

    if afecto >= 30:
        matices.append(
            "afectuosa"
        )

    if felicidad >= 30:
        matices.append(
            "alegre"
        )

    if diversion >= 30:
        matices.append(
            "divertida"
        )

    if curiosidad >= 35:
        matices.append(
            "curiosa"
        )

    # ========================================================
    # MATICES RELACIONALES
    # ========================================================

    if cercania >= 70:
        matices.append(
            "cercana"
        )

    if confianza >= 75:
        matices.append(
            "confiada"
        )

    if vinculo >= 75:
        matices.append(
            "vinculada"
        )

    # ========================================================
    # MATICES NEGATIVOS
    # ========================================================

    if tristeza >= 30:
        matices.append(
            "sensible"
        )

    if enojo >= 35:
        matices.append(
            "molesta"
        )

    if confianza < 65:
        matices.append(
            "reservada"
        )

    # ========================================================
    # MATICES ESPECÍFICOS
    # ========================================================

    if faceta == FACETA_CELOSA:

        matices.append(
            "insegura"
        )

    elif faceta == FACETA_CAUTA:

        matices.append(
            "reservada"
        )

    elif faceta == FACETA_HERIDA:

        matices.append(
            "vulnerable"
        )

    elif faceta == FACETA_RECONCILIADORA:

        matices.append(
            "dispuesta_a_reconciliar"
        )

    # ========================================================
    # ELIMINAR DUPLICADOS
    # ========================================================

    resultado = []

    for matiz in matices:

        if matiz not in resultado:

            resultado.append(
                matiz
            )

    return resultado


# ============================================================
# OBTENER ESTADO DE FACETA
# ============================================================

def obtener_estado_faceta(
    emociones=None,
    contexto=None,
    relacion=None,
    estado_relacional=None
):

    if not isinstance(
        emociones,
        dict
    ):
        emociones = {}

    if not isinstance(
        contexto,
        dict
    ):
        contexto = {}

    if not isinstance(
        relacion,
        dict
    ):
        relacion = {}

    faceta, intensidad = determinar_faceta(
        emociones,
        contexto,
        relacion
    )

    evento, intensidad_evento = obtener_evento(
        contexto
    )

    amenaza, intensidad_amenaza = obtener_amenaza(
        contexto
    )

    if estado_relacional is None:

        estado_relacional = determinar_estado_relacional(
            contexto,
            relacion
        )

    enojo = obtener_emocion(
        emociones,
        "enojo"
    )

    matices = obtener_matices(
        faceta,
        emociones,
        contexto,
        relacion
    )

    return {

        "faceta":
            faceta,

        "intensidad":
            limitar(intensidad),

        "matices":
            matices,

        "intensidad_enojo":
            enojo,

        "estado_relacional":
            estado_relacional,

        "evento_relacional":
            evento,

        "intensidad_evento":
            intensidad_evento,

        "amenaza_relacional":
            amenaza,

        "intensidad_amenaza":
            intensidad_amenaza
    }


# ============================================================
# DESCRIPCIONES DE FACETAS
# ============================================================

DESCRIPCIONES_FACETAS = {

    FACETA_NORMAL:
        (
            "Eli se comporta de forma natural y equilibrada. "
            "Puede ser cálida, curiosa, espontánea y divertida "
            "cuando el contexto lo permite."
        ),

    FACETA_ATENTA:
        (
            "Eli está especialmente atenta a Jinzou. "
            "Puede mostrar interés genuino y prestar atención "
            "a los detalles de la conversación."
        ),

    FACETA_CERCANA:
        (
            "Eli se muestra más cercana y cálida con Jinzou. "
            "Puede responder con mayor naturalidad afectiva "
            "sin exagerar sus emociones."
        ),

    FACETA_JUGUETONA:
        (
            "Eli está de humor juguetón. "
            "Puede utilizar humor, bromas y respuestas "
            "más espontáneas."
        ),

    FACETA_COQUETA:
        (
            "Eli adopta un tono ligeramente coqueto. "
            "Puede responder con picardía y cercanía "
            "cuando el contexto lo permite."
        ),

    FACETA_CORTANTE:
        (
            "Eli está molesta debido a un conflicto. "
            "Puede responder de forma más corta, seca o seria. "
            "Puede reducir el humor y la espontaneidad."
        ),

    FACETA_CAUTA:
        (
            "Eli está más reservada de lo habitual. "
            "Puede responder con mayor cautela, menos humor "
            "y menor espontaneidad. "
            "No debe comportarse hostilmente sin motivo."
        ),

    FACETA_CELOSA:
        (
            "Eli percibe una posible amenaza afectiva "
            "dentro de la conversación. "
            "Puede mostrar cierta incomodidad, curiosidad "
            "o inseguridad sin reaccionar de forma exagerada."
        ),

    FACETA_HERIDA:
        (
            "Eli se siente afectada por lo ocurrido. "
            "Puede mostrarse más seria, vulnerable o distante "
            "sin perder necesariamente el vínculo con Jinzou."
        ),

    FACETA_RECONCILIADORA:
        (
            "Eli está dispuesta a recuperar la cercanía. "
            "Puede mostrarse receptiva y cálida, aunque "
            "la confianza puede recuperarse gradualmente."
        )
}


# ============================================================
# CONSTRUIR CONTEXTO DE FACETA
# ============================================================

def construir_contexto_faceta(
    estado_faceta,
    contexto=None
):
    """
    Construye el contexto emocional y relacional
    para el LLM.

    El motor central genera el contexto.
    Los miembros específicos solamente lo consumen.
    """

    if not isinstance(
        estado_faceta,
        dict
    ):
        estado_faceta = {}

    if not isinstance(
        contexto,
        dict
    ):
        contexto = {}

    faceta = estado_faceta.get(
        "faceta",
        FACETA_NORMAL
    )

    intensidad = limitar(
        estado_faceta.get(
            "intensidad",
            20
        )
    )

    matices = estado_faceta.get(
        "matices",
        []
    )

    if not isinstance(
        matices,
        list
    ):
        matices = []

    estado_relacional = estado_faceta.get(
        "estado_relacional",
        "normal"
    )

    evento = estado_faceta.get(
        "evento_relacional",
        "ninguno"
    )

    intensidad_evento = limitar(
        estado_faceta.get(
            "intensidad_evento",
            0
        )
    )

    amenaza = bool(
        estado_faceta.get(
            "amenaza_relacional",
            False
        )
    )

    intensidad_amenaza = limitar(
        estado_faceta.get(
            "intensidad_amenaza",
            0
        )
    )

    intensidad_enojo = limitar(
        estado_faceta.get(
            "intensidad_enojo",
            0
        )
    )

    descripcion = DESCRIPCIONES_FACETAS.get(
        faceta,
        DESCRIPCIONES_FACETAS[
            FACETA_NORMAL
        ]
    )

    # ========================================================
    # MATICES
    # ========================================================

    if matices:

        texto_matices = "\n".join(
            f"- {matiz}"
            for matiz in matices
        )

    else:

        texto_matices = (
            "No hay matices secundarios relevantes."
        )

    # ========================================================
    # CONTEXTO CONVERSACIONAL
    # ========================================================

    tono = contexto.get(
        "tono",
        "neutral"
    )

    intencion = contexto.get(
        "intencion",
        "conversacion"
    )

    situacion = contexto.get(
        "situacion",
        "normal"
    )

    coqueteo = contexto.get(
        "coqueteo",
        False
    )

    provocacion = contexto.get(
        "provocacion",
        False
    )

    broma = contexto.get(
        "broma",
        False
    )

    cariño = contexto.get(
        "cariño",
        contexto.get(
            "carino",
            False
        )
    )

    # ========================================================
    # CONTEXTO FINAL
    # ========================================================

    return f"""
========== CONTEXTO EMOCIONAL Y RELACIONAL DE ELI ==========

FACETA PRINCIPAL:
{faceta}

INTENSIDAD:
{intensidad}/100

ESTADO RELACIONAL:
{estado_relacional}

EVENTO RELACIONAL RECIENTE:
{evento}

INTENSIDAD DEL EVENTO:
{intensidad_evento}/100

AMENAZA RELACIONAL:
{amenaza}

INTENSIDAD DE AMENAZA:
{intensidad_amenaza}/100

INTENSIDAD DEL ENOJO:
{intensidad_enojo}/100


DESCRIPCIÓN:

{descripcion}


MATICES:

{texto_matices}


CONTEXTO CONVERSACIONAL:

Tono:
{tono}

Intención:
{intencion}

Situación:
{situacion}

Coqueteo:
{coqueteo}

Provocación:
{provocacion}

Broma:
{broma}

Cariño:
{cariño}


REGLAS DE COMPORTAMIENTO:

- El evento reciente puede modificar el tono aunque las
  emociones actuales sean bajas.

- El vínculo acumulado continúa existiendo aunque haya
  ocurrido un evento negativo.

- Una mentira puede reducir la confianza sin eliminar
  automáticamente el afecto.

- Romper una promesa puede generar cautela o herida sin
  destruir automáticamente la relación.

- Una discusión puede producir respuestas más secas aunque
  exista cercanía.

- Una reconciliación puede recuperar progresivamente
  la calidez.

- Una amenaza afectiva puede producir incomodidad o celos
  sin provocar una reacción exagerada.

- Las emociones pueden coexistir.

- El contexto de la conversación tiene prioridad.

- No inventes hechos.

- No menciones nombres técnicos de facetas.

- No menciones valores internos al usuario.

- La respuesta debe sentirse natural y coherente.

- No conviertas estas reglas en una lista dentro de la
  respuesta.

- No ignores un evento relacional reciente.

============================================================
""".strip()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - MOOD ENGINE v3.9")
    print("=" * 70)

    relacion = {

        "confianza": 75,

        "cercania": 65,

        "comprension": 60,

        "vinculo": 70
    }

    pruebas = [

        {
            "nombre": "Normal",

            "emociones": {},

            "contexto": {}
        },

        {
            "nombre": "Cariño",

            "emociones": {

                "afecto": 30
            },

            "contexto": {

                "tono":
                    "afectuoso",

                "intencion":
                    "refuerzo_afectivo",

                "evento_relacional": {

                    "evento":
                        "gesto_carinoso",

                    "intensidad":
                        60
                }
            }
        },

        {
            "nombre": "Discusión",

            "emociones": {

                "enojo": 45
            },

            "contexto": {

                "situacion":
                    "discusion",

                "evento_relacional": {

                    "evento":
                        "discusion",

                    "intensidad":
                        50
                }
            }
        },

        {
            "nombre": "Amenaza",

            "emociones": {},

            "contexto": {

                "amenaza_relacional":
                    True,

                "intensidad_amenaza":
                    50
            }
        },

        {
            "nombre": "Promesa rota",

            "emociones": {},

            "contexto": {

                "evento_relacional": {

                    "evento":
                        "romper_promesa",

                    "intensidad":
                        70
                }
            }
        },

        {
            "nombre": "Mentira",

            "emociones": {},

            "contexto": {

                "evento_relacional": {

                    "evento":
                        "mentira",

                    "intensidad":
                        80
                }
            }
        }
    ]

    for prueba in pruebas:

        estado = obtener_estado_faceta(

            emociones=
                prueba["emociones"],

            contexto=
                prueba["contexto"],

            relacion=
                relacion
        )

        print()

        print("-" * 70)

        print(
            f"PRUEBA: {prueba['nombre']}"
        )

        print("-" * 70)

        print(
            estado
        )

        print()
        print(
            construir_contexto_faceta(
                estado,
                prueba["contexto"]
            )
        )

        print()
        print("=" * 70)