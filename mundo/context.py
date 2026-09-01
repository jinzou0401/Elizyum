
# ============================================================
# ELIZYUM - CONTEXT ENGINE
# mundo/context.py
#
# Motor CENTRAL de contexto de Elizyum.
#
# Este módulo NO pertenece a Eli.
# No contiene personalidad ni comportamiento específico.
#
# Responsabilidad:
#
# - almacenar contexto de entrada
# - normalizar datos
# - obtener tono
# - obtener intención
# - obtener situación
# - obtener emociones/contexto relacional
# - mantener compatibilidad con módulos superiores
#
# Las personalidades específicas pueden adaptar este contexto
# posteriormente.
# ============================================================


# ============================================================
# VALORES BASE
# ============================================================

CONTEXTO_BASE = {
    "situacion": "normal",
    "tono": "neutral",
    "intencion": "conversacion",

    "coqueteo": False,
    "provocacion": False,
    "broma": False,
    "carino": False,

    "evento_relacional": "ninguno",
    "intensidad_evento": 0,

    "amenaza_relacional": False,
    "intensidad_amenaza": 0
}


# ============================================================
# UTILIDADES
# ============================================================

def limitar(valor, minimo=0, maximo=100):

    try:
        valor = int(float(valor))
    except (TypeError, ValueError):
        valor = minimo

    return max(
        minimo,
        min(maximo, valor)
    )


# ============================================================
# CREAR CONTEXTO
# ============================================================

def crear_contexto(
    datos=None
):
    """
    Crea un contexto normalizado.
    """

    contexto = CONTEXTO_BASE.copy()

    if not isinstance(datos, dict):
        return contexto

    contexto.update(
        datos
    )

    return normalizar_contexto(
        contexto
    )


# ============================================================
# NORMALIZAR CONTEXTO
# ============================================================

def normalizar_contexto(
    contexto=None
):
    """
    Garantiza que el contexto tenga una estructura válida.
    """

    if not isinstance(contexto, dict):
        contexto = {}

    resultado = CONTEXTO_BASE.copy()

    for clave in resultado:

        if clave in contexto:
            resultado[clave] = contexto[clave]

    # --------------------------------------------------------
    # EVENTO RELACIONAL
    # --------------------------------------------------------

    evento = resultado.get(
        "evento_relacional",
        "ninguno"
    )

    if isinstance(evento, dict):

        evento_nombre = evento.get(
            "evento",
            "ninguno"
        )

        intensidad = limitar(
            evento.get(
                "intensidad",
                resultado.get(
                    "intensidad_evento",
                    0
                )
            )
        )

        resultado["evento_relacional"] = evento_nombre
        resultado["intensidad_evento"] = intensidad

    else:

        if not isinstance(evento, str):
            evento = "ninguno"

        resultado["evento_relacional"] = evento

        resultado["intensidad_evento"] = limitar(
            resultado.get(
                "intensidad_evento",
                0
            )
        )

    # --------------------------------------------------------
    # AMENAZA RELACIONAL
    # --------------------------------------------------------

    amenaza = resultado.get(
        "amenaza_relacional",
        False
    )

    if isinstance(amenaza, dict):

        activa = amenaza.get(
            "activa",
            amenaza.get(
                "amenaza",
                False
            )
        )

        intensidad = amenaza.get(
            "intensidad",
            resultado.get(
                "intensidad_amenaza",
                0
            )
        )

        resultado["amenaza_relacional"] = bool(
            activa
        )

        resultado["intensidad_amenaza"] = limitar(
            intensidad
        )

    else:

        resultado["amenaza_relacional"] = bool(
            amenaza
        )

        resultado["intensidad_amenaza"] = limitar(
            resultado.get(
                "intensidad_amenaza",
                0
            )
        )

    # --------------------------------------------------------
    # BOOLEANOS
    # --------------------------------------------------------

    resultado["coqueteo"] = bool(
        resultado.get(
            "coqueteo",
            False
        )
    )

    resultado["provocacion"] = bool(
        resultado.get(
            "provocacion",
            False
        )
    )

    resultado["broma"] = bool(
        resultado.get(
            "broma",
            False
        )
    )

    resultado["carino"] = bool(
        resultado.get(
            "carino",
            resultado.get(
                "cariño",
                False
            )
        )
    )

    # --------------------------------------------------------
    # COMPATIBILIDAD
    # --------------------------------------------------------

    # Mantener ambas formas para módulos antiguos/nuevos.

    resultado["cariño"] = resultado["carino"]

    return resultado


# ============================================================
# OBTENER VALOR
# ============================================================

