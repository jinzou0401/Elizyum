
# ============================================================
# ELIZYUM - ELI / CONTEXT AI
# ============================================================
#
# Analizador de contexto especializado de Eli.
#
# Este módulo utiliza el contexto general de:
#
#     mundo/context_ai.py
#
# y añade las reglas específicas de Eli:
#
# - amenaza relacional
# - estado relacional
# - eventos relacionales
#
# ============================================================


# ============================================================
# CONTEXTO GENERAL
# ============================================================

from mundo.context_ai import (
    limitar,
    contiene_alguna,
    normalizar_texto,
    detectar_tono,
    detectar_intencion,
    detectar_emociones_contextuales,
    detectar_senales_conversacionales
)


# ============================================================
# ESTADOS RELACIONALES DE ELI
# ============================================================

ESTADO_NORMAL = "normal"
ESTADO_DISCUSSION = "discusion"
ESTADO_DISTANTE = "distante"
ESTADO_RECONCILIACION = "reconciliacion"


# ============================================================
# DETECTAR AMENAZA RELACIONAL
# ============================================================

def detectar_amenaza_relacional(texto):

    texto = normalizar_texto(texto)

    palabras = [
        "otra chica",
        "otra mujer",
        "otro chico",
        "otro hombre",
        "mi novia",
        "mi novio",
        "una chica",
        "un chico",
        "salí con",
        "sali con",
        "me gusta otra",
        "me gusta otro"
    ]

    if contiene_alguna(
        texto,
        palabras
    ):

        return {
            "amenaza_relacional": True,
            "intensidad": 60
        }

    return {
        "amenaza_relacional": False,
        "intensidad": 0
    }


# ============================================================
# DETECTAR ESTADO RELACIONAL
# ============================================================

def detectar_estado_relacional(texto):

    texto = normalizar_texto(texto)

    # --------------------------------------------------------
    # RECONCILIACIÓN
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "perdón",
            "perdon",
            "lo siento",
            "disculpa",
            "disculpame",
            "discúlpame",
            "hagamos las paces"
        ]
    ):

        return ESTADO_RECONCILIACION

    # --------------------------------------------------------
    # DISCUSIÓN
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "estoy enojado",
            "estoy enojada",
            "me molesta",
            "no estoy de acuerdo",
            "déjame",
            "dejame",
            "cállate",
            "callate"
        ]
    ):

        return ESTADO_DISCUSSION

    # --------------------------------------------------------
    # DISTANCIA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "necesito espacio",
            "déjame solo",
            "dejame solo",
            "déjame tranquila",
            "dejame tranquila",
            "no quiero hablar"
        ]
    ):

        return ESTADO_DISTANTE

    return ESTADO_NORMAL


# ============================================================
# DETECTAR EVENTO RELACIONAL
# ============================================================

def detectar_evento_relacional(texto):

    texto = normalizar_texto(texto)

    # --------------------------------------------------------
    # RECONCILIACIÓN
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "perdón",
            "perdon",
            "lo siento",
            "disculpa",
            "disculpame",
            "discúlpame",
            "hagamos las paces"
        ]
    ):

        return {
            "evento": "reconciliacion",
            "intensidad": 60
        }

    # --------------------------------------------------------
    # APOYO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te apoyo",
            "estoy contigo",
            "cuenta conmigo",
            "no estás sola",
            "no estas sola",
            "no te voy a dejar"
        ]
    ):

        return {
            "evento": "apoyo",
            "intensidad": 60
        }

    # --------------------------------------------------------
    # AFECTO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te quiero",
            "te amo",
            "me importas",
            "te extraño",
            "te extrano"
        ]
    ):

        return {
            "evento": "gesto_carinoso",
            "intensidad": 60
        }

    # --------------------------------------------------------
    # PROMESA CUMPLIDA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "cumplí",
            "cumpli",
            "lo prometido",
            "cumplí mi promesa",
            "cumpli mi promesa"
        ]
    ):

        return {
            "evento": "cumplio_promesa",
            "intensidad": 70
        }

    # --------------------------------------------------------
    # ROMPER PROMESA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "rompí mi promesa",
            "rompi mi promesa",
            "no cumplí",
            "no cumpli"
        ]
    ):

        return {
            "evento": "romper_promesa",
            "intensidad": 70
        }

    # --------------------------------------------------------
    # MENTIRA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te mentí",
            "te menti",
            "era mentira",
            "te engañé",
            "te engañe"
        ]
    ):

        return {
            "evento": "mentira",
            "intensidad": 80
        }

    # --------------------------------------------------------
    # DISTANCIA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "no quiero hablar",
            "déjame solo",
            "dejame solo",
            "necesito espacio"
        ]
    ):

        return {
            "evento": "ignorar",
            "intensidad": 50
        }

    # --------------------------------------------------------
    # DISCUSIÓN
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "estoy enojado",
            "estoy enojada",
            "me molesta",
            "no estoy de acuerdo"
        ]
    ):

        return {
            "evento": "discusion",
            "intensidad": 50
        }

    # --------------------------------------------------------
    # SIN EVENTO
    # --------------------------------------------------------

    return {
        "evento": None,
        "intensidad": 0
    }


