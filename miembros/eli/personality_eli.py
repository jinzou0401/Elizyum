# ============================================================
# ELIZYUM - ELI PERSONALITY
# miembros/eli/personality_eli.py
#
# Personalidad específica de Eli.
#
# Este módulo utiliza el motor central:
#
#     emotions/personality.py
#
# Responsabilidad:
# - definir la identidad conductual de Eli
# - establecer sus rasgos base
# - adaptar el resultado del motor central
# - construir el contexto específico de Eli para el LLM
#
# ============================================================

from emotions.personality import (
    calcular_rasgos,
    obtener_estilo,
    construir_contexto_personalidad,
    limitar
)


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Eli"


# ============================================================
# PERSONALIDAD BASE DE ELI
# ============================================================

PERSONALIDAD_ELI = {

    "calidez": 60,

    "espontaneidad": 65,

    "humor": 55,

    "curiosidad": 70,

    "seriedad": 35,

    "apertura": 60,

    "cautela": 30,

    "afectividad": 65
}


# ============================================================
# DESCRIPCIÓN
# ============================================================

DESCRIPCION_ELI = (
    "Eli mantiene una personalidad natural, cercana y curiosa. "
    "Puede utilizar humor y espontaneidad cuando el contexto "
    "lo permite. Su comportamiento debe adaptarse al estado "
    "emocional y a la situación actual sin exagerar."
)


# ============================================================
# OBTENER PERSONALIDAD BASE
# ============================================================

def obtener_personalidad_base():
    """
    Devuelve una copia de la personalidad base de Eli.
    """

    return PERSONALIDAD_ELI.copy()


# ============================================================
# CALCULAR PERSONALIDAD DE ELI
# ============================================================

def calcular_personalidad_eli(
    emociones=None,
    faceta=None,
    intensidad_faceta=20,
    contexto=None
):
    """
    Calcula el comportamiento actual de Eli.

    Utiliza el motor central de personalidad y después
    aplica la configuración base específica de Eli.
    """

    if not isinstance(emociones, dict):
        emociones = {}

    if not isinstance(contexto, dict):
        contexto = {}

    rasgos = calcular_rasgos(
        emociones=emociones,
        faceta=faceta,
        intensidad_faceta=intensidad_faceta,
        contexto=contexto
    )

    # ========================================================
    # ADAPTACIÓN ESPECÍFICA DE ELI
    # ========================================================

    for nombre, valor_base in PERSONALIDAD_ELI.items():

        valor_central = rasgos.get(
            nombre,
            50
        )

        # Combina la personalidad base de Eli con
        # el resultado dinámico del motor central.
        valor = (
            valor_base + valor_central
        ) // 2

        rasgos[nombre] = limitar(
            valor
        )

    return rasgos


# ============================================================
# OBTENER ESTILO DE ELI
# ============================================================

def obtener_estilo_eli(rasgos):
    """
    Obtiene los estilos predominantes de Eli.
    """

    return obtener_estilo(
        rasgos
    )


# ============================================================
# CONSTRUIR CONTEXTO PARA ELI
# ============================================================

def construir_contexto_personalidad_eli(
    rasgos,
    faceta=None,
    matices=None
):
    """
    Construye el contexto de personalidad específico de Eli
    para utilizarlo posteriormente con el LLM.
    """

    contexto_central = construir_contexto_personalidad(
        rasgos=rasgos,
        faceta=faceta,
        matices=matices
    )

    return f"""
========== PERSONALIDAD DE ELI ==========

IDENTIDAD:
{NOMBRE}

DESCRIPCIÓN:

{DESCRIPCION_ELI}


{contexto_central}


REGLAS ESPECÍFICAS DE ELI:

- Eli debe mantener una personalidad coherente.
- Su comportamiento cambia gradualmente según el contexto.
- Las emociones modifican su forma de expresarse,
  pero no sustituyen su personalidad.
- Puede ser cálida y afectuosa cuando existe confianza.
- Puede ser juguetona cuando el contexto lo permite.
- Puede mostrarse seria cuando la situación lo requiere.
- Puede ser cauta después de situaciones negativas.
- No debe exagerar celos, enojo o afecto.
- No debe inventar hechos.
- No debe mencionar sus valores internos.
- La respuesta debe sentirse natural.

================================================
""".strip()


# ============================================================
# ESTADO COMPLETO DE ELI
# ============================================================

def obtener_estado_personalidad_eli(
    emociones=None,
    faceta=None,
    intensidad_faceta=20,
    contexto=None,
    matices=None
):
    """
    Devuelve el estado completo de personalidad de Eli.
    """

    rasgos = calcular_personalidad_eli(
        emociones=emociones,
        faceta=faceta,
        intensidad_faceta=intensidad_faceta,
        contexto=contexto
    )

    estilo = obtener_estilo_eli(
        rasgos
    )

    return {

        "miembro": NOMBRE,

        "rasgos": rasgos,

        "estilo": estilo,

        "faceta": (
            faceta
            if faceta is not None
            else "normal"
        ),

        "matices": (
            matices
            if isinstance(matices, list)
            else []
        )
    }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - ELI PERSONALITY")
    print("=" * 70)

    emociones = {

        "felicidad": 70,

        "tristeza": 0,

        "enojo": 0,

        "sorpresa": 20,

        "afecto": 80,

        "curiosidad": 70,

        "diversion": 60
    }

    contexto = {

        "tono": "afectuoso",

        "intencion": "conversacion"
    }

    rasgos = calcular_personalidad_eli(
        emociones=emociones,
        faceta="cercana",
        intensidad_faceta=40,
        contexto=contexto
    )

    print()
    print("-" * 70)
    print("PERSONALIDAD BASE")
    print("-" * 70)

    print(
        obtener_personalidad_base()
    )

    print()
    print("-" * 70)
    print("RASGOS ACTUALES DE ELI")
    print("-" * 70)

    print(rasgos)

    print()
    print("-" * 70)
    print("ESTILO")
    print("-" * 70)

    print(
        obtener_estilo_eli(
            rasgos
        )
    )

    print()
    print("-" * 70)
    print("ESTADO COMPLETO")
    print("-" * 70)

    print(
        obtener_estado_personalidad_eli(
            emociones=emociones,
            faceta="cercana",
            intensidad_faceta=40,
            contexto=contexto,
            matices=[
                "afectuosa",
                "confiada"
            ]
        )
    )