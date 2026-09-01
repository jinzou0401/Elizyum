
# ============================================================
# ELIZYUM - MUNDO / CONTEXT AI v1.0
# ============================================================
#
# Analizador GENERAL de contexto conversacional.
#
# Este módulo pertenece a:
#
#     mundo/context_ai.py
#
# Su función es proporcionar información contextual que pueda
# ser utilizada por cualquier miembro de Elizyum.
#
# NO contiene:
#
# - personalidad específica
# - relaciones específicas
# - emociones específicas de un miembro
# - estados relacionales de un miembro
# - eventos relacionales de un miembro
#
# La lógica especializada de cada miembro debe vivir dentro
# de:
#
#     miembros/<nombre>/
#
# ============================================================


# ============================================================
# UTILIDADES
# ============================================================

def limitar(valor, minimo=0, maximo=100):

    try:
        valor = int(float(valor))
    except (TypeError, ValueError):
        return minimo

    return max(
        minimo,
        min(maximo, valor)
    )


def contiene_alguna(texto, palabras):

    if not isinstance(texto, str):
        return False

    return any(
        palabra in texto
        for palabra in palabras
    )


def normalizar_texto(texto):

    if not isinstance(texto, str):
        return ""

    return texto.lower().strip()


# ============================================================
# DETECTAR TONO
# ============================================================

def detectar_tono(texto):

    texto = normalizar_texto(texto)

    if not texto:
        return "neutral"

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
            "no quería",
            "no queria",
            "hagamos las paces"
        ]
    ):

        return "reconciliador"

    # --------------------------------------------------------
    # HOSTILIDAD
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "idiota",
            "estupido",
            "estúpido",
            "estupida",
            "estúpida",
            "mierda",
            "carajo",
            "joder",
            "cállate",
            "callate",
            "molesto",
            "molesta",
            "enojado",
            "enojada",
            "cabreado",
            "cabreada"
        ]
    ):

        return "hostil"

    # --------------------------------------------------------
    # TRISTEZA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "estoy triste",
            "me siento triste",
            "estoy mal",
            "me siento mal",
            "estoy solo",
            "estoy sola",
            "me siento vacío",
            "me siento vacio",
            "quiero llorar",
            "estoy llorando",
            "me duele"
        ]
    ):

        return "triste"

    # --------------------------------------------------------
    # AFECTO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te quiero",
            "te amo",
            "amor",
            "cariño",
            "linda",
            "bonita",
            "preciosa",
            "guapa"
        ]
    ):

        return "afectuoso"

    # --------------------------------------------------------
    # JUEGO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "jaja",
            "jajaja",
            "xd",
            "😂",
            "🤣",
            "broma",
            "bromeo",
            "jugar"
        ]
    ):

        return "jugueton"

    return "neutral"


# ============================================================
# DETECTAR INTENCIÓN
# ============================================================

def detectar_intencion(texto):

    texto = normalizar_texto(texto)

    if not texto:
        return "ninguna"

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

        return "reconciliacion"

    # --------------------------------------------------------
    # APOYO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "necesito ayuda",
            "ayudame",
            "ayúdame",
            "necesito hablar",
            "me siento mal",
            "estoy triste"
        ]
    ):

        return "buscar_apoyo"

    # --------------------------------------------------------
    # AFECTO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te quiero",
            "te amo",
            "te extraño",
            "te extrano",
            "me importas"
        ]
    ):

        return "refuerzo_afectivo"

    # --------------------------------------------------------
    # JUEGO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "jaja",
            "jajaja",
            "xd",
            "😂",
            "🤣"
        ]
    ):

        return "juego"

    # --------------------------------------------------------
    # COMPARTIR
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te voy a contar",
            "mira esto",
            "adivina",
            "sabes qué",
            "sabes que"
        ]
    ):

        return "compartir"

    return "conversacion"


# ============================================================
# DETECTAR EMOCIONES CONTEXTUALES
# ============================================================

def detectar_emociones_contextuales(texto):

    texto = normalizar_texto(texto)

    emociones = {
        "felicidad": 0,
        "tristeza": 0,
        "enojo": 0,
        "sorpresa": 0,
        "afecto": 0,
        "curiosidad": 0,
        "diversion": 0
    }

    # --------------------------------------------------------
    # AFECTO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "te quiero",
            "te amo",
            "amor",
            "cariño",
            "me importas",
            "te extraño",
            "te extrano"
        ]
    ):

        emociones["afecto"] = 30

    # --------------------------------------------------------
    # TRISTEZA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "estoy triste",
            "me siento triste",
            "estoy mal",
            "me siento mal",
            "estoy solo",
            "estoy sola",
            "me duele"
        ]
    ):

        emociones["tristeza"] = 40

    # --------------------------------------------------------
    # ENOJO
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "estoy enojado",
            "estoy enojada",
            "me molesta",
            "estoy harto",
            "estoy harta",
            "qué mierda",
            "que mierda",
            "carajo"
        ]
    ):

        emociones["enojo"] = 45

    # --------------------------------------------------------
    # DIVERSIÓN
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "jaja",
            "jajaja",
            "xd",
            "😂",
            "🤣",
            "broma",
            "juego"
        ]
    ):

        emociones["diversion"] = 40
        emociones["felicidad"] = 25

    # --------------------------------------------------------
    # SORPRESA
    # --------------------------------------------------------

    if contiene_alguna(
        texto,
        [
            "wow",
            "no puede ser",
            "en serio",
            "enserio"
        ]
    ):

        emociones["sorpresa"] = 20

    # --------------------------------------------------------
    # CURIOSIDAD
    # --------------------------------------------------------

    if "?" in texto:

        emociones["curiosidad"] = 25

    return emociones


# ============================================================
# DETECTAR SEÑALES CONVERSACIONALES GENERALES
# ============================================================

def detectar_senales_conversacionales(texto):

    texto = normalizar_texto(texto)

    return {

        "broma": contiene_alguna(
            texto,
            [
                "jaja",
                "jajaja",
                "xd",
                "😂",
                "🤣",
                "broma",
                "bromeo"
            ]
        ),

        "provocacion": contiene_alguna(
            texto,
            [
                "te reto",
                "te desafío",
                "te desafio",
                "a que no",
                "apuesto a que",
                "te atreves"
            ]
        )
    }


# ============================================================
# ANALIZAR CONTEXTO GENERAL
# ============================================================

def analizar_contexto(texto):

    texto = normalizar_texto(texto)

    tono = detectar_tono(
        texto
    )

    intencion = detectar_intencion(
        texto
    )

    emociones = detectar_emociones_contextuales(
        texto
    )

    senales = detectar_senales_conversacionales(
        texto
    )

    return {

        "tono":
            tono,

        "intencion":
            intencion,

        "emociones":
            emociones,

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
    print("        CONTEXTO GENERAL DETECTADO")
    print("==============================================")

    print()
    print("MENSAJE:")
    print(texto)

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

        "Hola",

        "Jajaja mira esto 😂",

        "Hoy me siento bastante mal",

        "Estoy enojado",

        "Perdón, no quería hacerlo",

        "Necesito ayuda",

        "Te quiero mucho",

        "¿Qué estás haciendo?",

        "Te reto a que lo hagas"
    ]

    for mensaje in mensajes_prueba:

        imprimir_contexto(
            mensaje
        )