# ============================================================
# ANALIZAR CONTEXTO DE ELI
# ============================================================

def analizar_contexto(texto):

    texto = normalizar_texto(texto)

    # --------------------------------------------------------
    # CONTEXTO GENERAL
    # --------------------------------------------------------

    contexto_general = {
        "tono": detectar_tono(texto),
        "intencion": detectar_intencion(texto),
        "emociones": detectar_emociones_contextuales(texto),
        "senales": detectar_senales_conversacionales(texto)
    }

    # --------------------------------------------------------
    # CONTEXTO RELACIONAL DE ELI
    # --------------------------------------------------------

    amenaza = detectar_amenaza_relacional(
        texto
    )

    estado_relacional = detectar_estado_relacional(
        texto
    )

    evento_relacional = detectar_evento_relacional(
        texto
    )

    senales = contexto_general["senales"]

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    return {

        "situacion":
            estado_relacional,

        "tono":
            contexto_general["tono"],

        "intencion":
            contexto_general["intencion"],

        "emociones":
            contexto_general["emociones"],

        "contexto_relacional":
            amenaza,

        "estado_relacional":
            estado_relacional,

        "evento_relacional":
            evento_relacional,

        "broma":
            senales["broma"],

        "provocacion":
            senales["provocacion"]
    }


# ============================================================
# COMPATIBILIDAD
# ============================================================

def detectar_contexto(texto):

    return analizar_contexto(
        texto
    )


# ============================================================
# DEBUG
# ============================================================

def imprimir_contexto(texto):

    contexto = analizar_contexto(
        texto
    )

    print()
    print("==============================================")
    print("       CONTEXTO DE ELI DETECTADO")
    print("==============================================")

    print()
    print("MENSAJE:")
    print(texto)

    print()
    print("SITUACIÓN:")
    print(contexto["situacion"])

    print()
    print("TONO:")
    print(contexto["tono"])

    print()
    print("INTENCIÓN:")
    print(contexto["intencion"])

    print()
    print("EMOCIONES:")
    print(contexto["emociones"])

    print()
    print("CONTEXTO RELACIONAL:")
    print(contexto["contexto_relacional"])

    print()
    print("ESTADO RELACIONAL:")
    print(contexto["estado_relacional"])

    print()
    print("EVENTO RELACIONAL:")
    print(contexto["evento_relacional"])

    print()
    print("SEÑALES:")
    print(
        {
            "broma": contexto["broma"],
            "provocacion": contexto["provocacion"]
        }
    )

    print()
    print("==============================================")


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    mensajes_prueba = [

        "Hola Eli",

        "Jajaja mira esto 😂",

        "Hoy me siento bastante mal",

        "Estoy enojado contigo",

        "Perdón Eli, no quería hacerlo",

        "Me gusta otra chica",

        "Necesito espacio",

        "Te quiero mucho",

        "Cumplí mi promesa",

        "Te mentí"
    ]

    for mensaje in mensajes_prueba:

        imprimir_contexto(
            mensaje
        )