def obtener(
    contexto,
    nombre,
    defecto=None
):
    """
    Obtiene un valor del contexto de forma segura.
    """

    if not isinstance(contexto, dict):
        return defecto

    return contexto.get(
        nombre,
        defecto
    )


# ============================================================
# OBTENER TONO
# ============================================================

def obtener_tono(
    contexto
):

    return obtener(
        contexto,
        "tono",
        "neutral"
    )


# ============================================================
# OBTENER INTENCIÓN
# ============================================================

def obtener_intencion(
    contexto
):

    return obtener(
        contexto,
        "intencion",
        "conversacion"
    )


# ============================================================
# OBTENER SITUACIÓN
# ============================================================

def obtener_situacion(
    contexto
):

    return obtener(
        contexto,
        "situacion",
        "normal"
    )


# ============================================================
# OBTENER EVENTO
# ============================================================

def obtener_evento(
    contexto
):

    contexto = normalizar_contexto(
        contexto
    )

    return (
        contexto["evento_relacional"],
        contexto["intensidad_evento"]
    )


# ============================================================
# OBTENER AMENAZA
# ============================================================

def obtener_amenaza(
    contexto
):

    contexto = normalizar_contexto(
        contexto
    )

    return (
        contexto["amenaza_relacional"],
        contexto["intensidad_amenaza"]
    )


# ============================================================
# OBTENER MARCADORES CONVERSACIONALES
# ============================================================

def obtener_marcadores(
    contexto
):

    contexto = normalizar_contexto(
        contexto
    )

    return {
        "coqueteo": contexto["coqueteo"],
        "provocacion": contexto["provocacion"],
        "broma": contexto["broma"],
        "carino": contexto["carino"]
    }


# ============================================================
# ACTUALIZAR CONTEXTO
# ============================================================

def actualizar(
    contexto,
    datos
):
    """
    Añade o actualiza información del contexto.
    """

    contexto = normalizar_contexto(
        contexto
    )

    if not isinstance(datos, dict):
        return contexto

    contexto.update(
        datos
    )

    return normalizar_contexto(
        contexto
    )


# ============================================================
# RESUMEN
# ============================================================

def obtener_resumen(
    contexto
):

    contexto = normalizar_contexto(
        contexto
    )

    evento, intensidad_evento = obtener_evento(
        contexto
    )

    amenaza, intensidad_amenaza = obtener_amenaza(
        contexto
    )

    return {

        "situacion":
            contexto["situacion"],

        "tono":
            contexto["tono"],

        "intencion":
            contexto["intencion"],

        "coqueteo":
            contexto["coqueteo"],

        "provocacion":
            contexto["provocacion"],

        "broma":
            contexto["broma"],

        "carino":
            contexto["carino"],

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
# CONSTRUIR CONTEXTO PARA MÓDULOS SUPERIORES
# ============================================================

def construir_contexto(
    contexto
):
    """
    Convierte el contexto estructurado en un bloque textual
    reutilizable por motores superiores.
    """

    resumen = obtener_resumen(
        contexto
    )

    return f"""
========== CONTEXTO DE ELIZYUM ==========

SITUACIÓN:
{resumen["situacion"]}

TONO:
{resumen["tono"]}

INTENCIÓN:
{resumen["intencion"]}

COQUETEO:
{resumen["coqueteo"]}

PROVOCACIÓN:
{resumen["provocacion"]}

BROMA:
{resumen["broma"]}

CARIÑO:
{resumen["carino"]}

EVENTO RELACIONAL:
{resumen["evento_relacional"]}

INTENSIDAD DEL EVENTO:
{resumen["intensidad_evento"]}/100

AMENAZA RELACIONAL:
{resumen["amenaza_relacional"]}

INTENSIDAD DE AMENAZA:
{resumen["intensidad_amenaza"]}/100

==========================================
""".strip()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - CONTEXT ENGINE")
    print("=" * 70)

    contexto = crear_contexto({

        "situacion": "discusion",

        "tono": "serio",

        "intencion": "resolver_conflicto",

        "evento_relacional": {
            "evento": "discusion",
            "intensidad": 50
        },

        "amenaza_relacional": {
            "activa": False,
            "intensidad": 0
        }

    })

    print()
    print("CONTEXTO NORMALIZADO")
    print(contexto)

    print()
    print("-" * 70)
    print("RESUMEN")
    print("-" * 70)

    print(
        obtener_resumen(
            contexto
        )
    )

    print()
    print("-" * 70)
    print("CONTEXTO TEXTUAL")
    print("-" * 70)

    print(
        construir_contexto(
            contexto
        )
    )
